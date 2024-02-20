# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.12-2024.1
# ***************************************************************
import datetime
import os
import subprocess
import sys
import time
import numpy as np
import ftplib
from multiprocessing import Pool
import h5py
from PIL import Image
from bs4 import BeautifulSoup
import requests
from michaelPanPrintLib.change_print import print_with_style
import matplotlib.pyplot as plt
from osgeo import gdal, osr, gdal_array
import platform
import matplotlib
import matplotlib.dates as mdates
if platform.system() != "Windows":
    matplotlib.use('Agg')
gdal.UseExceptions()  # 避免osr使用警告
gdal.PushErrorHandler('CPLQuietErrorHandler')
print_with_style(f"该库的关键词有：ovr, matplotlib, tif, modis, file, time, array, shp, cleanup等，"
                 f"使用select_method方法查找具体的方法", no_color=True)
"""

"""


def select_method(select_str: str):  # 查询这个库里面有哪些方法
    """
    :param select_str: 任意想要查询的字符串
    :return: None
    """
    all_method_list = ['get_ovr_information方法，查看ovr文件的信息，不用再使用软件查看。',
                       'draw_many_matplotlib_pic方法，绘制一个主图上有多个子图的图片。',
                       'generate_ovr方法，使用HDF或PNG或tif数据生成ovr文件。',
                       'hdf_to_tif方法，HDF文件转换TIF文件。',
                       'modis_data_mosaic方法，完成modis数据拼接功能。',
                       'modis_data_projection方法，完成modis数据投影转换功能。',
                       'modis_data_download方法，完成modis数据下载功能。',
                       'modis_data_change_res方法，完成modis数据分辨率转换功能。',
                       'modis_data_clip_china方法，完成modis数据裁剪中国区功能。',
                       'time_date_num方法，完成时间年月日是一年中第几天的互转功能。'
                       'trans_file方法，完成文件传输任务。',
                       'array_to_rgba方法，完成图像数组依据颜色条绘制彩色图功能。',
                       'clip_image_by_shp方法，完成依据shp文件对彩色图进行裁剪功能',
                       'cleanup_server_disk方法，完成服务器磁盘空间清理功能',
                       'start_a_timed_task方法，完成启动一个定时任务功能'
                       ]
    print_with_style(f"输入的查询参数为：{select_str}，查询的结果如下：", color='blue')
    for a_info in all_method_list:
        if select_str in a_info:
            print_with_style(f"   {a_info}", color='cyan')


def get_ovr_information(input_ovr_file: str, show_img=False):  # 查看ovr文件的信息，不用再使用软件查看
    """
    :param input_ovr_file: 传入的ovr文件路径
    :param show_img: 是否显示图片，默认为False
    :return: None
    """
    # 打开OVR文件
    ds = gdal.Open(input_ovr_file)
    print_with_style(f"当前打开的ovr文件为：【{os.path.basename(input_ovr_file)}】", color="blue")
    # 获取投影信息
    proj = ds.GetProjection()
    print_with_style(f"该ovr文件的投影信息为：【{proj}】", color="blue")
    # 获取地理变换信息
    geo_transform = ds.GetGeoTransform()
    print_with_style(f"该ovr文件的地理变换信息为：【{geo_transform}】", color="blue")
    # 读取第一个波段的数据到NumPy数组
    band = ds.GetRasterBand(1)
    image = band.ReadAsArray()
    print_with_style(f"该ovr文件的图像尺寸为：【{image.shape}】", color="blue")
    if show_img:
        # 创建pyplot图形
        plt.figure()
        # 显示数组作为灰度图像
        plt.imshow(image, cmap='jet')
        # 不显示坐标轴值
        plt.axis('off')
        plt.show()
    # 关闭数据集
    ds = None


