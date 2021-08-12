from xarray.backends.api import open_dataset
from dcatregister.netcdf import get_spatial_info, open_dataset
from pathlib import Path

RESOURCES = "resources"
resource_dir = Path(__file__).parent / RESOURCES

def test_open():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    assert data


def test_spatial_info():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    geo_spatial = get_spatial_info(data)
    geo_spatial_expected = {
        "type":"BoundingBox",
        "value":{
            "xmax":"36.4",
            "xmin":"-3.143333333333",
            "ymax":"40.76666667766666666667",
            "ymin":"0.69"
            }
        }
    assert geo_spatial == geo_spatial_expected