from datetime import date, datetime, timedelta
from typing import Dict, Literal, Optional
from abc import ABC, abstractmethod
from pathlib import Path
import zipfile
import uuid
import os
import io

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from requests.exceptions import RequestException
from dotenv import load_dotenv
from cdsapi.api import Client
import xarray as xr

load_dotenv()


class Area:
    def __init__(self, locale: Optional[str] = None):
        if locale:
            locale = locale.upper()
            if locale not in self.areas:
                raise ValueError(
                    "Unkown locale. Please use the predefined areas"
                    "or Area.from_coords() function. Pre-defined locales: "
                    f"{list(self.areas)}"
                )
        self.locale = locale

    def __repr__(self) -> str:
        return f"Area('{self.locale}')"

    areas = {
        None: {"N": 90.0, "W": -180.0, "S": -90.0, "E": 180.0},
        "BRA": {"N": 5.5, "W": -74.0, "S": -33.75, "E": -32.25},
        "ARG": {"N": -21.0, "W": -74.0, "S": -56.0, "E": -53.0},
    }

    @property
    def bbox(self):
        c = self.areas[self.locale]
        return [c["N"], c["W"], c["S"], c["E"]]

    @classmethod
    def from_coords(
        cls, north: float, west: float, south: float, east: float
    ) -> "Area":
        bbox = {"N": north, "W": west, "S": south, "E": east}
        cls._validate_bbox(bbox)

        for name, area in cls.areas.items():
            if area == bbox:
                return cls(name)

        custom = f"CUSTOM_{len(cls.areas)}"
        cls.areas[custom] = bbox
        return cls(custom)

    @classmethod
    def _validate_bbox(cls, bbox: dict[str, float]) -> None:
        if abs(bbox["N"]) > 90 or abs(bbox["S"]) > 90:
            raise ValueError("Latitude must be between -90 and 90")

        if abs(bbox["W"]) > 180 or abs(bbox["E"]) > 180:
            raise ValueError("Longitude must be between -180 and 180")


class Specs(BaseModel): ...


class BaseRequest(ABC, BaseModel):
    name: str = Field(
        ..., description="Copernicus dataset. e.g: 'reanalysis-era5-land'"
    )
    request: Specs = Field(
        ..., description="Request specifications. Expects a Specs child"
    )

    @abstractmethod
    def download(self, output: str) -> str: ...

    @classmethod
    def get_client(cls, key: Optional[str] = None) -> Client:
        if not key:
            key = os.getenv("CDSAPI_TOKEN", None)
            if not key:
                raise ValueError(
                    "Environment variable CDSAPI_TOKEN not found in the system.\n"
                    'Execute `$ export CDSAPI_TOKEN="<MY_UID_TOKEN>"` '
                    "or pass the key in the request to fix.\n"
                    "These credentials are found in your Copernicus User Page: \n"
                    "https://cds.climate.copernicus.eu/user/<USER>"
                )

        uuid.UUID(key)

        client = Client(
            url="https://cds.climate.copernicus.eu/api",
            key=key,
        )

        return client

    class Config:
        arbitrary_types_allowed = True