def draw_many_matplotlib_pic(num_plot: list, w_h: list, x_data: list, y_data: list, x_ticks: list, y_ticks: list,
                             x_label: list,
                             y_label: list, x_lim: list, y_lim: list, sub_title: list, pic_type: list,
                             pic_line_color: list,
                             time_type: list, title: str, save_or_show: str, font_path=None):  # 绘制一个主图上有多个子图的图片
    """
    :param num_plot: 子图的数量，传入行列数量的列表，例如[12, 10]
    :param w_h: 主图的长和宽，例如[10, 7]
    :param x_data:  每一个子图的x轴数据，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
    :param y_data:  每一个子图的y轴数据，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
    :param x_ticks: 每一个子图的x轴显示，先行后列，例如：子图数量是2*2，[[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]]
    :param y_ticks: 每一个子图的x轴显示，先行后列，例如：子图数量是2*2，[[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]]
    :param x_label: 每一个子图的x轴标签，先行后列，例如：子图数量是2*2，['这是x1', '这是x2', '这是x3', '这是x4']
    :param y_label: 每一个子图的y轴标签，先行后列，例如：子图数量是2*2，['这是y1', '这是y2', '这是y3', '这是y4']
    :param x_lim:   每一个子图的x轴范围，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
    :param y_lim:   每一个子图的y轴范围，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
    :param sub_title: 每一个子图的标题，先行后列，例如：子图数量是2*2，['这是标题1', '这是标题2', '这是标题3', '这是标题4']
    :param pic_type: 绘制哪种类型的图有折线、散点、直方图，对应字符串位 line point rectangle，例如：子图数量是2*2，['line', 'line', 'line', 'line']
    :param pic_line_color: 每一个子图颜色，先行后列，例如：子图数量是2*2，['blue', 'blue', 'blue', 'blue']
    :param time_type: 每一个子图是否需要将X轴显示时间,为None是不需要，先行后列，例如：子图数量是2*2，[None, '%m-%d %H', None, None]
    :param title: 主图的标题
    :param save_or_show: 保存或者显示图片，show为展示，传入路径为保存
    :param font_path: 默认为None，当显示中文时需要传入支持中文的字体
    :return: None
    
    ----
    draw_many_matplotlib_pic([2, 2], [12, 10],
                             [[0, 1], [0, 1], [0, 1], [0, 1]],
                             [[0, 1], [0, 1], [0, 1], [0, 1]],
                             [[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]],
                             [[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]],
                             ['这是x1', '这是x2', '这是x3', '这是x4'],
                             ['这是y1', '这是y2', '这是y3', '这是y4'],
                             [[0, 1], [0, 1], [0, 1], [0, 1]],
                             [[0, 1], [0, 1], [0, 1], [0, 1]],
                             ['这是标题1', '这是标题2', '这是标题3', '这是标题4'],
                             ['line', 'line', 'line', 'line'],
                             ['blue', 'blue', 'blue', 'blue'],
                             [None, '%m-%d %H', None, None],
                             '这是主标题',
                             'show')
    """
    from matplotlib import font_manager
    if font_path is not None:
        my_font = font_manager.FontProperties(fname=font_path)  # 坐标轴显示中文，simsun.ttc表示字体文件
    fig, ax = plt.subplots(num_plot[0], num_plot[1])
    fig.set_size_inches(w_h[0], w_h[1])
    if font_path is not None:
        fig.suptitle(title, y=0.95, ha='center', fontproperties=my_font)
    else:
        fig.suptitle(title, y=0.95, ha='center')
    count_num = 0
    for i in range(num_plot[0]):
        for j in range(num_plot[1]):
            if pic_type[count_num] == 'line':
                ax[i, j].plot(x_data[count_num], y_data[count_num], color=pic_line_color[count_num])
            elif pic_type[count_num] == 'point':
                ax[i, j].scatter(x_data[count_num], y_data[count_num], c=pic_line_color[count_num])
            elif pic_type[count_num] == 'rectangle':
                ax[i, j].hist(x_data[count_num], y_data[count_num], c=pic_line_color[count_num])
            if time_type[count_num] is not None:
                # 改变时间显示样式
                ax[i, j].xaxis.set_major_formatter(mdates.DateFormatter(time_type[count_num]))
            ax[i, j].set_xlim(x_lim[count_num])
            ax[i, j].set_xticks(x_ticks[count_num])
            ax[i, j].set_yticks(y_ticks[count_num])
            ax[i, j].set_ylim(y_lim[count_num])
            if font_path is not None:
                ax[i, j].set_ylabel(y_label[count_num], fontproperties=my_font)
                ax[i, j].set_xlabel(x_label[count_num], fontproperties=my_font)
                ax[i, j].set_title(sub_title[count_num], fontproperties=my_font)
            else:
                ax[i, j].set_ylabel(y_label[count_num])
                ax[i, j].set_xlabel(x_label[count_num])
                ax[i, j].set_title(sub_title[count_num])
            count_num += 1
            print(count_num)
    if save_or_show == 'show':
        plt.show()
    else:
        fig.savefig(save_or_show, format='pdf', bbox_inches='tight', dpi=300)


