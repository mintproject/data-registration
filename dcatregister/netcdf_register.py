import argparse
import os
import json
import logging
from dcatregister.api import Datacatalog
from dcatregister.netcdf import get_spatial_info, get_svo, get_temporal_info, open_dataset
from dcatregister.utils import create_variable_metadata, get_svo_sparql


def create_dataset_file_content(name, description, temporal_coverage, data_type, directory):
    return {
        "name": name,
        "description": description,
        "metadata": {
            "temporal_coverage": temporal_coverage,
            "datatype": data_type,
        },
        "resources": os.path.join(directory,"resources.json"),
        "variables": os.path.join(directory,"variables.json")
    }


def main():
    parser = argparse.ArgumentParser(description='Register a dataset')
    parser.add_argument('files',
                        metavar='files',
                        type=str,
                        nargs='+',
                        help='dataset details file'
                        )
    parser.add_argument('--dataset_id',
                        help='The dataset name',
                        required=True
                        )
    parser.add_argument('--dataset_name',
                        help='The dataset name',
                        required=True
                        )
    parser.add_argument('--dataset_description',
                        help='Dataset description',
                        required=True
                        )
    parser.add_argument('-p',
                        '--provenance_id',
                        help='provenance id of the user',
                        required=False,
                        default="9ef60317-5da5-4050-8bbc-7d6826fee49f",
                        )

    parser.add_argument(
        '--url',
        help='The datacatalog url',
        required=False,
        default="https://datacatalog.dev.mint.isi.edu/",
    )

    # Parse argprovenance_id, datacatalog_url
    args = parser.parse_args()
    files = args.files
    dataset_id = args.dataset_id
    dataset_description = args.dataset_description
    dataset_name = args.dataset_name
    provenance_id = args.provenance_id
    datacatalog_url = args.url


    dataset_directory = os.path.join(os.getcwd(), dataset_id)
    dataset_parent_file = os.path.join(dataset_directory, "dataset.json")

    datacatalog = Datacatalog(datacatalog_url, provenance_id)

    # Create directories and files

    if not os.path.exists(dataset_directory):
        os.mkdir(dataset_directory)
    resource_file_path = os.path.join(dataset_directory, 'resources.json')
    dataset_file_path = os.path.join(dataset_directory, 'dataset.json')
    variables_file_path = os.path.join(dataset_directory, 'variables.json')
    try:
        resource_file = open(resource_file_path, 'w', encoding='utf8')
        dataset_file = open(dataset_file_path, 'w', encoding='utf8')
        variable_file = open(variables_file_path, 'w', encoding='utf8')
    except TypeError as error:
        logging.error(error)
        exit(1)
    # Store the variables and resources
    variables = []
    resources = []
    dataset_temporal_coverage = {'start_time': None, 'end_time': None}

    # Loop the files
    for _f in files:
        data = open_dataset(_f)
        try:
            name = data.attrs['title']
        except:
            name = os.path.basename(_f)
        variables = extract_variables_netcdf(data)
        resource = extract_resource_netcdf(name, data)
        start_time = resource['metadata']['temporal_coverage']['start_time']
        end_time = resource['metadata']['temporal_coverage']['end_time']
        if not dataset_temporal_coverage['start_time'] or start_time < dataset_temporal_coverage['start_time']:
            dataset_temporal_coverage['start_time'] = start_time
        if not dataset_temporal_coverage['end_time'] or end_time > dataset_temporal_coverage['end_time']:
            dataset_temporal_coverage['end_time'] = end_time
        resources.append(resource)

    # Write the JSON definition files
    dataset = create_dataset_file_content(
        dataset_name, dataset_description, dataset_temporal_coverage, '', dataset_directory)
    print(dataset)
    variable_file.write(json.dumps(variables, indent=4))
    resource_file.write(json.dumps(resources, indent=4))
    dataset_file.write(json.dumps(dataset, indent=4))
    variable_file.close()
    resource_file.close()
    dataset_file.close()
    datacatalog.create_provenance_id(provenance_id)
    print(dataset_parent_file)
    with open(dataset_parent_file) as details_file:
        details = json.load(details_file)
        datacatalog.register_dataset(details)
        datacatalog.sync_datasets_metadata()


def extract_resource_netcdf(name, data):
    resource = {
        'name': name,
        "resource_type": "CSV",
        "data_url": "http://",
        "metadata": {
            "temporal_coverage": get_temporal_info(data),
            "spatial_coverage": get_spatial_info(data)
        }
    }
    return resource


def extract_variables_netcdf(data):
    variables = []
    svo_names = get_svo(data)
    for svo_name in svo_names:
        svo_data = get_svo_sparql(svo_name)
        variable = create_variable_metadata(
            name=svo_data['metadata_label'],
            metadata_label=svo_data['metadata_label'],
            metadata_unit=svo_data['metadata_unit'],
            svo_name=svo_data['svo_name'],
            svo_description=svo_data['svo_description'],
            svo_uri=svo_data['svo_uri']
        )
        variables.append(variable)
    return variables


if __name__ == "__main__":
    main()
