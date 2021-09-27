from dcatregister.utils import get_svo_sparql
from dcatregister.netcdf import get_spatial_info, open_dataset, get_temporal_info, get_svo
from pathlib import Path

RESOURCES = "resources"
resource_dir = Path(__file__).parent / RESOURCES


def test_open():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    assert data


def test_temporal_info():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    temporal_info = get_temporal_info(data)
    temporal_info_excepted = {
        'start_time': '2017-01-01T00:00:00', 'end_time': '2017-01-31T22:00:00'}
    assert temporal_info == temporal_info_excepted


def test_spatial_info():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    geo_spatial = get_spatial_info(data)
    geo_spatial_expected = {
        "type": "BoundingBox",
        "value": {
            "xmax": 36.4,
            "xmin": -3.143333333333,
            "ymax": 40.766666666667,
            "ymin": 0.69
        }
    }
    assert geo_spatial == geo_spatial_expected


def test_get_variables():
    data = open_dataset(resource_dir / "Test1_2D-d.nc")
    svo = get_svo(data)
    assert svo == ['max_channel_flow_depth']