def generate_ovr(input_file_path: str, database_name: str, res: float, lon=-180, lat=90,
                 band_name=None):  # HDF或PNG或tif数据生成ovr文件
    """
    :param input_file_path:  输入的HDF或PNG或tif文件
    :param database_name:  数据集名称
    :param res: 分辨率
    :param lon: 最小经度
    :param lat: 最大维度
    :param band_name: 当数据为多维度数据时使用 如果是2*1440*720的数据 那么band_name就应该是['ab', 'aa']
    :return: None
    """
    input_file_path_temp = input_file_path.lower()
    output_file_path = f"{os.path.dirname(input_file_path)}/{os.path.basename(input_file_path).split('.')[0]}.{database_name.replace('/', '-')}.tif"
    if input_file_path_temp.endswith('.hdf'):
        # 打开HDF5文件
        hdf5_file = h5py.File(input_file_path, 'r')
        # 获取数据集
        dataset = hdf5_file[database_name][:]
        # 读取为numpy数组
        dataset_list = []
        output_path_list = []
        # --------------判断数据集通道数量-------------
        if dataset.ndim > 2:
            for i in range(dataset.shape[2]):
                if dataset.shape[2] == 2:  # 当第三个维度通道数为2时
                    dataset_list.append(dataset[:, :, i])
                elif dataset.shape[0] == 2:
                    dataset_list.append(dataset[i, :, :])
                elif dataset.shape[2] > 2:
                    dataset_list.append(dataset[:, :, 0])
                    break
                elif dataset.shape[0] > 2:
                    dataset_list.append(dataset[0, :, :])
                    break
        else:
            dataset_list.append(dataset)
        # ------------------------------------------
        for i, dataset in enumerate(dataset_list):
            if len(dataset_list) == 2:  # 当通道数大于1时修改输出文件名
                for_path, file_extension = os.path.splitext(output_file_path)
                if band_name is None:
                    print(f'输入为多通道数据，但是配置文件中未给出，请检查')
                    output_path = f"{for_path}_{i}{file_extension}"
                else:
                    output_path = f"{for_path}-{band_name[i]}{file_extension}"
            else:
                output_path = output_file_path
            # 获取维度
            xsize = dataset.shape[1]
            ysize = dataset.shape[0]
            # 创建GeoTIFF数据集
            gtiff_driver = gdal.GetDriverByName('GTiff')
            gtiff_ds = gtiff_driver.Create(output_file_path, xsize, ysize, 1, gdal.GDT_Float32)
            # 设置投影坐标系
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)  # WGS84经纬度坐标
            gtiff_ds.SetProjection(srs.ExportToWkt())
            # 写入数组数据到GeoTIFF
            gdal_array.BandWriteArray(gtiff_ds.GetRasterBand(1), dataset)
            gdal.AllRegister()
            # 生成ovr金字塔
            gtiff_ds = None
            ds = gdal.Open(output_file_path)
            ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32, 64, 128, 256])
            ovrds = gdal.Open(output_file_path + '.ovr', gdal.GA_Update)
            ovrds.SetGeoTransform([lon, res, 0, lat, 0, -res])
            proj = osr.SpatialReference()
            proj.SetWellKnownGeogCS('WGS84')
            ovrds.SetProjection(proj.ExportToWkt())
            # 关闭文件
            ovrds = None
            ds = None
            # 删除中间的tif
            os.remove(output_path)
            hdf5_file.close()
    
    elif input_file_path_temp.endswith('.tif'):
        gdal.AllRegister()
        ds = gdal.Open(input_file_path)  # 加了gdal.GA_Update时，读入JPG返回的事none
        ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32, 64, 128, 256])
        output_path = input_file_path + '.ovr'
        ovrds = gdal.Open(output_path, gdal.GA_Update)
        ovrds.SetGeoTransform([lon, res, 0, lat, 0, -res])
        proj = osr.SpatialReference()
        proj.SetWellKnownGeogCS('WGS84')
        ovrds.SetProjection(proj.ExportToWkt())
    elif input_file_path_temp.endswith('.png'):
        tempimg = Image.open(input_file_path)
        tempimg = tempimg.resize((8192, 4096), Image.ANTIALIAS)
        output_path = f"{os.path.dirname(input_file_path)}/{os.path.basename(input_file_path).split('.')[0]}_change.png"
        tempimg.save(output_path)
        ds = gdal.Open(output_path)
        ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32])  # , 16, 32, 64, 128, 256
        ds.SetGeoTransform([lon, res, 0, lat, 0, -res])
        proj = osr.SpatialReference()
        proj.SetWellKnownGeogCS('WGS84')
        ds.SetProjection(proj.ExportToWkt())


def hdf_to_tif(input_hdf_file: str, database_name: str, output_tif_file: str):  # HDF文件转换TIF文件
    hdf5_file = h5py.File(input_hdf_file, 'r')
    dset = hdf5_file[database_name]
    hdf5_data = dset[:]
    xsize = dset.shape[1]
    ysize = dset.shape[0]
    # 创建geotiff
    driver = gdal.GetDriverByName("GTiff")
    output_ds = driver.Create(output_tif_file, xsize, ysize, 1, gdal.GDT_Float32)
    # 设置投影
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    output_ds.SetProjection(srs.ExportToWkt())
    output_ds.GetRasterBand(1).WriteArray(hdf5_data)
    # 关闭文件
    hdf5_file.close()
    output_ds = None


