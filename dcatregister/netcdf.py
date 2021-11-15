import xarray as xr
import datetime

VARIABLES_EXCLUDED = ['time', 'datetime', 'latitude', 'longitude']

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
    spatial_dict = dict()
    if len(data.geospatial_bounds) > 0:
        spatial_data = data.geospatial_bounds
        spatial_dict['type'] = 'BoundingBox'
        xmax, xmin, ymax, ymin = [float(x) for x in spatial_data]
        spatial_dict['value'] = {
            'xmax': xmax,
            'xmin': xmin,
            'ymax': ymax,
            'ymin': ymin
        }
    return spatial_dict

def get_temporal_info(data):
    t = dict()
    if len(data.datetime) > 0 and len(data.datetime.data) > 0:
        date_s = str(data.datetime[0].data)
        date_e = str(data.datetime[-1].data)
        date_start = datetime.datetime.strptime(date_s, "%Y-%m-%d %H:%M:%S")
        date_end = datetime.datetime.strptime(date_e, "%Y-%m-%d %H:%M:%S")
        t['start_time'] = date_start.isoformat()
        t['end_time'] = date_end.isoformat()
    return t

def get_svo(data: dict):
    """Get svo from a Netcdf xrray dataset

    Args:
        data (dict): The xarray data
    """
    svo = []
    for name, variable  in data.variables.items():
        attr = variable.attrs
        if attr['long_name'] not in VARIABLES_EXCLUDED:
            svo.append(attr['long_name'])
    return svo
            
if __name__ == '__main__':
    PATH = '../../Topoflow_Galana/Test1_2D-Q_1.nc'
    data = open_dataset(PATH)
    spatial = get_spatial_info(data)
    temporal = get_temporal_info(data)