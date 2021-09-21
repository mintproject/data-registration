from dcatregister.utils import create_variable_metadata, get_svo_sparql


def test_get_svo_from_netcdf():
    svo_name = "land_surface_water__depth"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_sparql(svo_name, sparql_server)
    data_expected = {
        'metadata_label': 'Surface Water',
        'metadata_unit': 'm',
        'svo_uri': 'https://w3id.org/okn/i/mint/LAND_SURFACE_WATER__DEPTH',
        'svo_description': '                    land_surface_water__depth\n                        \nThis variable has the recorded  phenomenon:water(land_surface)@context~on_water\nThis variable has the recorded  matter water\nThis variable has the recorded context phenomenon land_surface\nThis variable has the recorded context body land\nThis variable has the recorded context abstraction surface\nThis variable has the recorded units L.\nThis variable has the recorded property depth                                                ', 
        'svo_name': 'land_surface_water__depth'
    }
    assert data == data_expected

def test_get_svo_from_netcdf_not_found():
    svo_name = "land_surface_water__depth_WRONG"
    sparql_server = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query'
    data = get_svo_sparql(svo_name, sparql_server)
    assert data == {}
  
def test_create_entry_datacatalog_variable():
    svo_name = "land_surface_water__depth"
    data = {
        'metadata_label': 'Surface Water',
        'metadata_unit': 'm',
        'svo_uri': 'https://w3id.org/okn/i/mint/LAND_SURFACE_WATER__DEPTH',
        'svo_description': '                    land_surface_water__depth\n                        \nThis variable has the recorded  phenomenon:water(land_surface)@context~on_water\nThis variable has the recorded  matter water\nThis variable has the recorded context phenomenon land_surface\nThis variable has the recorded context body land\nThis variable has the recorded context abstraction surface\nThis variable has the recorded units L.\nThis variable has the recorded property depth                                                ', 
        'svo_name': 'land_surface_water__depth'
    }
    test_name = "Topoflow example 2 dimensional from ethiopia"
    create_variable_metadata(
        name=test_name,
        metadata_label=data['metadata_label'],
        metadata_unit=data['metadata_unit'],
        svo_name=data['svo_name'],
        svo_description=data['svo_description'],
        svo_uri=data['svo_uri']
    )


def test_create_entry_datacatalog_variable_without_info():
    """Testing the case where the model catalog does not have information about the variable
    """
    svo_name = "land_surface_water__depth"
    data = {
    }
    test_name = "Topoflow example 2 dimensional from ethiopia"
    create_variable_metadata(
        name=test_name,
        svo_name=svo_name,
    )