def modis_data_mosaic(input_path):  # 完成modis数据拼接功能
    """
    :param input_path: 下载的modis hdf数据路径
    :return: None
    """
    input_path_list = os.listdir(input_path)
    input_files = []
    count_num = 0
    geotransform = 0
    for a_path in input_path_list:
        a_path = f"{input_path}/{a_path}"
        if a_path.endswith('tif') and 'output_merge' not in a_path:
            if count_num == 0:
                dataset = gdal.Open(a_path)
                geotransform = dataset.GetGeoTransform()
                count_num += 1
            input_files.append(a_path)
    # 新建一个VRT数据集
    output_vrt = f'{input_path}/output.vrt'
    vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear')
    vrt_ds = gdal.BuildVRT(output_vrt, input_files, options=vrt_options)
    # 为VRT数据集设置geotransform和projection
    projection = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    vrt_ds.SetProjection(projection)
    vrt_ds.SetGeoTransform(geotransform)
    # 将VRT数据集重新投影并合并到单个GeoTIFF中
    output_geotiff = f'{input_path}/output_merge.tif'
    gdal.Warp(output_geotiff, vrt_ds, dstSRS='EPSG:4326', outputType=gdal.GDT_Float32)
    # 清理内存
    vrt_ds = None
    del vrt_ds
    os.remove(output_vrt)
    print_with_style(f'【{input_path}】路径下的数据拼接成功', color='cyan')


def modis_data_projection(input_path, k1, k2, proj='WGS84'):  # 完成modis数据投影转换功能
    """
    :param input_path: 下载的hdf文件夹路径
    :param k1: 数组在modis数据集中的位置，例如 0
    :param k2: 数组在modis数据集中的位置，例如 0
    :param proj: 投影方式，可以不填，默认WGS84
    :return: None
    """
    for a_path in os.listdir(input_path):
        a_path = f"{input_path}/{a_path}"
        if a_path.endswith('hdf'):
            srs = osr.SpatialReference()
            srs.SetWellKnownGeogCS(proj)
            in_ds = gdal.Open(a_path)
            datasets = in_ds.GetSubDatasets()
            output_tif_path = a_path.replace('hdf', 'tif')
            gdal.Warp(output_tif_path, datasets[k1][k2], dstSRS=srs.ExportToWkt())
    print_with_style(f'【{input_path}】路径下的数据投影转换成功', color='cyan')


def modis_data_change_res(input_file, output_file, res, proj='WGS84'):  # 完成modis数据分辨率转换功能
    """
    :param input_file: 需要转换的tif文件
    :param output_file: 转换完成后输出的tif文件
    :param res: 需要转换的目标分辨率
    :param proj:  投影方式，可以不填，默认WGS84
    :return: None
    """
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS(proj)
    in_ds = gdal.Open(input_file)
    gdal.Warp(output_file, in_ds, dstSRS=srs.ExportToWkt(), xRes=res, yRes=res)
    print_with_style(f'【{input_file}】文件数据分辨率转换成功', color='cyan')


def modis_data_clip_china(input_file, output_file):  # 完成modis数据裁剪中国区功能
    cmd_str = "gdalwarp -of GTiff -te 70.0 0.0 140.0 60.0 " + input_file + " " + output_file
    os.system(cmd_str)