class ERA5LandSpecs(Specs):
    product_type: list[str] = Field(
        default=["reanalysis"],
        description="List of product types (e.g., ['reanalysis'])",
    )
    variable: list[str] = Field(
        default=[
            "2m_temperature",
            "total_precipitation",
            "2m_dewpoint_temperature",
            "surface_pressure",
        ],
        description="List of variables (e.g., ['2m_temperature'])",
        validate_default=True,
    )
    date: str = Field(
        default=str((datetime.now() - timedelta(days=6)).date()),
        description=(
            "ISO Format date, can also be a date range with '/' "
            "(e.g. 2020-10-25 or 2020-10-25/2022-01-30)"
        ),
        validate_default=True,
    )
    # year: str
    # month: str
    # day: list[str]
    time: list[str] = Field(
        default=[
            "00:00",
            "03:00",
            "06:00",
            "09:00",
            "12:00",
            "15:00",
            "18:00",
            "21:00",
        ],
        description=("List of hours in each day to be downloaded"),
        validate_default=True,
    )
    locale: Optional[Literal["BRA", "ARG"]] = Field(
        default=None,
        description=(
            "Auto set `area` based on a country code using a pre-defined bbox"
            f" in Area class: {list(Area.areas)}"
        ),
        validate_default=True,
    )
    area: Optional[Dict[Literal["N", "S", "W", "E"], float]] = Field(
        default=None,
        description=(
            "Auto set `area` based on a country code using a pre-defined bbox"
            "in Area class"
        ),
        validate_default=True,
    )
    format: Literal["grib", "netcdf"] = Field(default="netcdf")
    download_format: Literal["zip", "unarchived"] = Field(default="zip")

    @field_validator("product_type")
    @classmethod
    def validate_product_type(cls, value: str) -> str:
        assert value, "`product_type` must be a list of strings"
        return value

    @field_validator("variable")
    @classmethod
    def validate_variable(cls, value: list[str]) -> list[str]:
        assert value, "`variable` must be a list of strings"
        return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        assert isinstance(value, str), "`date` must be a string"

        if "/" in value:
            ini, end = value.split("/")
            date.fromisoformat(end)
        else:
            ini = value
        date.fromisoformat(ini)
        return value

    @field_validator("time")
    @classmethod
    def validate_time(cls, value: list[str]) -> list[str]:
        assert value, "empty time list"
        for time in value:
            assert ":" in time, "format: 'hh:00'. e.g '23:00'"
            hour, mins = time.split(":")
            assert mins == "00", "minutes must be 00. e.g '23:00'"
            assert hour in [
                f"{h:02d}" for h in range(24)
            ], f"invalid hour {hour}. e.g '23:00'"
        return value

    @field_validator("area")
    @classmethod
    def validate_area(
        cls,
        value: Optional[dict[Literal["N", "S", "W", "E"], float]],
        values: ValidationInfo,
    ) -> Optional[dict[Literal["N", "S", "W", "E"], float]]:
        if value is not None:
            return Area.from_coords(
                north=value["N"],
                west=value["W"],
                south=value["S"],
                east=value["E"],
            ).bbox

        locale = values.data["locale"]
        if locale:
            return Area(locale).bbox
        return Area().bbox


class ERA5LandRequest(BaseRequest):
    """
    https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
    """

    api_key: Optional[str] = Field(default=None)
    name: Literal["reanalysis-era5-land"] = Field(
        default="reanalysis-era5-land", validate_default=True
    )
    request: ERA5LandSpecs = Field(default=ERA5LandSpecs(), validate_default=True)

    # pylint: disable=maybe-no-member
    def download(self, output: str) -> str:
        request: ERA5LandSpecs = self.request
        output = Path(output)

        if request.download_format == "zip":
            output = output.with_suffix(".zip")
        else:
            if request.format == "netcdf":
                output = output.with_suffix(".nc")
            else:
                output = output.with_suffix(".grib")

        if not output.is_dir() and output.exists():
            return str(output)

        client = self.get_client(self.api_key)

        try:
            client.retrieve(
                self.name,
                {
                    "product_type": request.product_type,
                    "variable": request.variable,
                    "date": request.date,
                    "time": request.time,
                    "area": request.area,
                    "data_format": request.format,
                    "download_format": request.download_format,
                },
                str(output),
            )
        except (RequestException, KeyboardInterrupt) as e:
            output.unlink(missing_ok=True)
            raise e

        return str(output)


class DataSet:
    @classmethod
    def from_netcdf(cls, fpath: str) -> xr.Dataset:
        if Path(fpath).suffix == ".zip":
            with zipfile.ZipFile(fpath, "r") as zip_files:
                zfiles = zip_files.namelist()
                if len(zfiles) != 1:
                    raise ValueError(f"multiple or no data found in {fpath}")
                with zip_files.open(zfiles[0]) as zfile:
                    data = zfile.read()
                    return xr.open_dataset(io.BytesIO(data), engine="h5netcdf")
        return xr.open_dataset(fpath, engine="netcdf4")
