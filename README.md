Examples
========

First create soil resources
  * cd ./example/soil
  * python ./create_soil_resources_json.py ./Africa_Soil_Pts.csv "https://data.mint.isi.edu/files/soil/horn_of_africa" > resources.json

Then register the dataset
  * python ../../register_dataset.py ./dataset_details.json "http://localhost:7000" "9ef60317-5da5-4050-8bbc-7d6826fee49f"