def modis_data_download(task: str, this_year: int, days_num: str, part_list: list, download_path: str,
                        token1=None):  # 完成modis数据下载功能
    """
    :param task: 下载任务，例如：MOD11A1
    :param this_year: 下载的年：例如：2023
    :param days_num:  下载的年中第几天，例如253    ps:可以用time_date_num方法转换
    :param part_list:  地区列表，例如["h23v03", "h24v03", "h25v03"]
    :param download_path: 下载的路径，例如：D:/work/temp/LST/156
    :param token1: 可以不添加，当方法中自带token失效时，需要传入新的
    :return: None
    """
    if token1 is None:
        token1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2OTg3MTk5NTUsIm5iZiI6MTY5ODcxOTk1NSwiZXhwIjoxODU2Mzk5OTU1LCJ1aWQiOiJ6b2VsdTIwMjIiLCJlbWFpbF9hZGRyZXNzIjoiMzA0OTQ4MzQ0QHFxLmNvbSIsInRva2VuQ3JlYXRvciI6InpvZWx1MjAyMiJ9.9owE4fUkODF8xQ0DHzbQaQJ2CA7K8IMde896Q4jh0Hg"
    root_url = f"https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/61/{task}"
    output_file_list = []
    download_url_list = []
    alter_url = f"{root_url}{this_year}/{days_num}"
    # 发送GET请求，设置cookies
    response_root = requests.get(alter_url, verify=False)
    if response_root.status_code == 200:
        soup_root = BeautifulSoup(response_root.text, "html.parser")
        link_tags = soup_root.findAll("a")
        # 遍历提取出的元素，获取链接列表
        for a_tag in link_tags:
            a_href = a_tag.get("href")
            if ".hdf" in a_href and a_href != "None":  # 进行数据筛选
                if len(part_list) > 1:  # 指定地区的情况
                    a_part = a_href.split(".")[2]  # 地区位置
                    if a_part not in part_list:  # 位置不在地区列表的情况
                        continue
                else:  # 全部地区的情况
                    pass
                file_url = f"{alter_url}/{os.path.basename(a_href)}"
                out_file_path = f"{download_path}/{os.path.basename(a_href)}"
                if file_url in download_url_list:  # 过滤掉重复路径
                    continue
                if not os.path.exists(out_file_path):  # 文件不存在时
                    download_url_list.append(file_url)
                    output_file_list.append(out_file_path)
                else:
                    # 获取文件大小（以字节为单位）
                    file_size = os.path.getsize(out_file_path)
                    file_size_kb = file_size / 1024
                    if file_size_kb > 5:
                        download_url_list.append(file_url)
                        output_file_list.append(out_file_path)
    print_with_style(f"开始下载，总共{len(download_url_list)}个，请耐心等待...", no_color=True)
    if len(download_url_list) > 1:  # 去掉所有数据都存在的情况
        pool = Pool(processes=5)
        for j in range(len(download_url_list)):
            if os.path.exists(output_file_list[j]):  # 如果下载文件存在且文件大小大于20KB时跳过下载
                file_size = int(os.path.getsize(output_file_list[j]) / (1024 * 20))
                if file_size >= 1:
                    print_with_style(f"{output_file_list[j]}文件已经存在，跳过下载。", no_color=True)
            pool.apply_async(func=download_func,
                             args=(download_url_list[j], token1, output_file_list[j], j, len(download_url_list)), )
        pool.close()
        pool.join()
    print_with_style(f"{this_year}年第{int(days_num)}天的{task}数据下载完成！", no_color=True)


def time_date_num(input_str: str):  # 完成时间年月日是一年中第几天的互转功能
    """
    :param input_str: 时间字符串，格式为这两种：20230605或2023256，第一种是年月日，第二种是年第几天
    :return: None
    """
    if len(input_str) == 8:
        input_time = datetime.datetime.strptime(input_str, "%Y%m%d")
        day_of_year = input_time.timetuple().tm_yday
        print_with_style(f"当前日期为{input_str[:4]}年第{day_of_year}天", color='blue')
    elif len(input_str) == 7:
        init_time = datetime.datetime.strptime(f"{input_str[:4]}0101", "%Y%m%d")
        finish_time = init_time + datetime.timedelta(days=int(input_str[4:]) - 1)
        time_str = finish_time.strftime("%Y%m%d")
        print_with_style(f"{input_str[:4]}年第{int(input_str[4:])}天的日期为：{time_str}", color='blue')
    else:
        raise Exception(f"时间字符串位数不对，请检查输入是否正确，当前输入为【{input_str}】")


def trans_file(ftp_host: str, ftp_port: int, ftp_username: str, ftp_password: str, local_file: str,
               server_path: str):  # 完成文件传输任务
    """
    :param ftp_host:  看名称即可
    :param ftp_port:  看名称即可
    :param ftp_username:  看名称即可
    :param ftp_password:  看名称即可
    :param local_file:  需要上传的本地文件路径
    :param server_path:  ftp服务器路径
    :return: None
    """
    # 连入Ftp服务器
    ftp = ftplib.FTP()
    ftp.connect(ftp_host, ftp_port)
    ftp.login(ftp_username, ftp_password)
    # 如果目录不存在的话创建目录
    os.makedirs(os.path.dirname(server_path), exist_ok=True)
    # 上传本地文件到FTP服务器
    with open(local_file, "rb") as file:
        ftp.storbinary("STOR " + server_path, file)
    # 关闭FTP连接
    ftp.close()


