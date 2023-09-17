import exifread


def get_exif(image):
    dict = {}
    with open(image, 'rb') as f:
        exif = exifread.process_file(f)

        for key, value in exif.items():
            if key == "EXIF ExposureTime":
                exposure = value.values[0].numerator / value.values[0].denominator
                dict['exposure'] = exposure
            elif key == 'EXIF FNumber':
                dict['fnumber'] = value.values[0].numerator / value.values[0].denominator
            elif key == 'EXIF ISOSpeedRatings':
                dict['iso'] = value.values[0].numerator / value.values[0].denominator
            elif key == 'EXIF FocalLength':
                dict['focallength'] = value.values[0].numerator / value.values[0].denominator
            elif key == 'Image ImageWidth':
                dict['width'] = value.values[0]
            elif key == 'Image ImageLength':
                dict['length'] = value.values[0]
            elif key == 'Image DateTime':
                dict['datetime'] = value.values[0]
    return dict
