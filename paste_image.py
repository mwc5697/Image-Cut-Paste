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

### rotate first image depends on row and column number ###
im = im.rotate(90, expand=True) if (r > c and not side(im)) or (r < c and side(im)) else im

#### rotate other images to have same width & height as first image ###
im_c = list(range(0, r*c-1))
for i in range(1, r*c):
	im_c[i-1] = Image.open(input_files[i])
	if side(im) != side(im_c[i-1]):
		im_c[i-1] = im_c[i-1].rotate(90, expand=True)

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
						order = i
						flip = True
						mirror = False if j!=k else True
						leftOrTop = True if k == 0 else False
						dif = eTECompare(lSide, mainSide, subSide[::-1])

					if dif > (eTECompare(lSide, mainSide, subSide)):
						order = i
						flip = False
						mirror = False if j!=k else True
						leftOrTop = True if k == 0 else False
						dif = eTECompare(lSide, mainSide, subSide)
				except:
					pass

	if not side(mainImage) and flip != mirror:
		flip = not flip
		mirror = not mirror

	return order, flip, mirror, leftOrTop, dif

### merge two images ###
def mergeImage(mainImage, subImage, leftOrTop, more):
	wm, hm = mainImage.size
	ws, hs = subImage.size

	sideYes = not side(mainImage) if more else side(mainImage)

	if sideYes and not leftOrTop: # right
		plate = Image.new('RGB', (wm+ws, hm))
		plate.paste(mainImage, (0,0))
		plate.paste(subImage, (wm,0))

	if sideYes and leftOrTop: # left
		plate = Image.new('RGB', (wm+ws, hm))
		plate.paste(mainImage, (ws,0))
		plate.paste(subImage, (0,0))

	if not sideYes and leftOrTop: # top
		plate = Image.new('RGB', (wm, hm+hs))
		plate.paste(mainImage, (0,hs))
		plate.paste(subImage, (0,0))

	if not sideYes and not leftOrTop: # bottom
		plate = Image.new('RGB', (wm, hm+hs))
		plate.paste(mainImage, (0,0))
		plate.paste(subImage, (0,hm))

	return plate


### check if merging two or three images and make merged image ###
def longImage(mainImage, others, rOrC, pOrF):
    
	info2 = nextImage(mainImage, others)
	others[info2[0]] = ImageOps.flip(others[info2[0]]) if info2[1] else others[info2[0]]
	others[info2[0]] = ImageOps.mirror(others[info2[0]]) if info2[2] else others[info2[0]]
	       
	im2 = others[info2[0]]
	others.remove(others[info2[0]])
	merge = mergeImage(mainImage, im2, info2[3], False)

	if rOrC > 2:
		a = nextImage(mainImage, others)
		b = nextImage(im2, others)
		info3 = a if a[4] < b[4] else b
		others[info3[0]] = ImageOps.flip(others[info3[0]]) if info3[1] else others[info3[0]]
		others[info3[0]] = ImageOps.mirror(others[info3[0]]) if info3[2] else others[info3[0]]
		       
		im3 = others[info3[0]]
		others.remove(others[info3[0]])
		merge = mergeImage(merge, im3, info3[3], pOrF)

	return merge, others

### find whether row or column is bigger ###
shortS = c if side(im) else r
longS = r if side(im) else c

### merge images to make long image ###
merged, im_rest = longImage(im, im_c, longS, True)

### merge other images to make second long image ###
mergedImages = []
merged2, im_rest = longImage(im_rest[0], im_rest[1:], longS, True)
mergedImages.append(merged2)

### merge other images to make third long image ###
if shortS > 2:
	merged3, im_rest = longImage(im_rest[0], im_rest[1:], longS, True)
	mergedImages.append(merged3)

### merge all merged images ###
full = longImage(merged, mergedImages, shortS, False)[0]
full.save('%s.jpg' % (name))
