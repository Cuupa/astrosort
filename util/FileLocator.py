import os
import platform
import re

CANON_RAW = '.cr2'


def find_images_on_removable():
    operating_system = platform.system()

    removables = []
    if operating_system == 'Windows':
        removables = _find_removable_windows()
    images_location = _search_for_images(removables)
    return _list_images(images_location)


def _list_images(location):
    if location is None:
        return []
    image_files = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if str(file).lower().endswith(CANON_RAW):
                absolute_path = os.path.abspath((os.path.join(root, file)))
                image_files.append(absolute_path)
    return image_files


def _search_for_images(removables) -> str | None:
    for drive in removables:
        fixed_drive = drive + ':'
        dir_content = _try_get_dir_content(fixed_drive)
        dirs = []
        for dir in dir_content:
            full_path = os.path.join(fixed_drive, dir)
            if os.path.isdir(full_path):
                dirs.append(full_path)

        if _check_canon(dirs):
            return fixed_drive
    return None


def _try_get_dir_content(dir):
    try:
        return os.listdir(dir)
    except PermissionError as pe:
        return []


def _check_canon(dirs) -> bool:
    for dir in dirs:
        if dir.endswith('DCIM'):
            return True
    return False
    '''
    regex = '([1-9]?[0-9]{2})EOS[1-9]{1}[0-9]{0,2}D'
    for dir in dirs:
        found = re.search(regex, dir)
        if found:
            return True
    return False
    '''


def _find_removable_windows() -> list[str]:
    from ctypes import windll
    import string
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def find_images_on_path():
    return None