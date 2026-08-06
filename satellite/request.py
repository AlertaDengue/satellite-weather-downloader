from typing import Optional, Dict, Literal
from datetime import date, datetime, timedelta
from pathlib import Path

import xarray as xr
from loguru import logger

from satellite.models import ERA5LandRequest, ERA5LandSpecs, DataSet

_DEFAULT_VARIABLES = [
    "2m_temperature",
    "total_precipitation",
    "2m_dewpoint_temperature",
    "surface_pressure",
]

_DEFAULT_TIMES = [
    "03:00",
    "06:00",
    "09:00",
    "12:00",
    "15:00",
    "18:00",
    "21:00",
    "00:00",
]


class ReanalysisERA5Land:
    """High-level interface for ERA5-Land reanalysis data.

    Handles download, precipitation accumulation correction, and dataset
    loading.  The output dataset is ready for use with the ``.cope``
    extension (``ds.cope.to_dataframe(adm)``)

    Usage::

        req = ReanalysisERA5Land(locale="BRA", date="2024-01-01/2024-01-05")
        ds = req.run("my_output")
        df = ds.cope.to_dataframe(ADM2.get(code="3304557", adm0="BRA"))
    """

    def __init__(
        self,
        variable: Optional[list[str]] = None,
        date: Optional[str] = None,
        time: Optional[list[str]] = None,
        locale: Optional[Literal["BRA", "ARG"]] = None,
        area: Optional[Dict[Literal["N", "S", "W", "E"], float]] = None,
        format: Literal["grib", "netcdf"] = "netcdf",
        download_format: Literal["zip", "unarchived"] = "zip",
        api_token: Optional[str] = None,
    ):
        self.variable = variable or list(_DEFAULT_VARIABLES)
        self.date = date or str((datetime.now() - timedelta(days=6)).date())
        self.time = time or list(_DEFAULT_TIMES)
        self.locale = locale
        self.area = area
        self.format = format
        self.download_format = download_format
        self.api_token = api_token

    def _build_request(self, **overrides) -> ERA5LandSpecs:
        kw: dict = dict(
            product_type=["reanalysis"],
            variable=self.variable,
            date=self.date,
            time=self.time,
            locale=self.locale,
            area=self.area,
            format=self.format,
            download_format=self.download_format,
        )
        kw.update(overrides)
        return ERA5LandSpecs(**kw)  # type: ignore[arg-type]

    def _download(self, output: str, **overrides) -> xr.Dataset:
        req = self._build_request(**overrides)
        ds = _load_or_download(
            ERA5LandRequest(api_key=self.api_token, request=req), output
        )
        return ds

    def run(self, output: str) -> xr.Dataset:
        """Download and return the full reanalysis dataset.

        If ``total_precipitation`` is among the requested variables the
        extra 00:00 sample of the next day is fetched automatically so that
        daily totals are correct.
        """
        ds = self._download(output)

        if "total_precipitation" not in self.variable:
            return ds

        tp_next_day = self._download_tp_next_day(output)
        return xr.concat([ds, tp_next_day], dim="time", combine_attrs="override")

    def _download_tp_next_day(self, output: str) -> xr.Dataset:
        next_day = _next_day(self.date)
        return self._download(
            f"{Path(output).with_suffix('')}_tp",
            date=next_day,
            variable=["total_precipitation"],
            time=["00:00"],
        )


def reanalysis_era5_land(
    output: str,
    api_token: Optional[str] = None,
    product_type: Optional[list[str]] = None,
    variable: Optional[list[str]] = None,
    date: Optional[str] = None,
    time: Optional[list[str]] = None,
    locale: Optional[Literal["BRA", "ARG"]] = None,
    area: Optional[Dict[Literal["N", "S", "W", "E"], float]] = None,
    format: Literal["grib", "netcdf"] = "netcdf",
    download_format: Literal["zip", "unarchived"] = "zip",
) -> xr.Dataset:
    """Download ERA5-Land reanalysis and return an ``xr.Dataset``.

    This is a convenience function that wraps :class:`ReanalysisERA5Land`.
    See the class docstring for parameter details.
    """
    overrides = {}
    if product_type is not None:
        overrides["product_type"] = product_type

    req = ReanalysisERA5Land(
        variable=variable,
        date=date,
        time=time,
        locale=locale,
        area=area,
        format=format,
        download_format=download_format,
        api_token=api_token,
    )
    ds = req._download(output, **overrides)

    if variable is not None and "total_precipitation" not in variable:
        return ds

    if variable is None and "total_precipitation" not in _DEFAULT_VARIABLES:
        return ds

    tp_next_day = req._download_tp_next_day(output)
    return xr.concat([ds, tp_next_day], dim="time", combine_attrs="override")


def _next_day(date_str: str) -> str:
    end = date_str.split("/")[-1]
    return (date.fromisoformat(end) + timedelta(days=1)).isoformat()


def _load_or_download(req: ERA5LandRequest, output: str) -> xr.Dataset:
    path = req.download(output)

    if not Path(path).exists():
        raise FileNotFoundError(
            f"Download produced no file at {path}. "
            "Check your CDS API credentials and network connection."
        )

    try:
        ds = DataSet.from_netcdf(path)
    except Exception as e:
        logger.warning(f"Failed to load {path}, re-downloading: {e}")
        Path(path).unlink(missing_ok=True)
        path = req.download(output)
        ds = DataSet.from_netcdf(path)

    if "valid_time" in ds.coords:
        ds = ds.rename({"valid_time": "time"})
    return ds
