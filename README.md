# Image-Cut-Paste
Use Pillow to cut an image to several pieces &amp;  paste pieces to make original image

## Requirements

* image file
* shell script with Pillow Library - pip install Pillow

## Features

- write 'cut_image.py ${image_file_name} ${column_number}  ${row_number} ${prefix_output_filename}' on shell script

  - cut column x row number of images with input
  - put random number between 0 to column x row number on each images
  - rotating, fliping, mirroring images randomly(50% chance for each action)
  - create folder name with prefix output filename
  - save cut images inside the folder

For example, it will create 12 images when you write 'cut_image_py hana.jpeg 2 2 test' in folder name 'test' with prefix name + random number
