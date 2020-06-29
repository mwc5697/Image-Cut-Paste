# Importing sys, PIL,random module 
import sys
from PIL import Image, ImageOps
import random
import os
from operator import sub

### Input ###
input_folder = str(sys.argv[1])
c = int(sys.argv[2])
r = int(sys.argv[3])
name = str(sys.argv[4])

input_files = [(os.path.join(input_folder,i)) for i in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder,i)) and input_folder in i]

### first image ###
im = Image.open(input_files[0])

### check if height is larger than width(paste image on left or right) ###
def side(image):
	w, h = image.size
	isSide = True if h > w else False
	return isSide

#### rotate other images to have same width & height as first image ###
im_c = list(range(0, r*c-1))
for i in range(1, r*c):
	im_c[i-1] = Image.open(input_files[i])
	if side(im) != side(im_c[i-1]):
		im_c[i-1] = im_c[i-1].rotate(90, expand=True)

#im_c[0].show()
#im_c[1].show()
#im_c[2].show()

### get list of pixel value on one edge ###
def pixelInfo(image, length, isSide, start):
	pixelList = []
	for i in range(0,length):
		if isSide: #left or right
			pixelList.append(image.getpixel((start,i)))
		else: #top or bottom
			pixelList.append(image.getpixel((i,start)))
	return pixelList

### edge to edge comparison value ###
def eTECompare(length, edge1, edge2):
	compare = []
	for i in range(0,length):
		compare.append(tuple(map(lambda x, y: abs(x - y), edge1[i], edge2[i])))
		val = sum([x+y+z for (x,y,z) in compare])
	return val if val > 100 else float('inf')

### find nextImage's info ###
def nextImage(mainImage, others):
	w, h = mainImage.size
	lSide = h if side(mainImage) else w
	sSide = w if side(mainImage) else h

	dif = float('inf')
	order = 0
	leftOrTop = False
	flip = False
	mirror = False

	for i in range(len(others)):
		for j in range(0, sSide, sSide-1):
			for k in range(0, sSide, sSide-1):
				mainSide = pixelInfo(mainImage, lSide, side(mainImage), k)
				subSide = pixelInfo(others[i], lSide, side(others[i]), j)
				try:
					if dif > (eTECompare(lSide, mainSide, subSide[::-1])):
						#print(eTECompare(length, mainSide, subSide[::-1]))
						#print(i,j,k)
						order = i
						flip = True
						mirror = False if j!=k else True
						#print(k)
						leftOrTop = True if k == 0 else False
						dif = eTECompare(lSide, mainSide, subSide[::-1])

					if dif > (eTECompare(lSide, mainSide, subSide)):
						#print(eTECompare(length, mainSide, subSide))
						#print(i,j,k)
						order = i
						flip = False
						#print(k)
						mirror = False if j!=k else True
						leftOrTop = True if k == 0 else False
						dif = eTECompare(lSide, mainSide, subSide)
				except:
					pass

	if not side(mainImage) and flip != mirror:
		flip = not flip
		mirror = not mirror

	return order, flip, mirror, leftOrTop

### merge two images ###
def mergeImage(mainImage, subImage, leftOrTop):
	wm, hm = mainImage.size
	ws, hs = subImage.size

	#print(side(mainImage))
	#print(leftOrTop)
	if side(mainImage) and not leftOrTop: # right
		plate = Image.new('RGB', (wm+ws, hm))
		plate.paste(mainImage, (0,0))
		plate.paste(subImage, (wm,0))

	if side(mainImage) and leftOrTop: # left
		plate = Image.new('RGB', (wm+ws, hm))
		plate.paste(mainImage, (wm,0))
		plate.paste(subImage, (0,0))

	if not side(mainImage) and leftOrTop: # top
		plate = Image.new('RGB', (wm, hm+hs))
		plate.paste(mainImage, (0,hm))
		plate.paste(subImage, (0,0))
	  
	if not side(mainImage) and not leftOrTop: # bottom
		plate = Image.new('RGB', (wm, hm+hs))
		plate.paste(mainImage, (0,0))
		plate.paste(subImage, (0,hm))

	return plate

### get information of second image ###
num, flip, mirror, leftOrTop = nextImage(im, im_c)
#print(nextImage(im, im_c))

### change second image ###
im_c[num] = ImageOps.flip(im_c[num]) if flip else im_c[num]
im_c[num] = ImageOps.mirror(im_c[num]) if mirror else im_c[num]

### create first merge image ###
a = mergeImage(im, im_c[num], leftOrTop)

### create second merge image ###
im_c.remove(im_c[num])
num2, flip2, mirror2, leftOrTop2 = nextImage(im_c[0], im_c[1:])
#print(flip2, mirror2, leftOrTop2)
im_c[num2+1] = ImageOps.flip(im_c[num2+1]) if flip2 else im_c[num2+1]
im_c[num2+1] = ImageOps.mirror(im_c[num2+1]) if mirror2 else im_c[num2+1]

b = mergeImage(im_c[0], im_c[num2+1], leftOrTop2)

### merge two created image ###
numA, flipA, mirrorA, leftOrTopA = nextImage(a, [b])
#print(flipA, mirrorA, leftOrTopA)
b = ImageOps.flip(b) if flipA else b
b = ImageOps.mirror(b) if mirrorA else b

### save 2x2 image file with given name ###
mergeImage(a, b, leftOrTopA).save('%s.jpg' % (name))
