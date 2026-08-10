from abc import ABC, abstractmethod
from typing import Union, Optional

import pandas as pd
import numpy as np
import xarray as xr
import xagg as xa
from loguru import logger
from epiweeks import Week

from satellite.geo.models import ADM, ADMBase

xr.set_options(keep_attrs=True)


class CopeExtensionBase(ABC):
    """
    This class is an `xr.Dataset` extension base class. It's children will
    works as a dataset layer with the purpose of enhancing the xarray dataset
    with new methods. The expect input dataset is an `netCDF4` file from
    Copernicus API; this extension will work on certain data variables,
    the method that extracts with the correct parameters can be found in
    `extract_reanalysis` module.

    Usage:
    ```
    ds.cope.to_dataframe(ADM)
    ds.cope.adm_ds(ADM)
    ```
    See also: satellite.ADM2

    date       : datetime object.
    epiweek    : Epidemiological week (format: YYYYWW)
    temp_min   : Minimum┐
    temp_med   : Average├─ temperature in `celcius degrees` given a geocode.
    temp_max   : Maximum┘
    precip_min : Minimum┐
    precip_med : Average├─ of total precipitation in `mm` given a geocode.
    precip_max : Maximum┘
    precip_tot : Total daily precipitation in `mm` given a geocode. ERA5-Land
                 `tp` is accumulated from 00 UTC, so the daily total of a UTC
                 day is the `00:00` sample of the following day.
    pressao_min: Minimum┐
    pressao_med: Average├─ sea level pressure in `hPa` given a geocode.
    pressao_max: Maximum┘
    umid_min   : Minimum┐
    umid_med   : Average├─ percentage of relative humidity given a geocode.
    umid_max   : Maximum┘
    """

    @abstractmethod
    def to_dataframe(self, adms: Union[list[ADM], ADM]) -> pd.DataFrame:
        pass

    @abstractmethod
    def adm_ds(self, adm: ADM) -> xr.Dataset:
        pass

    @abstractmethod
    def to_sql(self, adms, con, tablename, schema, raw, **kwargs) -> None:
        """
        Reads the data for each geocode and insert the rows into the
        database one by one, created by sqlalchemy engine with the URI.
        This method is convenient to prevent the memory overhead when
        executing with a large amount of geocodes.
        """
        pass


