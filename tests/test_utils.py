from dcatregister.utils import get_svo_from_netcdf


def test_get_svo_from_netcdf():
    svo_name = "land_surface_water__depth"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_from_netcdf(svo_name, sparql_server)
    print(data)


def test_get_svo_from_netcdf_not_found():
    svo_name = "land_surface_water__depth_WRONG"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_from_netcdf(svo_name, sparql_server)
    assert data == {}
  