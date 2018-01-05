__author__ = "bythew3i"

from PIL import Image, ImageDraw
from math import sqrt

PLAYERCOLOR = (56, 59, 102) # player color reference
PCOLORAPPR = 5 # player color approximation (tryin to find the pixel whose color distance with PLAYERCOLR is less than this value)
BCOLORDIFF = 30 # board color difference (calculate the color distance of a pixel and background color, if greater than this value, we consider this pixel is from board)
BCOLORAPPR = 5 # board color approximation (After finding topmost board pixel, use it to find the rightmost pixel by calling "isCloseColor" function with this value)

def aimTarget(im, tx, ty, color=33):
	imw = im.size[0] # width
	imh = im.size[1] # height
	draw = ImageDraw.Draw(im)
	draw.line((0, ty, imw-1, ty), fill=color)
	draw.line((tx, 0, tx, imh-1), fill=color)
	del draw

def colorDistance(c1, c2):
	return sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2)

def isCloseColor(c1, c2, ref):
	return -ref < c1[0]-c2[0] < ref \
		and -ref < c1[1]-c2[1] < ref \
		and -ref < c1[2]-c2[2] < ref

def setFrame(im, color=200):
	imw = im.size[0] # width
	imh = im.size[1] # height
	draw = ImageDraw.Draw(im)
	# draw.line((0, imh//2, imw-1, imh//2), fill=color)
	draw.line((imw//2, 0, imw//2, imh-1), fill=color)
	draw.line((0, imh//3, imw-1, imh//3), fill=color)
	draw.line((0, imh*2//3, imw-1, imh*2//3), fill=color)
	del draw

def findPlayer(im):
	offsetX = 5
	offsetY = -10
	imw = im.size[0]
	imh = im.size[1]
	for y in range(imh*2//3, imh//2, -1):
		for x in range(imw):
			cur = im.getpixel((x, y))
			if colorDistance(cur, PLAYERCOLOR) <= PCOLORAPPR:
				return x+offsetX, y+offsetY
	return None


def findBoard(im, right=True): # only search left half
	offsetY = 3
	boardColor = None
	topX = None

	imw = im.size[0]
	imh = im.size[1]

	xfrm, xto = imw//2, 0
	if right:
		xfrm, xto = imw-1, imw//2
	# find the top and board color
	for y in range(int(imh/3), int(imh/2)):
		preColor = im.getpixel((xto, y))
		for x in range(xfrm, xto, -1):
			curColor = im.getpixel((x, y))
			if colorDistance(curColor, preColor) > BCOLORDIFF:
				# return x, y
				topX = x
				boardColor = im.getpixel((x, y+offsetY))
				break
		if boardColor!=None:
			break

	# find left/right edge
	for x in range(imw-1, 0, -1):
		for y in range(int(imh/3), int(imh/2)):
			curColor = im.getpixel((x, y))
			if isCloseColor(curColor, boardColor, BCOLORAPPR):
				return topX, y

	return None

for i in range(19):
	im = Image.open("img_data/screenshot{}.png".format(i+1))
	# 750 x 1334
	tx, ty = findPlayer(im)
	bx, by = findBoard(im, tx < im.size[0]//2) ## check the next board location
	# print(bx, by)
	# setFrame(im) ## draw the frame
	aimTarget(im, tx, ty)
	aimTarget(im, bx, by, 200)

	im.save("research/sample{}.png".format(i+1))