@xr.register_dataset_accessor("cope")
class CopeExtension(CopeExtensionBase):
    def __init__(self, xarray_ds: xr.Dataset):
        self._ds = xarray_ds

    def to_dataframe(self, adms: Union[list[ADM], ADM]) -> pd.DataFrame:
        adms = [adms] if isinstance(adms, ADMBase) else adms
        dfs = []
        for adm in adms:
            dfs.append(_adm_to_dataframe(self._ds, adm=adm))
        return pd.concat(dfs, ignore_index=True)

    def to_sql(
        self,
        adms: Union[list[int], int],
        con,
        tablename: str,
        schema: Optional[str] = None,
        raw: bool = False,
        verbose: bool = True,
    ) -> None:
        adms = [adms] if isinstance(adms, ADMBase) else adms
        for adm in adms:
            _geocode_to_sql(
                dataset=self._ds,
                adm=adm,
                con=con,
                schema=schema,
                tablename=tablename,
            )
            if verbose:
                logger.info(
                    f"{adm.code} updated on {schema + '.' if schema else ''}{tablename}"
                )

    def adm_ds(self, adm: ADM):
        return _adm_ds(ds=self._ds, adm=adm)

    def batch_to_df(
        self, gdf: "pd.DataFrame", exclude_geocodes: Optional[set] = None
    ) -> "pd.DataFrame":
        """Compute all weather stats for all municipalities at once.

        Returns DataFrame with columns matching copernicus_bra:
        date, geocode, epiweek, temp_min, temp_med, temp_max,
        precip_min, precip_med, precip_max, precip_tot,
        pressao_min, pressao_med, pressao_max,
        umid_min, umid_med, umid_max.

        Much faster than per-ADM to_dataframe/to_sql.
        """
        import pandas as pd
        import numpy as np
        from epiweeks import Week

        ds = _convert_units(self._ds)
        weightmap = xa.pixel_overlaps(ds, gdf, silent=True)
        agg = xa.aggregate(ds, weightmap, silent=True).to_dataset().sortby("time")

        precip_tot_da = None
        if "precip" in agg.data_vars:
            precip_tot_da = _daily_precip_tot(agg)
            agg["precip"] = _compute_hourly_increments(agg["precip"])

        gb = agg.resample(time="1D")
        gmin = gb.map(np.min).drop_vars(
            ["code", "name", "adm1", "adm0"], errors="ignore"
        )
        gmean = gb.map(np.mean).drop_vars(
            ["code", "name", "adm1", "adm0"], errors="ignore"
        )
        gmax = gb.map(np.max).drop_vars(
            ["code", "name", "adm1", "adm0"], errors="ignore"
        )

        codes = np.array([str(c) for c in agg.code.values])
        if exclude_geocodes:
            keep = np.array([c not in exclude_geocodes for c in codes])
            pi_range = np.where(keep)[0]
        else:
            pi_range = range(len(codes))

        varnames = sorted(gmin.data_vars)
        prefixes = {}
        for v in varnames:
            if v.endswith("_min"):
                prefixes.setdefault(v[:-4], {})["min"] = v
            elif v.endswith("_med"):
                prefixes.setdefault(v[:-4], {})["med"] = v
            elif v.endswith("_max"):
                prefixes.setdefault(v[:-4], {})["max"] = v

        records = []
        for pi in pi_range:
            for ti in range(len(gmin.time)):
                dt = pd.to_datetime(gmin.time.values[ti]).date()
                epiweek = int(str(Week.fromdate(dt)))
                row = {"date": dt, "geocode": codes[pi], "epiweek": epiweek}

                for prefix, cols in prefixes.items():
                    for suffix in ("min", "med", "max"):
                        key = f"{prefix}_{suffix}"
                        col_name = cols.get(suffix)
                        if col_name and col_name in gmin.data_vars:
                            source = {"min": gmin, "med": gmean, "max": gmax}[suffix]
                            val = float(
                                source[col_name].isel(poly_idx=pi, time=ti).values
                            )
                            row[key] = round(val, 4) if not np.isnan(val) else None

                if precip_tot_da is not None:
                    pt = float(precip_tot_da.isel(poly_idx=pi, time=ti).values)
                    row["precip_tot"] = round(pt, 4) if not np.isnan(pt) else None

                records.append(row)

        return pd.DataFrame(records)


def _geocode_to_sql(
    dataset: xr.Dataset,
    adm: ADM,
    con,
    schema: str,
    tablename: str,
) -> None:
    df = _adm_to_dataframe(dataset=dataset, adm=adm)
    df.to_sql(
        name=tablename,
        schema=schema,
        con=con,
        if_exists="append",
        index=False,
    )
    del df


def _adm_to_dataframe(dataset: xr.Dataset, adm: ADM) -> pd.DataFrame:
    ds = _adm_ds(ds=dataset, adm=adm)
    df = ds.to_dataframe().reset_index()
    del ds
    df = df.drop(columns=["poly_idx", "name"])
    if df.empty:
        return pd.DataFrame(
            columns=["time", "code", "epiweek"]
            + [c for c in df.columns if c not in ("poly_idx", "name", "time", "code")]
        )
    df = df.assign(epiweek=int(str(Week.fromdate(pd.to_datetime(df.time).iloc[0]))))
    columns_to_round = list(
        set(df.columns).difference(set(["time", "code", "epiweek"]))
    )
    df[columns_to_round] = df[columns_to_round].apply(lambda x: np.round(x, 4))
    df = df.rename(columns={"time": "date", "code": "geocode"})
    return df


def _adm_ds(ds: xr.Dataset, adm: ADM) -> xr.Dataset:
    ds = _convert_units(ds)
    weightmap = xa.pixel_overlaps(ds, adm.to_dataframe(), silent=True)
    ds = xa.aggregate(ds, weightmap, silent=True).to_dataset().sortby("time")

    precip_tot_da = None
    if "precip" in ds.data_vars:
        precip_tot_da = _daily_precip_tot(ds)
        ds["precip"] = _compute_hourly_increments(ds["precip"])

    gb = ds.resample(time="1D")
    gmin, gmean, gmax = (
        _reduce_by(gb, np.min, "min"),
        _reduce_by(gb, np.mean, "med"),
        _reduce_by(gb, np.max, "max"),
    )
    coords = [ds.code, ds.name, gmin, gmean, gmax]
    if precip_tot_da is not None:
        coords.append(precip_tot_da)
    result = xr.combine_by_coords(coords, data_vars="all")
    if "precip_tot" in result.data_vars:
        result = result.dropna(dim="time", subset=["precip_tot"], how="all")
    return result


