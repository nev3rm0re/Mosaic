#!/usr/bin/python
import sys
import random
import os

import MySQLdb, MySQLdb.cursors
from PIL import Image

mask_image = "bg/mask.png"
bg_image = "bg/real-image.png"
output_filename = "result.png"
tiles_dir = "proto/uniform"

tile_size = (85, 85)
image_limit = 430 # no limit, was: 350

def get_cursor():
	conn = MySQLdb.connect(
		host="localhost",
		user="sandbox", 
		passwd="sandbox", 
		db="sandbox",
		cursorclass=MySQLdb.cursors.DictCursor
	)
	
	return conn.cursor()

def save_coords(id, coords):
	get_cursor().execute(
		"UPDATE fitmeimages SET x = %d, y = %d WHERE id = %d" % (coords + (id, )))
	

def get_tiles():
	"""
	Fetches uploaded images from the database and returns an 
	array of dicts: {id:, filename:, shade:, x:, y: }
	"""
		
	cursor = get_cursor()
	
	cursor.execute("SELECT * FROM fitmeimages ORDER BY shade ASC, id ASC")
	return cursor.fetchall();
	
def cell_is_usable(cell):
	"""
	Analyze colors in cell and return true if an image 
	can be placed here
	"""
	maxcolors = tile_size[0] * tile_size[1]
	colors = cell.getcolors(maxcolors)
	
	is_usable = False
	
	for color in colors:	
		if color[1][3] == 255 and color[0] >= 0:
			is_usable = True
			break
			
	return is_usable

def main():
	image = Image.open(mask_image)
	
	width = image.size[0] / tile_size[0]
	height = image.size[1] / tile_size[1]
	
	thumbnail_count = 0

	tiles = get_tiles()
			
	output = Image.open(bg_image)
	
	for x in range(width):
		for y in range(height):
			cell = image.crop((x * tile_size[0], y * tile_size[1], 
								( x + 1 ) * tile_size[0],
								( y + 1 ) * tile_size[1]))
								
			if (cell_is_usable(cell)):
				thumbnail_count += 1
				
				if image_limit == 0 or thumbnail_count < image_limit:
					tile_to_paste = random.choice(tiles)
					tile = Image.open(os.path.join(tiles_dir, tile_to_paste["filename"]))
					output.paste(tile, (x * tile_size[0], y * tile_size[1]))
					save_coords(tile_to_paste["id"], (x * tile_size[0], y*tile_size[1]))
		
	output.save(output_filename)
	
	print "width: %s; height: %s" % (str(width), str(height))
	print "%d thumbnails will fit" % thumbnail_count

if __name__ == "__main__":
	main()

