from PIL import Image
import rasterio
import numpy as np
from glob import glob
import os
import gdal

data_dir = '/Users/mm_shane/Downloads/data/'
file_list = sorted(os.listdir(data_dir))
file_list = np.unique(file_list)  # duplicate files??


def read_file(file):
    im = Image.open(file)
    return np.array(im)


# since it's sorted, group the a and b together
# http://book.pythontips.com/en/latest/enumerate.html
groups = []

# for each index number and filename in the list
for counter, fname in enumerate(file_list):
    # if we're on an "a." item only
    if "a." in fname:
        afile = file_list[counter]  # starts at 0
        bfile = file_list[counter + 1]  # starts at 0
        entiremonth = [afile, bfile]
        groups.append(entiremonth)

# def setBigNumsZero(arr):
#     for idx, i in enumerate(arr):
#         if i < -2.0e20:
#             arr[idx] = -1
#     return arr

for x in groups:
    a_data = read_file(data_dir + x[0])
    b_data = read_file(data_dir + x[1])

    combine = (a_data + b_data) / 2 # average the entire month

    # for whatever reason, there's huuuuge negative numbers in here, so i set them to zero
    # combine = setBigNumsZero(combine)

    newname = x[0].replace("a.", "")

    # sanity check
    if x[1].replace("b.", "") != newname:
        print('crap what happened here?')
        print(x[0])
        print(x[1])

    # doesn't work
    # from: https://stackoverflow.com/questions/37648439/simplest-way-to-save-array-into-raster-file-in-python
    dst_filename = "/Users/mm_shane/arcgis/tifavg/output/" + newname
    x_pixels = combine.shape[0]  # number of pixels in x
    y_pixels = combine.shape[1]  # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filename, x_pixels, y_pixels, 1, gdal.GDT_Float32)
    dataset.GetRasterBand(1).WriteArray(combine)

    #     Shanes-MacBook-Pro-6:tifavg mm_shane$ python combineparts.py
    # combineparts.py:41: RuntimeWarning: overflow encountered in add
    #   combine = (a_data + b_data) / 2 # average the entire month
    # ERROR 4: Attempt to create new tiff file `/Users/mm_shane/arcgis/tifavg/output/geo00apr15n14-VI3g.tif' failed: No such file or directory
    # Traceback (most recent call last):
    #   File "combineparts.py", line 61, in <module>
    #     dataset.GetRasterBand(1).WriteArray(combine)
    # AttributeError: 'NoneType' object has no attribute 'GetRasterBand'


#
