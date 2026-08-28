import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from satellite.models import ERA5LandRequest
from satellite.request import reanalysis_era5_land


def _fixture() -> Path:
    return Path(__file__).parent / "data" / "BR_20230101.nc"


class TestRemoveFiles(unittest.TestCase):
    def _run_fake(self, tmp: str, variable: list[str], remove_files: bool = False):
        main = Path(tmp) / "chunk_20230101.nc"
        tp = Path(tmp) / "chunk_20230101_tp.nc"
        shutil.copy(_fixture(), main)
        shutil.copy(_fixture(), tp)
        fake_download = MagicMock(side_effect=[str(main), str(tp)])
        with patch.object(ERA5LandRequest, "download", fake_download):
            ds = reanalysis_era5_land(
                "chunk_20230101",
                date="2023-01-01",
                variable=variable,
                locale="BRA",
                remove_files=remove_files,
            )
        return ds, main, tp

    def test_remove_files_with_precip(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds, main, tp = self._run_fake(
                tmp, ["2m_temperature", "total_precipitation"], remove_files=True
            )
            self.assertGreater(ds.sizes["time"], 0)
            self.assertFalse(main.exists(), "main file should be removed")
            self.assertFalse(tp.exists(), "next-day tp file should be removed")

    def test_remove_files_without_precip(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds, main, _tp = self._run_fake(tmp, ["2m_temperature"], remove_files=True)
            self.assertGreater(ds.sizes["time"], 0)
            self.assertFalse(main.exists(), "main file should be removed")

    def test_keep_files_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds, main, tp = self._run_fake(
                tmp, ["2m_temperature", "total_precipitation"]
            )
            self.assertGreater(ds.sizes["time"], 0)
            self.assertTrue(main.exists(), "main file should be kept")
            self.assertTrue(tp.exists(), "next-day tp file should be kept")


if __name__ == "__main__":
    unittest.main()
