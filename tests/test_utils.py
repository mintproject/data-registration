from dcatregister.utils import get_svo_sparql


def test_get_svo_from_netcdf():
    svo_name = "land_surface_water__depth"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_sparql(svo_name, sparql_server)
    assert data == {'metadata_label': 'Surface Water', 'metadata_unit': 'm', 'svo_uri': 'Surface Water', 'svo_description': 'Surface Water', 'svo_name': 'land_surface_water__depth'}

def test_get_svo_from_netcdf_not_found():
    svo_name = "land_surface_water__depth_WRONG"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_sparql(svo_name, sparql_server)
    assert data == {}
  