import util.FileLocator as fl
import util.PropertyReader as pr
import module.Cr2Module as cr2
import module.ExifModule as exifmodule
import frames.FrameDetector as frames
import util.Logger as logger
import module.FilenameModule as asiair


def main():
    options = pr.read()
    logger.init(options['logging'])
    frames.init(logger)

    if not options['path']:
        images = fl.find_images_on_removable()
    else:
        images = fl.find_images_on_path()

    logger.write('Found ' + str(len(images)) + ' images')

    light_frames = []
    dark_frames = []
    bias_frames = []
    flat_frames = []

    for image in images:
        logger.write('Examining ' + image)
        exif = exifmodule.get_exif(image)
        black_pixels = 0
        white_pixels = 0

        if asiair.is_valid(image, options['pattern']):
            logger.write('Filename matching ASIAIR template - contains type')
            asiair.process(image, options)

        if cr2.is_valid(image):
            logger.write('Identified as CR2 canon RAW image')
            black_pixels, white_pixels = cr2.count_black_pixels(image, options['black_treshold'],
                                                                options['white_treshold'])
        if frames.is_bias_frame(exif['exposure']):
            logger.write('Identified as a bias frame')
            bias_frames.append(image)
        elif frames.is_dark_frame(black_pixels, exif['width'], exif['length'], options['dark_frames_treshold']):
            logger.write('Identified as a dark frame')
            dark_frames.append(image)
        elif frames.is_flat_frame(black_pixels, white_pixels, exif['width'], exif['length'],
                                  options['flat_frames_treshold']):
            logger.write('Identified as a flat frame')
            flat_frames.append(image)
        else:
            logger.write('Identifed as light frame')
            light_frames.append(image)

        logger.write('')
    print('stop')


if __name__ == '__main__':
    main()
