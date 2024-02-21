# ***************************************************************
# Copyright (c) 2024 shinetek. All Rights Reserved.
# modifier:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2024.2
# ***************************************************************
from decimal import Decimal
import numpy as np


def get_submap_box(file_read, in_data, box, res):
    try:
        data_max_lat = file_read.attrs['Maximum Latitude']
        data_min_lat = file_read.attrs['Minimum Latitude']
        data_max_lon = file_read.attrs['Maximum Longitude']
        data_min_lon = file_read.attrs['Minimum Longitude']
        if type(data_max_lat) == np.ndarray:
            data_max_lat = file_read.attrs['Maximum Latitude'][0]
            data_min_lat = file_read.attrs['Minimum Latitude'][0]
            data_max_lon = file_read.attrs['Maximum Longitude'][0]
            data_min_lon = file_read.attrs['Minimum Longitude'][0]
    except Exception as ep:
        data_max_lat = 90
        data_min_lat = -90
        data_max_lon = 180
        data_min_lon = -180
    tar_top_lat = Decimal(str(box[3]))  # 左上角点纬度
    tar_btm_lon = Decimal(str(box[1]))  # 右下角点经度
    tar_btm_lat = Decimal(str(box[2]))  # 右下焦点纬度
    tar_top_lon = Decimal(str(box[0]))  # 左上角点经度
    res = Decimal(str(float(res)))
    # 计算最小交集box
    in_top_lon, in_top_lat, in_btm_lon, in_btm_lat = min_box(
        [tar_top_lat, tar_btm_lon, tar_btm_lat, tar_top_lon], [Decimal(str(data_max_lat)), Decimal(str(data_max_lon)), Decimal(str(data_min_lat)), Decimal(str(data_min_lon))])
    # 换算成i j
    min_i = int(round(Decimal(str(in_top_lon - Decimal(str(data_min_lon)))) / res))
    min_j = int(round(Decimal(str(Decimal(str(data_max_lat)) - in_top_lat)) / res))
    width = int(round(Decimal(str(in_btm_lon - in_top_lon)) / res + Decimal(0.6)))
    height = int(round(Decimal(str(in_top_lat - in_btm_lat)) / res + Decimal(0.6)))
    # 提取数据
    tar_dataset = in_data[min_j:min_j + height-1, min_i:min_i + width-1]
    return tar_dataset


def min_box(tarbox, srcbox):
    '''计算最小box,前提是数据范围比box的范围大'''
    tar_top_lat, tar_btm_lon, tar_btm_lat, tar_top_lon = tarbox
    src_top_lat, src_btm_lon, src_btm_lat, src_top_lon = srcbox
    in_top_lon = Decimal(str(tar_top_lon)) if tar_top_lon > src_top_lon else Decimal(str(src_top_lon))
    in_top_lat = Decimal(str(tar_top_lat)) if tar_top_lat < src_top_lat else Decimal(str(src_top_lat))
    in_btm_lon = Decimal(str(tar_btm_lon)) if tar_btm_lon < src_btm_lon else Decimal(str(src_btm_lon))
    in_btm_lat = Decimal(str(tar_btm_lat)) if tar_btm_lat > src_btm_lat else Decimal(str(src_btm_lat))
    return in_top_lon, in_top_lat, in_btm_lon, in_btm_lat