import xarray as xr
import datetime

def open_dataset(file_name: str):
    """Open a Netcdf 

    Args:
        file_name (str): [description]

    Returns:
        [type]: [description]
    """
    data=xr.open_dataset(file_name)
    return data

def get_spatial_info(data):
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
    t = dict()
    date_s = str(data.datetime[0]).split('\'')
    date_e = str(data.datetime[-1]).split('\'')
    date_start = datetime.datetime.strptime(date_s[3], "%Y-%m-%d %H:%M:%S")
    date_end = datetime.datetime.strptime(date_e[3], "%Y-%m-%d %H:%M:%S")
    t['start_time'] = date_start.isoformat()
    t['end_time'] = date_end.isoformat()
    return t


if __name__ == '__main__':
    PATH = '../../Topoflow_Galana/Test1_2D-Q_1.nc'
    data = open_dataset(PATH)
    print(data)
    spatial = get_spatial_info(data)
    temporal = get_temporal_info(data)
    print(temporal)