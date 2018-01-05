
from math import sqrt
import wda
from PIL import Image, ImageDraw
import time

MAGICNUM = 0.0019
PLAYERCOLOR = (56, 59, 102) # player standard color
PCOLORAPPR = 5 # max color approximation
BCOLORDIFF = 30 # min border color difference
BCOLORAPPR = 5

def colorDistance(c1, c2):
	return sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2)

def phyDistance(x1, y1, x2, y2):
	return sqrt((x1-x2)**2 + (y1-y2)**2)

def isCloseColor(c1, c2, ref):
	return -ref < c1[0]-c2[0] < ref \
		and -ref < c1[1]-c2[1] < ref \
		and -ref < c1[2]-c2[2] < ref

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


def getDistance(path):
	im = Image.open(path)
	# 750 x 1334
	tx, ty = findPlayer(im)
	bx, by = findBoard(im, tx < im.size[0]//2) ## check the next board location
	return phyDistance(tx, ty, bx, by)


def main():	
	tapX = 50
	tapY = 50
	path = 'buffer/resource.png'
	wait = 2

	c = wda.Client()
	s =  c.session()

	while True:
		c.screenshot(path)
		t = getDistance(path)*MAGICNUM
		# print(t)
		s.tap_hold(tapX, tapY, t) # tap element
		time.sleep(wait)
	

main()

