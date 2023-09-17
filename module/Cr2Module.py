import os

import rawpy


def init(options):
    global settings
    settings = options


def is_valid(file) -> bool:
    (filepath_no_ext, ext) = os.path.splitext(file)
    ext = ext.lower()
    return ext == '.cr2'


def count_black_pixels(file, black_pixel_treshold, white_pixel_treshold):
    if file is None:
        return

    raw = rawpy.imread(file)
    rgbs = raw.postprocess(use_camera_wb=True)
    rgbs = rgbs.astype('int32')
    number_of_black_pixels = 0
    number_of_white_pixels = 0
    for row in rgbs:
        for pixel in row:
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            average = (r + g + b) / 3
            if average < float(black_pixel_treshold):
                number_of_black_pixels += 1
            elif average > float(white_pixel_treshold):
                number_of_white_pixels += 1
    return number_of_black_pixels, number_of_white_pixels
