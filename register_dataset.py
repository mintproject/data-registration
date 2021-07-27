import requests
import logging
import json
import argparse

global DCAT, PROVID

PROVID = None #"9ef60317-5da5-4050-8bbc-7d6826fee49f"
DCAT = None #"http://localhost:7000"

REGISTER_DATA = "/datasets/register_datasets"
FIND_STDVARS = "/knowledge_graph/find_standard_variables"
REGISTER_STDVARS = "/knowledge_graph/register_standard_variables"
REGISTER_DSVARS = "/datasets/register_variables"
REGISTER_RESOURCES = "/datasets/register_resources"
RESOURCE_CHUNK_SIZE = 500
SYNC_DSMETA = "/datasets/sync_datasets_metadata"
PROVENANCE_URL = "/provenance/register_provenance"

def register_dataset(details):
    dsid = None
    # If a dataset id is present
    # - Don't create a new dataset with new variables
    if "id" in details:
        # Get dataset id
        dsid = details["id"]
    else:
        # Register dataset
        print("Registering dataset")
        dsid = create_dataset(details)

        print("Registering Variables")
        # Register standard variables
        if "standard_variables" in details:
            dsvars = create_standard_variables(details["variables"])
            create_dataset_variables(dsid, dsvars)

    print("Registering Resources")
    # Register resources
    resources = get_resources_json(details["resources"])
    if resources is not None and len(resources) > 0:
        create_resources(dsid, resources)


def sync_datasets_metadata():
    r = requests.post(DCAT + SYNC_DSMETA, headers={"Connection":"keep-alive"})


def create_dataset(details):
    # TODO: check for existing dataset with same name ?
    json = {
        "datasets": [
            {
            "provenance_id": PROVID,
            "name": details["name"],
            "description": details["description"],
            "metadata": details["metadata"]
            }
        ]
    }
    result = submit_request(REGISTER_DATA, json)
    if result is None or len(result["datasets"]) == 0:
        return None
    
    dsid = result["datasets"][0]["record_id"]
    return dsid


# - Find Standard Variables if they exist
# - Otherwise create Standard Variables for the ones that don't
#   - Get standard variable ids
def create_standard_variables(dsvars):
    if dsvars is not None and len(dsvars) > 0:
        stdvars = []
        for dsvar in dsvars:
            stdvars.extend(dsvar['standard_variables']) 
       
        find_existing_json = { "name__in": list(map(lambda var: var["name"], stdvars)) }
        find_result = submit_request(FIND_STDVARS, find_existing_json)

        cur_stdvars = {}
        if find_result is not None and len(find_result["standard_variables"]) > 0:
            for stdvar in find_result["standard_variables"]:
                cur_stdvars[stdvar["name"]] = stdvar

        new_stdvars = []
        for stdvar in stdvars:
            if stdvar["name"] not in cur_stdvars:
                new_stdvars.append(stdvar)
        
        if len(new_stdvars) > 0:
            register_json = { "standard_variables" : new_stdvars }
            register_result = submit_request(REGISTER_STDVARS, register_json)
            if register_result is not None and len(register_result["standard_variables"]) > 0:
                for stdvar in register_result["standard_variables"]:
                    stdvar["id"] = stdvar["record_id"]
                    cur_stdvars[stdvar["name"]] = stdvar        
        
        new_dsvars = []
        for dsvar in dsvars:
            new_dsvar = {
                "name": dsvar["name"],
                "metadata": dsvar["metadata"],
                "standard_variable_ids": []
            }
            for stdvar in dsvar["standard_variables"]:
                stdvarname = stdvar["name"]
                if stdvarname in cur_stdvars:
                    new_dsvar["standard_variable_ids"].append(cur_stdvars[stdvarname])
            
            new_dsvars.append(new_dsvar)

        return new_dsvars


# - Create dataset variables
#   - name, [standard_variable_ids], dataset_id
def create_dataset_variables(dsid, dsvars):
    if dsid is not None and dsvars is not None and len(dsvars) > 0:
        for dsvar in dsvars:
            dsvar["dataset_id"] = dsid
        register_json = { "variables": dsvars }
        register_result = (REGISTER_DSVARS, register_json)
        if register_result is not None:
            return register_result["variables"]


# Add resources to dataset
# - Add provenance and dataset id to the resources
# - Register resources upto RESOURCE_CHUNK_SIZE in one go
def create_resources(dsid, resources):
    if dsid is not None and resources is not None and len(resources) > 0:
        resource_chunks = divide_chunks(resources, RESOURCE_CHUNK_SIZE)
        chunkid = 1;
        for chunk in resource_chunks:
            print(f"Registering resource chunk {chunkid}")
            chunkid += 1
            chunklist = list(chunk)
            for resource in chunklist:
                resource["provenance_id"] = PROVID
                resource["dataset_id"] = dsid
            register_json = { "resources": chunklist }
            submit_request(REGISTER_RESOURCES, register_json)


# Fetch resources from json
# - If resources is a string, read from file, otherwise read resources list
def get_resources_json(resources):
    if isinstance(resources, list):
        return resources
    if isinstance(resources, str):
        with open(resources, "r") as infile:
            return json.load(infile)


# Fetch variables from json
# - If variables is a string, read from file, otherwise read variables list
def get_variables_json(variables):
    if isinstance(variables, list):
        return variables
    if isinstance(variables, str):
        with open(variables, "r") as infile:
            return json.load(infile)

# Helper function to submit a request to the data catalog
def submit_request(url, json):
    try:
        r = requests.post(DCAT + url, json=json)
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


# Yield successive n-sized chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


def create_provenance_id(provenance_id):
    provenance_definition = {
        "provenance": {
            "provenance_type": "user",
            "record_id": provenance_id,
            "name": "test_api_outside",
            "metadata": {"contact_information": {"email": "email@example.com"}}
        }
    }
    try:
        r = requests.post(f"""{DCAT}{PROVENANCE_URL}""", json=provenance_definition)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(r.json())
        logging.error("Error request", exc_info=True)
        exit(1)

def main():
    global DCAT, PROVID
    
    parser = argparse.ArgumentParser(description='Register a dataset')
    parser.add_argument('FILE',  help='dataset details file')
    parser.add_argument('DATA_CATALOG_URL', help='data catalog url', default="https://data-catalog.mint.isi.edu")
    parser.add_argument('PROVENANCE_ID', help='provenance id of the user', default="9ef60317-5da5-4050-8bbc-7d6826fee49f")

    args = parser.parse_args()
    DCAT = args.DATA_CATALOG_URL
    PROVID = args.PROVENANCE_ID

    create_provenance_id(PROVID)
    with open(args.FILE, "r") as details_file:
        details = json.load(details_file)
        register_dataset(details)
        sync_datasets_metadata()


if __name__=="__main__":
    main()
