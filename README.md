nutils
======

small console utils

Depencies
======

Python 2.7
https://www.python.org/downloads/

PIL for Python 2.7
http://www.pythonware.com/products/pil/

png_to_jpgpng.py
======
Converting PNG to JPEG with PNG alphachannel mask

How to use
Just convert
python png_to_jpg_gif.py -i d:/project/static/assets/my_super_assets
default quality 85

Convert and delete
python png_to_jpg_gif.py -i d:/project/static/assets/my_super_assets -r True
WARNING! If you write False it will delete it anyway

Convert with custom quality
python png_to_jpg_gif.py -i d:/project/static/assets/my_super_assets -q 85
Quality is integer between 0 and 100