# AstroSort

## About
AstroSort is a python program specifically designed for organizing images for astrophotography.
It automatically sorts images into their respective subfolders.

## Features
- **Autoimport**: This program automatically searches for removable drives
- **Frame-Type detection**: Detects `light-frames`, `dark-frames`, `bias-frames` and `flat-frames`
- **CR2 Support**: Supports Canon-RAW format
- **ASIAIR Support**: If you setup your ASIAIR to include things like frame type, object, filter or date into your filenames, AstroSort can pick it up and sort it to your likings
- **Customizable**: Percentage threshold for black values for your dark-frames to low? Want to disable autoimport? See [configuration](configuration)

## Installation
1. Download and install python from [https://www.python.org/downloads](https://www.python.org/downloads)
2. install pip via `python -m ensurepip --upgrade` in your command line
2. Download this project
3. Open command shell and navigate to the downloaded code
4. Type `pip install -r requirements.txt` 
5. Run the program by typing `python astrosort.py` or by doubleclicking `astrosort.py` in your file explorer

## Configuration
The configuration is done via the `configuration.ini`

### [general]
General ection
- **path**: Tell the program to look for images in the given path. if you want to use autoimport, keep the value after the `=` empty
- **target**: Path, where your images should be stored. This is a mandatory value

### [frames]
This is a frames specific section where you can configure your values for your dark-frames, flat-frames etc.
- **black_treshold**: Treshold value for your black values. Black values are calculated by adding red, green and blue channels (value between 0-255) of an image and dividing by three. If the resulting image is lower then the configured value here, it counts as a "black pixel" 
- **dark_frame_treshold**: Threshold value for percentage of black pixels to count as a dark frame
- **flat_frame_treshold**: Threshold value for percentage fo black pixels to count as a flat frame