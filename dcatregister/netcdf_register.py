import requests
import logging
import json
import argparse
import xarray as xr
from utils import get_svo_sparql
from netcdf import get_svo, get_spatial_info, get_temporal_info

global DCAT, PROVID

PROVID = None #"9ef60317-5da5-4050-8bbc-7d6826fee49f"
DATACATALOG_URL = 'https://datacatalog.dev.mint.isi.edu/'
REGISTER_DATA = "/datasets/register_datasets"
FIND_DATASET = "/datasets/find"
FIND_STDVARS = "/knowledge_graph/find_standard_variables"
REGISTER_STDVARS = "/knowledge_graph/register_standard_variables"
REGISTER_DSVARS = "/datasets/register_variables"
REGISTER_RESOURCES = "/datasets/register_resources"
RESOURCE_CHUNK_SIZE = 500
SYNC_DSMETA = "/datasets/sync_datasets_metadata"
PROVENANCE_URL = "/provenance/register_provenance"

def open_dataset(file_name: str):
    """Open a Netcdf 

    Args:
        file_name (str): [description]

    Returns:
        [type]: [description]
    """
    data=xr.open_dataset(file_name)
    return data

def submit_request(url, json):
    try:
        r = requests.post(DATACATALOG_URL + url, json=json)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(r.json())
        logging.error("Error request", exc_info=True)
        exit(1)
    if r.status_code == 200:
        result = r.json()
        if result["result"] == "success":
            return result
    return None

def create_standard_variables(stdvars):
    if stdvars is not None and len(stdvars) > 0:
        std_var_ids = []

        find_existing_json = { "name__in": stdvars }
        find_result = submit_request(FIND_STDVARS, find_existing_json)
        #print('find result : ',find_result)

        cur_stdvars = {}
        if find_result is not None and len(find_result["standard_variables"]) > 0:
            for stdvar in find_result["standard_variables"]:
                cur_stdvars[stdvar["name"]] = stdvar
                std_var_ids.append(stdvar['id'])
        print('cur_stdvars : ', cur_stdvars)
        print('std_var_ids : ', std_var_ids)

        new_stdvars = []
        for stdvar in stdvars:
            if stdvar not in cur_stdvars:
                new_stdvars.append(stdvar)
        
        if len(new_stdvars) > 0:
            standard_variables = []
            for name in new_stdvars:
                std_var = {
                    "name": name,
                    "ontology": "MyOntology",  # where do I get this? => use dummy data for now
                    "uri": "http://my_ontology_uri.org/standard_names/" + name
                }
                standard_variables.append(std_var)
            register_json = { "standard_variables" : standard_variables }
            register_result = submit_request(REGISTER_STDVARS, register_json)
            print('register_result : ', register_result["standard_variables"])

            if register_result is not None and len(register_result["standard_variables"]) > 0:
                for stdvar in register_result["standard_variables"]:
                    std_var_ids.append(stdvar["record_id"])
                    cur_stdvars[stdvar["name"]] = stdvar        
        return  std_var_ids

def register_dataset(dataset_id, provenance_id, description):
    find_existing_json = { "dataset_ids__in": [dataset_id] }
    find_result = submit_request(FIND_DATASET, find_existing_json)
    print('find dataset result : ', find_result)
    if find_result is not None and len(find_result["datasets"]) > 0:
        # Get dataset id
        # ???
        pass
    else:
        # Register dataset
        print("Registering dataset")
        dsid = create_dataset(dataset_id, provenance_id, description)

        # print("Registering Variables")
        # # Register standard variables
        # if "standard_variables" in details:
        #     dsvars = create_standard_variables(details["variables"])
        #     create_dataset_variables(dsid, dsvars)

def create_dataset(dataset_id, provenance_id, description):
    json = {
        "datasets": [
            {
            "record_id": dataset_id,
            "provenance_id": provenance_id, #? where will i get this from? => ip parameter
            "name": "temp name",                # where will i get this from? => ip parameter
            "description": description,
            #"metadata": details["metadata"]             #where will i get this from? => not required
            }
        ]
    }
    result = submit_request(REGISTER_DATA, json)
    print('Result : ', result)
    if result is None or len(result["datasets"]) == 0:
        return None
    
    dsid = result["datasets"][0]["record_id"]    
    return dsid                                         # what should i return?

def create_dataset_variables(dsid, variables, std_var_ids):
    if dsid is not None and variables is not None and len(variables) > 0:
        dsvars = []
        for dsvar in variables:
            print('dsvar : ', dsvar)
            temp = {}
            temp["dataset_id"] = dsid
            temp["name"] = dsvar["long_name"]
            temp["metadata"] = {
                "units" : dsvar["units"]
            }
            temp["standard_variable_ids"] = std_var_ids
            dsvars.append(temp)
        register_json = { "variables": dsvars }
        register_result = (REGISTER_DSVARS, register_json)
        if register_result is not None:
            return register_result[1]["variables"]

def main():
    global DCAT, PROVID
    
    parser = argparse.ArgumentParser(description='Register a dataset')
    #parser.add_argument('FILE',  help='dataset details file')
    parser.add_argument('DATASET_ID', help='dataset id', default="")
    #parser.add_argument('PROVENANCE_ID', help='provenance id of the user', default="9ef60317-5da5-4050-8bbc-7d6826fee49f")

    args = parser.parse_args()
    dataset_id = args.DATASET_ID
    PATH = '../../Topoflow_Galana/Test1_2D-Q_1.nc'
    data = open_dataset(PATH)
    #print(data.metadata)
    var = data.variables
    print(var) # => register all variables which are not latitude, longitude and time
    n = len(var)
    sql_query_url = 'https://endpoint.mint.isi.edu/modelCatalog-1.8.0/query' #for getting uri and ontology information
    register_std_variables = []
    variables = []
    
    svo_names = get_svo(data)
    for svo in svo_names:
        svo_data = get_svo_sparql(v.attrs['svo_name'], sql_query_url)
        if len(svo_data) > 0:
            print('svo_data : ', svo_data)
        else:
            register_std_variables.append(v.attrs['svo_name'])

    std_var_ids = create_standard_variables(register_std_variables)
    
    #provenance_id = args.PROVENANCE_ID
    description = data.title
    register_dataset(dataset_id, '9ef60317-5da5-4050-8bbc-7d6826fee49f', description)

    dataset_vars = create_dataset_variables(dataset_id, variables, std_var_ids)

    #create_provenance_id(PROVID)
    # with open(args.FILE, "r") as details_file:
    #     details = json.load(details_file)
    #     register_dataset(details)
    #     sync_datasets_metadata()


if __name__=="__main__":
    main()
