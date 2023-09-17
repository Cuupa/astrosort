def init(log):
    global logger
    logger = log


def is_bias_frame(exposure_time):
    is_bias = exposure_time < 0.0025
    logger.write('BIAS FRAME: ' + str(is_bias))
    if is_bias:
        logger.write(str(exposure_time) + ' < 0.0025')
    else:
        logger.write(str(exposure_time) + ' > 0.0025')
    return is_bias


def is_dark_frame(number_of_black_pixels, width, length, dark_frames_treshold):
    black_percentage = (number_of_black_pixels / (width * length)) * 100
    is_dark = black_percentage > float(dark_frames_treshold)
    logger.write('DARK FRAME: ' + str(is_dark))
    logger.write('Percentage of black pixel: ' + str(black_percentage))
    logger.write('Treshold: ' + str(dark_frames_treshold))
    return is_dark


def is_flat_frame(number_of_black_pixels, number_of_white_pixels, width, length, flat_frames_treshold):
    black_percentage = (number_of_black_pixels / (width * length)) * 100
    white_percentage = (number_of_white_pixels / (width * length)) * 100
    is_flat = black_percentage < float(flat_frames_treshold)
    logger.write('FLAT FRAME: ' + str(is_flat))
    logger.write('Percentage of black pixel: ' + str(black_percentage))
    logger.write('Percentage of white pixel: ' + str(white_percentage))
    logger.write('Treshold: ' + str(flat_frames_treshold))
    return is_flat
