import os
import re
import argparse
import numpy as np
from datetime import datetime

def get_CSC_coefficient(trend, gamut, bit_depth_img, bit_depth_coef, range_rgb, range_yuv):
    # 
    if gamut == "bt601":
        coef_Edot_RGB_to_Y = np.array([0.299, 0.587, 0.114])
    elif gamut == "bt709":
        coef_Edot_RGB_to_Y = np.array([0.2126, 0.7152, 0.0722])
    coef_Edot_R_minus_Y = (np.array([1, 0, 0]) - coef_Edot_RGB_to_Y)
    coef_Edot_B_minus_Y = (np.array([0, 0, 1]) - coef_Edot_RGB_to_Y)
    coef_Edot_RGB_to_Cr = coef_Edot_R_minus_Y / (2 * coef_Edot_R_minus_Y[0])
    coef_Edot_RGB_to_Cb = coef_Edot_B_minus_Y / (2 * coef_Edot_B_minus_Y[2])
    coef_Edot_RGB_to_YCbCr = np.vstack([coef_Edot_RGB_to_Y, coef_Edot_RGB_to_Cb, coef_Edot_RGB_to_Cr])
    assert(np.isclose(coef_Edot_RGB_to_YCbCr[0].sum(), 1))
    assert(np.isclose(coef_Edot_RGB_to_YCbCr[1].sum(), 0))
    assert(np.isclose(coef_Edot_RGB_to_YCbCr[2].sum(), 0))
    # coef_Edot_RGB_to_YCbCr = np.around(coef_Edot_RGB_to_YCbCr, 3)
    print(coef_Edot_RGB_to_YCbCr)
    min_rgb = 0
    mid_rgb = 1 << (bit_depth_img - 1)
    max_rgb = (1 << bit_depth_img) -1
    if range_rgb == "full":
        low_rgb, high_rgb = min_rgb, max_rgb
    elif range_rgb == "limited":
        low_rgb = 16 << (bit_depth_img - 8)
        high_rgb = 235 << (bit_depth_img - 8)
    
    min_yuv = 0
    mid_yuv = 1 << (bit_depth_img - 1)
    max_yuv = (1 << bit_depth_img) -1
    if range_yuv == "full":
        low_yuv, high_y, high_uv = min_yuv, max_yuv, max_yuv
    elif range_yuv == "limited":
        low_yuv = 16 << (bit_depth_img - 8)
        high_y = 235 << (bit_depth_img - 8)
        high_uv = 240 << (bit_depth_img - 8)

    coef_Ddot_RGB_to_YCbCr = coef_Edot_RGB_to_YCbCr.copy()
    coef_Ddot_RGB_to_YCbCr[0] *= (high_y - low_yuv) / (high_rgb - low_rgb)
    coef_Ddot_RGB_to_YCbCr[1:] *= (high_uv - low_yuv) / (high_rgb - low_rgb)
    coef_Ddot_RGB_to_YCbCr = np.around(coef_Ddot_RGB_to_YCbCr, 4)
    print(coef_Ddot_RGB_to_YCbCr)

    coef_Ddot_RGB_to_YCbCr_fix = coef_Ddot_RGB_to_YCbCr.copy()
    coef_Ddot_RGB_to_YCbCr_fix *= 1 << bit_depth_coef
    coef_Ddot_RGB_to_YCbCr_fix = np.around(coef_Ddot_RGB_to_YCbCr_fix)
    print(coef_Ddot_RGB_to_YCbCr_fix)

    coef_Edot_YCbCr_to_RGB = np.ones((3, 3))
    coef_Edot_YCbCr_to_RGB[0][1] *= 0
    coef_Edot_YCbCr_to_RGB[2][2] *= 0
    coef_Edot_YCbCr_to_RGB[1][1] *= (-1) * coef_Edot_RGB_to_Y[2] / coef_Edot_RGB_to_Y[1]
    coef_Edot_YCbCr_to_RGB[1][2] *= (-1) * coef_Edot_RGB_to_Y[0] / coef_Edot_RGB_to_Y[1]
    coef_Edot_YCbCr_to_RGB[::, 1] *= 2 * (1-coef_Edot_RGB_to_Y[2])
    coef_Edot_YCbCr_to_RGB[::, 2] *= 2 * (1-coef_Edot_RGB_to_Y[0])
    print(coef_Edot_YCbCr_to_RGB)

    coef_Ddot_YCbCr_to_RGB = coef_Edot_YCbCr_to_RGB.copy()
    coef_Ddot_YCbCr_to_RGB[:, 0] *= (high_rgb-low_rgb) / (high_y-low_yuv)
    coef_Ddot_YCbCr_to_RGB[:, 1:] *= (high_rgb-low_rgb) / (high_uv-low_yuv)
    print(coef_Ddot_YCbCr_to_RGB)

    if trend == "yuv2rgb":
        pass
    elif trend == "rgb2yuv":
        pass


trend = "rgb2yuv"
gamut = "bt709"
bit_depth_img = 8
bit_depth_coef = 8
range_rgb = "full"
range_yuv = "limited"

get_CSC_coefficient(trend, gamut, bit_depth_img, bit_depth_coef, range_rgb, range_yuv)
