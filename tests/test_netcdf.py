from utils.netcdf import get_spatial_info, open
from pathlib import Path

RESOURCES = "resources"
resource_dir = Path(__file__).parent / RESOURCES

def test_open():
    data = open(resource_dir / "Test1_2D-d")
    assert data


def test_spatial_info():
    data = open(resource_dir / "Test1_2D-d")
    geo_spatial = get_spatial_info(data)
    geo_spatial_expected = {"type":"BoundingBox","value":{"xmax":"36.4","xmin":"-3.14333333","ymax":"40.76666667","ymin":"0.69"}}
    assert geo_spatial == geo_spatial_expected