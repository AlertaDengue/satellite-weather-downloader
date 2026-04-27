import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import loguru
import numpy as np
import pandas as pd
import xarray as xr

from satellite import DataSet, ADM2, ADM0
from satellite.extensions.cope import CopeExtension

logger = loguru.logger


class TestWeatherCopebr(unittest.TestCase):
    def setUp(self) -> None:
        self.file = Path(__file__).parent / "data" / "BR_20230101.nc"
        self.dataset = DataSet.from_netcdf((str(self.file)))

    def test_get_latlons_from_geocode(self):
        adm = ADM2.get(code="3304557", adm0="BRA")

        self.assertEqual(adm.code, "3304557")
        self.assertEqual(adm.adm0.name, ADM0.get(code="BRA").name)

    def test_load_netcdf_daily_file(self):
        self.assertTrue(type(self.dataset) is xr.core.dataset.Dataset)
        self.assertEqual(list(self.dataset.keys()), ["t2m", "tp", "d2m", "msl"])
        self.assertEqual(
            list(self.dataset.coords),
            ["longitude", "latitude", "time"],
        )


class TestCopeExtension(unittest.TestCase):
    def setUp(self) -> None:
        self.file = Path(__file__).parent / "data" / "BR_20230101.nc"
        self.dataset = DataSet.from_netcdf(str(self.file))

    def test_cope_accessor_exists(self):
        self.assertTrue(hasattr(self.dataset, "cope"))

    def test_cope_is_cope_extension(self):
        self.assertIsInstance(self.dataset.cope, CopeExtension)

    def test_adm_ds_returns_dataset(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        result = self.dataset.cope.adm_ds(adm)
        self.assertIsInstance(result, xr.Dataset)

    def test_adm_ds_contains_expected_variables(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        ds = self.dataset.cope.adm_ds(adm)
        expected_vars = [
            "temp_min",
            "temp_med",
            "temp_max",
            "umid_min",
            "umid_med",
            "umid_max",
            "precip_min",
            "precip_med",
            "precip_max",
            "precip_tot",
        ]
        for var in expected_vars:
            self.assertIn(var, ds.data_vars, f"Missing variable: {var}")

    def test_adm_ds_has_time_coordinate(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        ds = self.dataset.cope.adm_ds(adm)
        self.assertIn("time", ds.coords)

    def test_to_dataframe_returns_dataframe(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        df = self.dataset.cope.to_dataframe(adm)
        self.assertIsInstance(df, pd.DataFrame)

    def test_to_dataframe_has_expected_columns(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        df = self.dataset.cope.to_dataframe(adm)
        expected_cols = ["date", "geocode", "epiweek"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_to_dataframe_with_multiple_adms(self):
        from satellite.geo import functional

        session = functional.session().__enter__()
        codes = [
            r[0]
            for r in session.execute(
                "SELECT code FROM adm2 WHERE adm0 = 'BRA' LIMIT 2"
            ).fetchall()
        ]
        adm1 = ADM2.get(code=codes[0], adm0="BRA")
        adm2 = ADM2.get(code=codes[1], adm0="BRA")
        df = self.dataset.cope.to_dataframe([adm1, adm2])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_to_dataframe_epiweek_format(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        df = self.dataset.cope.to_dataframe(adm)
        self.assertTrue(isinstance(df["epiweek"].iloc[0], (int, np.integer)))

    def test_to_sql_creates_dataframe_and_inserts(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        mock_con = MagicMock()
        with patch("satellite.extensions.cope._adm_to_dataframe") as mock_df:
            mock_df.return_value = pd.DataFrame(
                {
                    "date": ["2023-01-01"],
                    "geocode": [3304557],
                    "epiweek": [202301],
                    "temp_med": [25.0],
                }
            )
            self.dataset.cope.to_sql(
                adms=adm,
                con=mock_con,
                tablename="test_table",
                schema="test_schema",
                verbose=False,
            )
            mock_df.assert_called_once()

    def test_to_sql_with_verbose(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        mock_con = MagicMock()
        with patch("satellite.extensions.cope._adm_to_dataframe") as mock_df:
            mock_df.return_value = pd.DataFrame(
                {
                    "date": ["2023-01-01"],
                    "geocode": [3304557],
                    "epiweek": [202301],
                    "temp_med": [25.0],
                }
            )
            self.dataset.cope.to_sql(
                adms=adm,
                con=mock_con,
                tablename="test_table",
                schema="test_schema",
                verbose=True,
            )

    def test_to_sql_without_schema(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        mock_con = MagicMock()
        with patch("satellite.extensions.cope._adm_to_dataframe") as mock_df:
            mock_df.return_value = pd.DataFrame(
                {
                    "date": ["2023-01-01"],
                    "geocode": [3304557],
                    "epiweek": [202301],
                    "temp_med": [25.0],
                }
            )
            self.dataset.cope.to_sql(
                adms=adm,
                con=mock_con,
                tablename="test_table",
                verbose=False,
            )

    def test_to_sql_multiple_adms(self):
        from satellite.geo import functional

        session = functional.session().__enter__()
        codes = [
            r[0]
            for r in session.execute(
                "SELECT code FROM adm2 WHERE adm0 = 'BRA' LIMIT 2"
            ).fetchall()
        ]
        adm1 = ADM2.get(code=codes[0], adm0="BRA")
        adm2 = ADM2.get(code=codes[1], adm0="BRA")
        mock_con = MagicMock()
        with patch("satellite.extensions.cope._adm_to_dataframe") as mock_df:
            mock_df.return_value = pd.DataFrame(
                {
                    "date": ["2023-01-01"],
                    "geocode": [3304557],
                    "epiweek": [202301],
                    "temp_med": [25.0],
                }
            )
            self.dataset.cope.to_sql(
                adms=[adm1, adm2],
                con=mock_con,
                tablename="test_table",
                verbose=False,
            )
            self.assertEqual(mock_df.call_count, 2)


class TestConvertUnits(unittest.TestCase):
    def setUp(self) -> None:
        self.file = Path(__file__).parent / "data" / "BR_20230101.nc"
        self.dataset = DataSet.from_netcdf(str(self.file))

    def test_temperature_converted_to_celsius(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        ds = self.dataset.cope.adm_ds(adm)
        for var in ["temp_min", "temp_med", "temp_max"]:
            if var in ds.data_vars:
                self.assertTrue(
                    all(ds[var].values < 100),
                    f"{var} should be in reasonable Celsius range",
                )

    def test_precipitation_converted_to_mm(self):
        adm = ADM2.get(code="3304557", adm0="BRA")
        ds = self.dataset.cope.adm_ds(adm)
        for var in ["precip_min", "precip_med", "precip_max", "precip_tot"]:
            if var in ds.data_vars:
                self.assertTrue(
                    all(ds[var].values >= 0), f"{var} should be non-negative"
                )


if __name__ == "__main__":
    unittest.main()
