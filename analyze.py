#!/usr/bin/python
import sys
import random
import os

import argparse

from PIL import Image
import MySQLdb

from create_mosaic import cell_is_usable

mask_image = "bg/mask.png"
bg_image = "bg/real-image.png"
output_filename = "result.png"
tiles_dir = "proto/uniform"

tile_size = (85, 85)
image_limit = 0 # no limit, was: 350

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('--tile-size', type=int, help="tile size to analyze")
	args = parser.parse_args()
	
	if (args.tile_size):
		analyze((args.tile_size, args.tile_size))
	else: 
		for x in range(25, 101):
			tile_size = (x,x)
			analyze(tile_size)
	
def analyze(tile_size):
	image = Image.open(mask_image)
	
	width = image.size[0] / tile_size[0]
	height = image.size[1] / tile_size[1]
	
	thumbnail_count = 0

	tiles = os.listdir(os.path.join(os.path.dirname(sys.argv[0]), tiles_dir))
			
	output = Image.open(bg_image)
	
	for y in range(height):
		for x in range(width):
			cell = image.crop((x * tile_size[0], y * tile_size[1], 
								( x + 1 ) * tile_size[0],
								( y + 1 ) * tile_size[1]))
								
			if (cell_is_usable(cell)): 
				thumbnail_count += 1
	
	print "tile size: %dx%d" % tile_size, 
	print ". thumbnails: %d" % (thumbnail_count)

if __name__ == "__main__":
	main(sys.argv)