def array_to_rgba(data_array, color_bar_dic):  # 完成图像数组依据颜色条绘制任务
    """
    :param data_array: 二维图像数组
    :param color_bar_dic: 颜色条字典
    :return: Pillow格式的彩色图像, ndarray格式彩色图像数组(uint8), ndarray格式彩色图像数组(无固定类型)
    """
    t1 = time.time()
    print_with_style(f"程序开始，下面进行彩色图绘制(如果最后生成的图片为空白图，请检查数据集与颜色阈值字典是否匹配)",
                     no_color=True)
    color_image = np.ones((*data_array.shape, 4), dtype=np.uint8)  # 初始化彩色图像
    for a_key in color_bar_dic.keys():  # 遍历颜色条字典
        a_kind_list = color_bar_dic[a_key]
        dn_before = 0  # 初始化渐变绘图前置参数
        for i, a_tip_list in enumerate(a_kind_list):
            a_value = a_tip_list[0]
            a_color = a_tip_list[1]
            a_color.append(255)  # JPG to PNG
            if a_key == "range":  # 阈值范围绘图
                min_value, max_value = a_value
                mask = (data_array >= min_value) & (data_array < max_value)
                color_image[mask] = a_color
            elif a_key == "gradient":  # 渐变绘图，根据颜色字典来映射，并给二维数组上色
                if i == 0:
                    mask = data_array <= a_value
                    dn_before = a_value
                else:
                    mask = (data_array <= a_value) * (data_array > dn_before)
                    dn_before = a_value
                color_image[mask] = a_color
            else:  # single,fill,etc...
                color_image[data_array == a_value] = a_color
    img = Image.fromarray(color_image).convert('RGBA')
    t2 = time.time()
    print_with_style(f"绘图完成，总共用时为:【{round((t2 - t1), 2)}s】", no_color=True)
    return img, color_image, data_array


def clip_image_by_shp(image, file_read, data_array, shp_path):  # 依据shp对彩色图进行裁剪
    """
    :param image: ndarray格式彩色图像数组(uint8)---可以参考array_to_rgba方法返回值
    :param file_read: h5py库打开的对象
    :param data_array: ndarray格式彩色图像数组(无固定类型)---可以参考array_to_rgba方法返回值
    :param shp_path: shp文件路径
    :return: 裁剪后的图像或未裁剪的图像
    """
    import geopandas as gpd
    import cv2
    t1 = time.time()
    # 读取shp文件
    df = gpd.read_file(shp_path)
    # if 'NAME' in df.keys():
    #     result = df.loc[df['NAME'] == '西藏']
    # else:
    #     result = df
    result = df['geometry']
    coords = result.to_crs(epsg=4326).apply(lambda x: x.exterior.coords)
    point_list = []
    for a_coord in coords:
        for a_point in a_coord:
            point_list.append([a_point[0], a_point[1]])
    point_array = np.array(point_list)
    x_min = np.min(point_array[:, 0])
    x_max = np.max(point_array[:, 0])
    y_min = np.min(point_array[:, 1])
    y_max = np.max(point_array[:, 1])
    print_with_style(f"边界线点的最大最小坐标为： x_min:{x_min} | x_max:{x_max} | y_min:{y_min} | y_max:{y_max}",
                     color='blue')
    if "Maximum Latitude" in file_read.attrs.keys():
        x_min_h5 = file_read.attrs['Minimum Longitude']
        x_max_h5 = file_read.attrs['Maximum Longitude']
        y_min_h5 = file_read.attrs['Minimum Latitude']
        y_max_h5 = file_read.attrs['Maximum Latitude']
    elif "Left-Top X" in file_read.attrs.keys():
        x_min_h5 = file_read.attrs['Left-Top X']
        x_max_h5 = file_read.attrs['Right-Top X']
        y_min_h5 = file_read.attrs['Left-Bottom Y']
        y_max_h5 = file_read.attrs['Right-Top Y']
    else:
        x_min_h5 = 78
        x_max_h5 = 99.5
        y_min_h5 = 26
        y_max_h5 = 36.5
        print_with_style('请注意，数据集中没有经纬度范围，故赋值为西藏地区范围')
    print_with_style(
        f"HDF数据的最大最小坐标为： x_min_h5:{x_min_h5} | x_max_h5:{x_max_h5} | y_min_h5:{y_min_h5} | y_max_h5:{y_max_h5}",
        color='blue')
    if x_min_h5 <= x_min and y_min_h5 <= y_min and x_max_h5 >= x_max and y_max_h5 >= y_max:
        data_y_shape, data_x_shape = data_array.shape
        x_min_img = abs(x_max - x_max_h5) / 2
        y_min_img = abs(y_max - y_max_h5) / 2
        ratio_x = data_x_shape / (x_max_h5 - x_min_h5)
        ratio_y = data_y_shape / (y_max_h5 - y_min_h5)
        print_with_style(f"图像的尺寸【x:{data_x_shape}，y:{data_y_shape}】，比例系数【x:{ratio_x}，y:{ratio_y}】",
                         color='blue')
        multipliers = np.array([ratio_x, ratio_y]).reshape(1, -1)  # 比例系数矩阵
        subtrahends = np.array([x_min + x_min_img, y_min + y_min_img]).reshape(1, -1)  # 相对坐标矩阵
        points = np.array((point_array - subtrahends) * multipliers)  # 获得点在图像上的绝对位置
        points = points.astype(np.int32)
        mask = np.zeros((data_y_shape, data_x_shape, 4), dtype=np.uint8)
        cv2.fillPoly(mask, [points], (255, 255, 255, 255))
        mask = np.flip(mask, axis=0)  # 翻转y轴，避免边界线显示错误
        # 应用掩膜
        masked_image = cv2.bitwise_and(image, mask)
        img = Image.fromarray(masked_image).convert('RGBA')
        mask_poly = np.zeros((data_y_shape, data_x_shape, 4), dtype=np.uint8)
        mask_poly = cv2.polylines(mask_poly, [points], isClosed=True, color=(0, 0, 0, 255), thickness=1)
        mask_poly = np.flip(mask_poly, axis=0)  # 翻转y轴，避免边界线显示错误
        img_poly = Image.fromarray(mask_poly).convert('RGBA')
        img.paste(img_poly, (0, 0), mask=img_poly)
        t2 = time.time()
        print_with_style(f"生成彩色裁剪图像成功，用时为：【{round((t2 - t1), 2)}s】", no_color=True)
        return img
    else:
        print_with_style('数据集中的图像范围与目标地区范围未完全重叠或不重叠，直接返回无边界线图片')
        image = Image.fromarray(image).convert('RGBA')
        return image


