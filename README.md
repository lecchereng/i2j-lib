# i2j-lib
Image 2 Json library module stands alone from other external modules of Python core.
Feel free to include and use it in your python project.

The 'objects' file contains two definitions used internally to manage image file metadata like name and mime-type as well as image content.

The 'utils' file contains two methods:
* images_2_json_list: converting a list of binary images (but not only) into a JSON array with binary data converted in base64
* insert_at_path: adding or replacing the image json array into a specific path of the provided json document.

The path parameter admits these formats:
* path/to/element
* path/to/"array[index]
* path/to/element[field=value] <-- value with no ""
* path/to/element/array[index]/key
* path/to/element/array[field=value]/key
* path/to/key[index]/key[field=value]/key <-- value with no ""

You can see an example of how to use the lib in how2lib.py

A simple script to harvest random images is provided in downlaod_random_image.py

This software is developed and tested using 3.12 version of Python
I suggest using venev.
