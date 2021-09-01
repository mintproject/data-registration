from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template

def get_svo_sparql(svo_name: str, sparql_endpoint="https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query": str) -> dict:
    """Get the svo's dara required to register a DataCatalog resource

    Args:
        svo_name (str): The name of SVO. For example: land_surface_water__depth
        sparql_endpoint (str): The enpdoint https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query

    Raises:
        ValueError: Error when the query is wrong

    Returns:
        dict: Contains five attributes: metadata_label, metadata_unit, svo_unit, svo_description, svo_name
    """
    query_string = Template("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sd: <https://w3id.org/okn/o/sd#>
    SELECT ?metadata_label ?metadata_unit  ?svo_uri ?svo_description ?metadata_unit WHERE {
    GRAPH <http://endpoint.mint.isi.edu/modelCatalog-1.8.0/data/mint@isi.edu> {        
        ?svo_uri rdfs:label "$svo_name" ;
                sd:description ?svo_description .
        ?variable sd:hasStandardVariable ?svo_uri ;
                sd:description ?metadata_label ;
                sd:usesUnit ?metadata_unit_uri .
        ?metadata_unit_uri rdfs:label ?metadata_unit
    }
    }
    LIMIT 1
    """).safe_substitute(svo_name=svo_name)
    
    sparql = SPARQLWrapper(sparql_endpoint)

    sparql.setQuery(query_string)

    try :
        results = sparql.query()
    except :
        raise ValueError("Not found")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if 'results' in results and 'bindings' in results['results'] and len(results['results']['bindings']) > 0:
        new_var = results['results']['bindings'][0]
    else:
        return {}
    return {
        'metadata_label': new_var['metadata_label']['value'],
        'metadata_unit': new_var['metadata_unit']['value'],
        'svo_uri': new_var['metadata_label']['value'],
        'svo_description': new_var['metadata_label']['value'],
        'svo_name': svo_name
    }
