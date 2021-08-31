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


if __name__ == '__main__':
    PATH = '../../Topoflow_Galana/Test1_2D-d.nc'
    data = open_dataset(PATH)
    print(data)
    # spatial = get_spatial_info(data)
    # temporal = get_temporal_info(data)