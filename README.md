## Generate_sprites

Extracts PNG sprites from SkypeResources.dll(lib where smileys are) that look like smileys: height % width == 0, height // width > 6. Generates .css file with animation classes. Generates .html file showing extracted sprites.

## Usage

Put SkypeResources.dll into directory where generate_sprites.py is

``` bash
python3 generate_sprites.py
```

PNG sprites are in sprites/ folder

CSS file with classes is skype_sprites.css

HTML file showing extracted sprites is example.html

## Dependancies

Pillow

pefile.py. Version 2016.3.28 taken from [repo](https://github.com/erocarrera/pefile) and modified to remove hardcoded MAX_ALLOWED_ENTRIES check

## Notes

Tested with:

Pillow==3.4.2

pefile.py==2016.3.28

SkypeResources.dll FileVersion: 7.29.66.102

4.4.0-38-generic GNU/Linux
