import xarray as xr
import pandas as pd

def readable_time(time_ns):
    _, hours, minutes, seconds, *__ = pd.to_timedelta(time_ns).components
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def get_data(file_path):
    return xr.open_dataset(file_path, )

def windspeed_round(windspeed):
    return round(windspeed, 4)


    


