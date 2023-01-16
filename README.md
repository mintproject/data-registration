Examples
========

This repository contains scripts to create a dataset, resources and variables.

```bash
$ python register_dataset.py -h
usage: register_dataset.py [-h] FILE DATA_CATALOG_URL PROVENANCE_ID

Register a dataset

positional arguments:
  FILE              dataset details file
  DATA_CATALOG_URL  data catalog url
  PROVENANCE_ID     provenance id of the user

optional arguments:
  -h, --help        show this help message and exit
```

## How to use it?

You must create 3 files:

- dataset: the set (dataset) where the resources are stored
- resources: The resources of the dataset
- variables: The variables required to describe the resources.

We provide a example a [small example](./example/small_soil/)

### Registering

You must set up the server and provenance id.

- Datacatalog server: For testing purposes, we recommend to use the *dev catalog server*.
- Provenance id: For testing purposes, we recommend to use the id: `9ef60317-5da5-4050-8bbc-7d6826fee49f`

```bash
DATA_CATALOG_URL="https://data-catalog.dev.mint.isi.edu"
PROVENANCE_ID="9ef60317-5da5-4050-8bbc-7d6826fee49f"
cd example/small_soil
python ../../register_dataset.py ./dataset.json ${DATA_CATALOG_URL} ${PROVENANCE_ID}
```