def cleanup_server_disk(all_task):  # 服务器磁盘空间清理功能
    """
    :param all_task:  # 需要清理数据的列表，第一个参数为路径，第二个参数为保存天数，第三个参数为清理的文件格式(可以没有)。路径中
    DATE_MD、DATE_Y是替换子字符串，指代年月日 、年。 参数样例如下：
     [
        ['E:/pycharm_project/michaelPanUtilsLib/data/LST/DATE_MD/TMP', 5],
        ['E:/pycharm_project/michaelPanUtilsLib/data/SIC', 12, 'hdf'],
        ['E:/pycharm_project/michaelPanUtilsLib/data/OLR/DATE_Y/DATE_MD/TMP', 12]
     ]
    :return: None
    """
    print_with_style('清理功能将在5秒后开始运行，请再次核对路径是否正确，确保数据安全！')
    time.sleep(5)
    t1 = time.time()
    for a_task in all_task:  # 对于每一条清理信息
        save_day_len = a_task[1]
        a_path = a_task[0]
        file_type = None
        if len(a_task) > 2:  # 获取指定的文件类型
            file_type = a_task[2]
        if len(a_path) < 5:
            print_with_style(f"路径太短，为了安全自动跳过该条路径的清理：【{a_path}】")
            continue
        current_myd = datetime.datetime.now()
        for i in range(5000):  # 5000天的数据
            time_difference = current_myd - datetime.timedelta(days=i + save_day_len)
            y_time = time_difference.strftime("%Y")
            ymd_time = time_difference.strftime("%Y%m%d")
            if 'DATE_MD' not in a_path and 'DATE_Y' not in a_path:
                if not os.path.exists(a_path):  # 删除的路径不存在
                    continue
                for a_file in os.listdir(a_path):
                    if file_type is not None and not a_file.lower().endswith(file_type.lower()):
                        continue
                    if ymd_time in a_file:
                        print_with_style(f"删除【{a_path}/{a_file}】文件", no_color=True)
                        os.remove(f"{a_path}/{a_file}")
                if not os.listdir(a_path):
                    os.rmdir(a_path)
            else:
                a_path_alter = a_path.replace("DATE_Y", y_time).replace("DATE_MD", ymd_time)
                if not os.path.exists(a_path_alter):  # 删除的路径不存在
                    continue
                for a_file in os.listdir(a_path_alter):
                    if file_type is not None and not a_file.lower().endswith(file_type.lower()):
                        continue
                    print_with_style(f"删除【{a_path_alter}/{a_file}】文件", no_color=True)
                    os.remove(f"{a_path_alter}/{a_file}")
                if not os.listdir(a_path_alter):
                    os.rmdir(a_path_alter)
    t2 = time.time()
    print_with_style(f"数据清理完成，用时为：【{round((t2 - t1), 2)}s】", no_color=True)

def print_hello():
    print('hello world')

def start_a_timed_task(sec, a_function, args=None):  # 启动一个定时任务
    """
    :param sec: 多少秒执行一次
    :param a_function: 一个需要定时启动的方法
    :param args: 方法的参数字典(方法无参数的时候，字典为空)
    :return: None
    """
    from apscheduler.schedulers.blocking import BlockingScheduler
    # 创建一个调度器
    scheduler = BlockingScheduler()
    # 添加一个定时任务
    scheduler.add_job(a_function, 'interval', seconds=sec, kwargs=args)
    # 启动调度器
    scheduler.start()

