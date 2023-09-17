import os.path
import re
import shutil

regex = r'\}(.*?)\{'

actions_metadata = {
    '{TYPE}': lambda metadata, value: metadata.update({'type': value}),
    '{OBJECT}': lambda metadata, value: metadata.update({'object': value}),
    '{EXPOSURE_TIME}': lambda metadata, value: metadata.update({'exposure_time': value}),
    '{BINNING}': lambda metadata, value: metadata.update({'binning': value}),
    '{FILTER}': lambda metadata, value: metadata.update({'filter': value}),
    '{GAIN}': lambda metadata, value: metadata.update({'gain': value}),
    '{DATE_TIME}': lambda metadata, value: metadata.update({'date_time': value}),
    '{TEMPERATURE}': lambda metadata, value: metadata.update({'temperature': value}),
    '{IMAGE_NUMBER}': lambda metadata, value: metadata.update({'image_number': value}),
}

actions_filename = {
    '{TYPE}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['type']),
    '{OBJECT}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['object']),
    '{EXPOSURE_TIME}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['exposure']),
    '{BINNING}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['binning']),
    '{FILTER}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['filter']),
    '{GAIN}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['gain']),
    '{DATE_TIME}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['date_time']),
    '{TEMPERATURE}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['temperature']),
    '{IMAGE_NUMBER}': lambda target_dir, key, metadata: target_dir.replace(key, metadata['image_number']),
}

global seperator


def is_valid(image, pattern):
    _get_seperator(pattern)
    if seperator is not None:
        filename = os.path.basename(image)
        entries = filename.split(seperator)

        return 'Light' in entries
    return False


def _get_seperator(pattern):
    matches = re.findall(regex, pattern)
    if matches:
        global seperator
        seperator = matches[0]


def process(image, settings):
    pattern = settings['pattern']
    _get_seperator(pattern)
    filename = os.path.basename(image)
    filename_components = filename.split(seperator)
    template_components = pattern.split('}' + seperator + '{')

    if len(filename_components) != len(template_components):
        return

    metadata = _get_metadata(filename, filename_components, template_components)
    target_dir = settings['target_dir_pattern']
    target_dir = target_dir.replace('{TARGET}', settings['target'])
    target_dir = _sanitize_path(target_dir)
    target_dir = _get_filename(target_dir, metadata)
    shutil.copy(image, os.path.join(target_dir, filename))


def _sanitize_path(local_path):
    if '/' in local_path and '/' is not os.path.sep:
        return local_path.replace('/', os.path.sep)
    elif '\\' in local_path and '\\' is not os.path.sep:
        return local_path.replace('\\', os.path.sep)


def _get_filename(target_dir, metadata):
    filename_components = _split_by_path_seperator(target_dir)

    for key in filename_components:
        if '{' in key:
            target_dir = actions_filename[key](target_dir, key, metadata)
    return target_dir


def _split_by_path_seperator(target_dir):
    if '/' in target_dir:
        return target_dir.split('/')
    elif '\\' in target_dir:
        return target_dir.split('\\')
    return []


def _get_metadata(filename, filename_components, template_components) -> dict[str, str]:
    metadata = {'file': filename}

    for index in range(len(template_components)):
        key = template_components[index]
        if not key.startswith('{'):
            key = '{' + key
        if not key.endswith('}'):
            key = key + '}'
        actions_metadata[key](metadata, filename_components[index])

    return metadata
