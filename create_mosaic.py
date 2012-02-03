#!/usr/bin/python
import sys
import random
import os

from PIL import Image

mask_image = "bg/mask.png"
bg_image = "bg/real-image.png"
output_filename = "result.png"
tiles_dir = "proto/uniform"

tile_size = (85, 85)
image_limit = 0 # no limit, was: 350

def main():
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
								
			maxcolors = tile_size[0] * tile_size[1]
			colors = cell.getcolors(tile_size[0] * tile_size[1])
			
			avg_r = 0
			avg_g = 0
			avg_b = 0
			
			toprint = " "
			
			for color in colors:	
				avg_r += color[1][0] * color[0]
				avg_g += color[1][1] * color[0]
				avg_b += color[1][2] * color[0]
				
				if color[1][3] == 255 and color[0] >= 0:
					toprint = "w"
					break

			if (toprint == "w"):
				thumbnail_count += 1
				
				if image_limit == 0 or thumbnail_count < image_limit:
					tile_to_paste = random.choice(tiles)
					tile = Image.open(os.path.join(tiles_dir, tile_to_paste))
					output.paste(tile, (x * tile_size[0], y * tile_size[1]))
				
			# sys.stdout.write(toprint)
			
			avg_r /= maxcolors
			avg_g /= maxcolors
			avg_b /= maxcolors
			
		#print ""
		
	output.save(output_filename)
	
	print "width: %s; height: %s" % (str(width), str(height))
	print "%d thumbnails will fit" % thumbnail_count

if __name__ == "__main__":
	main()

