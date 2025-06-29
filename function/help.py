import numpy as np
import pandas as pd

def geo_to_local(lat, lon, ref_lat, ref_lon, M_PER_DEG):
    """
    将经纬度坐标 (lat, lon) 转换为以 ref_lat/ref_lon 为中心的局部平面坐标 (x, y)，单位：米。
    参数：
    - lat, lon: 原始经纬度坐标（可以是标量或数组）
    - ref_lat, ref_lon: 参考中心坐标
    返回：
    - x, y: 转换后的坐标（米）
    """
    lat = np.array(lat)
    lon = np.array(lon)
    x = (lon - ref_lon) * M_PER_DEG * np.cos(np.radians(ref_lat))
    y = (lat - ref_lat) * M_PER_DEG
    return x, y

def moving_average(x, w):
    return np.convolve(x, np.ones(w)/w, mode='valid')
