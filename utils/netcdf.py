import xarray as xr

def open(file_name: str):
    """Open a Netcdf 

    Args:
        file_name (str): [description]

    Returns:
        [type]: [description]
    """
    data=xr.open_dataset(file_name)
    return data

def get_spatial_info(data):
    #  Example output  {"type":"BoundingBox","value":{"xmax":"59.875","xmin":"10.125","ymax":"29.875","ymin":"-14.875"}}
    spatial_data = data.geospatial_bounds
    spatial_dict = dict()
    spatial_dict['type'] = 'BoundingBox'
    xmax, xmin, ymax, ymin = [float(x) for x in spatial_data]
    spatial_dict['value'] = {
        'xmax': xmax,
        'xmin': xmin,
        'ymax': ymax,
        'ymin': ymin
    }
    print(spatial_dict)
    return spatial_dict

def get_temporal_info(data):
    return


if __name__ == '__main__':
    PATH = '../../Topoflow_Galana/Test1_2D-Q_1.nc'
    data = open(PATH)
    print(data)
    spatial = get_spatial_info(data)
    get_temporal_info(data)