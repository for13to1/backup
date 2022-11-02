import os
import re
import argparse
import numpy as np
from datetime import datetime

def parse_path(path):
    realpath = os.path.realpath(path)
    dirpath = os.path.dirname(realpath)
    basename = os.path.basename(realpath)
    filename, extnname = os.path.splitext(basename)
    return (realpath, dirpath, basename, filename, extnname)


def yuv_read(file):
    realpath, dirpath, _, filename, _ = parse_path(file)
    temp, title = filename.split("-")
    ptn_yuv_sfd = re.compile("([1-9]\d+)x([1-9]\d+)_(4[024]{2})(s?p)_(8|10)")
    result = ptn_yuv_sfd.match(temp)
    if result:
        width, height, sample, layout, bit_depth = result.groups()
        width = int(width)
        height = int(height)
        bit_depth = int(bit_depth)
        print(f"YUV load: {realpath}")
    else:
        raise Exception("Failed to parse filename.")

    if sample == "444":
        width_C, height_C = width, height
    elif sample == "422":
        width_C, height_C = width // 2, height
    elif sample == "420":
        width_C, height_C = width // 2, height // 2
    count_Y = width * height
    count_C = width_C * height_C

    data_type = np.uint8
    if bit_depth == 10:
        data_type = np.uint16

    data_YUV = np.fromfile(realpath, data_type)
    data_Y = data_YUV[0:count_Y].reshape(height, width)
    if layout == "p":
        data_U = data_YUV[count_Y : count_Y + count_C].reshape(height_C, width_C)
        data_V = data_YUV[count_Y + count_C :].reshape(height_C, width_C)
    elif layout == "sp":
        data_U = data_YUV[count_Y::2].reshape(height_C, width_C)
        data_V = data_YUV[count_Y + 1 :: 2].reshape(height_C, width_C)

    YUV = (data_Y, data_U, data_V, sample, layout, bit_depth, title, dirpath)
    return YUV


def yuv_write(YUV, title, directory):
    data_Y, data_U, data_V, sample, layout, bit_depth, _, dirpath_src = YUV
    height, width = data_Y.shape
    if layout == "p":
        out = np.concatenate([data.flatten() for data in (data_Y, data_U, data_V)])
    elif layout == "sp":
        out = np.append(data_Y.flatten(), np.stack((data_U, data_V), axis=2).flatten())

    if directory == "_":
        dirpath_dst = dirpath_src
    else:
        dirpath_dst = os.path.realpath(directory)
    basename = f"{width}x{height}_{sample}{layout}_{bit_depth}-{title}.yuv"
    path = os.path.join(dirpath_dst, basename)
    out.tofile(path)
    print(f"YUV save: {path}")

def yuv_layout_format(file_yuv, layout_dst):
    YUV = yuv_read(file_yuv)
    data_Y, data_U, data_V, sample, layout_src, bit_depth, title_src, dirpath_src = YUV
    if layout_src != layout_dst:
        title_dst = f"{title_src}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        YUV_dst = (data_Y, data_U, data_V, sample, layout_dst, bit_depth, title_dst, dirpath_src)
        yuv_write(YUV_dst, title_dst, directory=dirpath_src)
    else:
        raise Exception("With same layout, try to convert nothing!")


parser = argparse.ArgumentParser(description="Convert YUV file from layout planar to semi-planar, and vice versa.")

parser.add_argument("-i", "--file_yuv", type=str, required=True,
                    help="Filename format required: '/path/to/{WIDTH}x{HEIGHT}_{SAMPLE}{LAYOUT}_{BITDEPTH}-{TITLE}.yuv'")
parser.add_argument("-t", "--layout_dst", type=str, choices=["p", "sp"], required=True,
                    help="'p' for planar, 'sp' for semi-planar")

args = parser.parse_args()

file_yuv = args.file_yuv
layout_dst = args.layout_dst

yuv_layout_format(file_yuv, layout_dst)
