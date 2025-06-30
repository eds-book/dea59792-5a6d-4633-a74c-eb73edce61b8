import numpy as np
import pandas as pd

def geo_to_local(lat, lon, ref_lat, ref_lon, M_PER_DEG):
    """
    Convert latitude and longitude coordinates (lat, lon) to local plane coordinates (x, y) centred on ref_lat/ref_lon, in metres.  
    Parameters:
    - lat, lon: Original latitude and longitude coordinates (can be scalars or arrays)
    - ref_lat, ref_lon: Reference centre coordinates
    Returns:
    - x, y: Converted coordinates (metres)
    """
    lat = np.array(lat)
    lon = np.array(lon)
    x = (lon - ref_lon) * M_PER_DEG * np.cos(np.radians(ref_lat))
    y = (lat - ref_lat) * M_PER_DEG
    return x, y

def moving_average(x, w):
    return np.convolve(x, np.ones(w)/w, mode='valid')
