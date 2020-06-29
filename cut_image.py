# Importing sys, PIL, random, os module 
import sys
from PIL import Image, ImageOps
import random
import os

# Input
input_file = str(sys.argv[1])
column = int(sys.argv[2])
row = int(sys.argv[3])
prefix = str(sys.argv[4])

im = Image.open(input_file) 
width, height = im.size

# resize the image
if width == height:
	height -= column
	
while width%row:
    width -= 1

while height%column:
    height -= 1

im_re = im.crop((0,0,width,height))

# Save Chops of original image(rotate, flip, mirror)
chopWidth = int(width/row)
chopHeight = int(height/column)

if not os.path.exists(prefix):
	os.mkdir(prefix)

r = list(range(0, column*row))
for x0 in range(0, width, chopWidth):
    for y0 in range(0, height, chopHeight):
    	try:
    		box = (x0, y0,
    			x0+chopWidth if x0+chopWidth <  width else width,
    			y0+chopHeight if y0+chopHeight < height else height)
    		#print('%s %s' % ('output', box))
    		boxImage = im_re.crop(box)
    		boxImage = boxImage.rotate(90, expand=True) if random.choice([True, False]) else boxImage
    		boxImage = ImageOps.flip(boxImage) if random.choice([True, False]) else boxImage
    		boxImage = ImageOps.mirror(boxImage) if random.choice([True, False]) else boxImage

    		num = random.choice(r)
    		r.remove(num)
    		boxImage.save('%s/%s%d.jpg' % (prefix, prefix.replace('.jpg',''), num))
    	except:
    		pass