# -----------------------------------------方法中用到的方法功能区，一般不作单独调用---------------------------------------------
def download_func(file_url, token1, out_file_path, j, i):
    str_html = requests.get(file_url, headers={"Authorization": f"Bearer {token1}"}, verify=False)
    if str_html.status_code != 200:
        print_with_style(f"{file_url}下载失败，状态码为：{str_html.status_code}", no_color=True)
    else:
        command = """wget -c --no-verbose --cut-dirs=3 "{file_url}" --header "Authorization: Bearer {token1}" -O {out_file_path}""".format(
            file_url=file_url, token1=token1, out_file_path=out_file_path)
        subprocess.call(command, shell=True)
        print_with_style(f"{out_file_path}下载完成({j}/{i})", no_color=True)
        print_with_style(f"下载URL为：{file_url}", no_color=True)


if __name__ == "__main__":
    # select_method('ovr')
    # modis_data_projection('D:/work/temp/LST/346', 0, 0)
    # modis_data_mosaic('D:/work/temp/LST/346')
    # time_date_num("20230819")
    # get_ovr_information("D:/pycharm_project/shinetekview-overview-pct/data/FY3G_PMR_Latlon_L3_KuR_GBAL_20231114000000_20231114235959_025KM_POAD_N.HDF.Ascending-precipRateESurface-mean.tif.ovr", show_img=True)
    # hdf_to_tif("D:/pycharm_project/shinetekview-overview-pct/data/FY3D_MERSI_GBAL_L2_LST_MLT_GLL_20210701_POAD_025KM_MS.HDF","MERSI_25Km_LST_N", "D:/pycharm_project/shinetekview-overview-pct/data/FY3D_MERSI_GBAL_L2_LST_MLT_GLL_20210701_POAD_025KM_MS.tif")
    # generate_ovr("D:/pycharm_project/shinetekview-overview-pct/data/FY3E_GNOSR_Latlon_L3_SWS_ORBT_20231121000000_20231121235959_025KM_POAD_X.HDF","GAL/SWS",0.25)
    # draw_many_matplotlib_pic([2, 2], [12, 10],
    #                          [[0, 1], [0,0.1, 0.3, 1], [0, 1], [0, 1]],
    #                          [[0, 1], [0,0.2, 0.5, 1], [0, 1], [0, 1]],
    #                          [[0.1, 0.9], [10, 20], [0.1, 0.9], [0.1, 0.9]],
    #                          [[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]],
    #                          ['这是x1', '这是x2', '这是x3', '这是x4'],
    #                          ['这是y1', '这是y2', '这是y3', '这是y4'],
    #                          [[0, 1], [0, 1], [0, 1], [0, 1]],
    #                          [[0, 1], [0, 1], [0, 1], [0, 1]],
    #                          ['这是标题1', '这是标题2', '这是标题3', '这是标题4'],
    #                          ['line', 'point', 'line', 'line'],
    #                          ['blue', 'blue', 'blue', 'blue'],
    #                          [None, '%m-%d %H', None, None],
    #                          '这是主标题',
    #                          'show',
    #                          'D:/pycharm_project/michaelPanUtilsLib/simsun.ttc')
    # img, color_image, data_array = array_to_rgba(h5py.File(r'E:\pycharm_project\Xizang_provincial_station\data\FY3D_MERSI_Latlon_L2_LAI_20230612_0250M_Latlon_D.HDF', 'r')['LAI'][()], {"fill": [[32001, [0, 0, 0], "填充值"]],"gradient": [[0, [255, 255, 255]], [0.25, [255, 227, 132]], [0.50, [255, 255, 0]], [0.75, [255, 128, 0]],[1, [51, 204, 51]], [2, [0, 255, 0]], [3, [0, 128, 0]], [4, [0, 102, 0]], [5, [255, 124, 128]],[6, [204, 0, 0]], [7, [255, 0, 255]], [8, [255, 0, 0]], [9, [102, 0, 204]]]})
    # array_to_tif(h5py.File(r'E:\pycharm_project\Xizang_provincial_station\data\FY3D_MERSI_Latlon_L2_LAI_20230612_0250M_Latlon_D.HDF', 'r')['LAI'][()], 'test1.tif',[78,3, 36.5], 0.0025)
    # cliped_img = clip_image_by_shp(color_image, h5py.File(r'E:\pycharm_project\Xizang_provincial_station\data\FY3D_MERSI_Latlon_L2_LAI_20230612_0250M_Latlon_D.HDF', 'r'), data_array, r'E:\pycharm_project\Xizang_provincial_station\data\shp\xizang\province.shp')
    # start_a_timed_task(3, print_hello, {})
    pass

