import csv
import json
import argparse

#CSVFILE = "../Africa_Soil_Pts.csv"
#URL = "https://data.mint.isi.edu/files/soil/horn_of_africa"

def print_resources_json(csvfile, url):
    resources = []
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # Skip header
        for row in csv_reader:
            resource = {
                "name": row[2],
                "resource_type": "CSV",
                "data_url": url +"/" + row[2],
                "metadata" : {
                    "spatial_coverage": {"type":"Point","value":{"x":str(row[3]),"y":str(row[4])}},
                    "temporal_coverage": {"start_time": "1850-01-01T00:00:00", "end_time": "2050-01-01T00:00:00"}
                }
            }
            resources.append(resource)
    print(json.dumps(resources, indent=3))


parser = argparse.ArgumentParser(description='Create soil resource json')
parser.add_argument('FILE',  help='soil csv file')
parser.add_argument('DATA_URL', help='url of the folder where soil files are kept')

args = parser.parse_args()
print_resources_json(args.FILE, args.DATA_URL)