def _daily_precip_tot(ds: xr.Dataset) -> xr.DataArray:
    precip00 = ds["precip"].sel(time=ds.time.dt.hour == 0).sortby("time")
    return precip00.shift(time=-1).rename("precip_tot")


def _compute_hourly_increments(da: xr.DataArray) -> xr.DataArray:
    """Convert cumulative tp to hourly increments.

    ERA5-Land tp at 00:00 is the accumulated total for the previous day.
    At other hours (03, 06, 09, ...) it is accumulated from 00:00 of the
    current day. So the increment for each step is:

    - 00:00: the value itself (previous day's total, used as-is for precip_tot)
    - First step after 00:00: the value itself (accumulation from midnight)
    - Subsequent steps: value[i] - value[i-1]
    - Last step before next 00:00: value[i] - value[i-1] (already correct
      since the next 00:00 starts a new accumulation cycle)
    """
    da = da.sortby("time")
    hours = da.time.dt.hour.values
    increments = da.copy()
    ntimes = len(hours)

    orig_shape = da.values.shape
    flat = da.values.reshape(-1, ntimes)

    for row in range(flat.shape[0]):
        src = flat[row]
        out = np.empty(ntimes)
        out[0] = src[0]  # 00:00 = previous day total

        for i in range(1, ntimes):
            if hours[i - 1] == 0:
                # Previous step was 00:00: current step starts a new
                # accumulation cycle from midnight, so the increment IS
                # the value itself (not a diff from 00:00).
                out[i] = src[i]
            else:
                out[i] = src[i] - src[i - 1]

        flat[row] = out

    np.clip(flat, 0, None, out=flat)
    increments.values = flat.reshape(orig_shape)
    return increments


def _reduce_by(ds: xr.Dataset, func, prefix: str) -> xr.Dataset:
    ds = ds.apply(func=func).drop_vars(
        ["code", "name", "adm1", "adm0"], errors="ignore"
    )

    return ds.rename(
        dict(
            zip(
                list(ds.data_vars),
                list(map(lambda x: f"{x}_{prefix}", list(ds.data_vars))),
            )
        )
    )


def _convert_units(ds: xr.Dataset) -> xr.Dataset:
    _ds = ds.copy()
    del ds
    _vars = list(_ds.data_vars.keys())

    parsed_vars = {}

    if "valid_time" in _ds.coords:
        parsed_vars["valid_time"] = "time"

    if "t2m" in _vars:
        _ds["t2m"] = _ds.t2m - 273.15
        _ds["t2m"].attrs = {"units": "degC", "long_name": "Temperatura"}
        parsed_vars["t2m"] = "temp"

        if "d2m" in _vars:
            _ds["d2m"] = _ds.d2m - 273.15

            e = 6.112 * np.exp(17.67 * _ds.d2m / (_ds.d2m + 243.5))
            es = 6.112 * np.exp(17.67 * _ds.t2m / (_ds.t2m + 243.5))
            rh = (e / es) * 100

            _ds["d2m"] = rh
            _ds["d2m"].attrs = {
                "units": "pct",
                "long_name": "Umidade Relativa do Ar",
            }
            parsed_vars["d2m"] = "umid"

    if "tp" in _vars:
        _ds["tp"] = _ds.tp * 1000
        _ds["tp"] = _ds.tp.round(5)
        _ds["tp"].attrs = {"units": "mm", "long_name": "Precipitação"}
        parsed_vars["tp"] = "precip"

    if "sp" in _vars:
        _ds["sp"] = _ds.sp * 0.00000986923
        _ds["sp"].attrs = {
            "units": "atm",
            "long_name": "Pressão ao Nível do Mar",
        }
        parsed_vars["sp"] = "pressao"

    return _ds.rename(parsed_vars)
