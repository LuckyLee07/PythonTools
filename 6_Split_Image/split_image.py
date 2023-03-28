# -*- coding: UTF-8 -*-
import os
import re
import sys
import shutil
from PIL import Image


def split_image(texfile, texrows, texcols):
	__, file = os.path.split(texfile)
	new_dir = file.replace('.png', '')
	if not os.path.exists(new_dir):
		os.mkdir(new_dir)

	cImage = Image.open(texfile)
	image_width = cImage.size[0]
	image_height = cImage.size[1]

	c_width = image_width//texcols
	c_height = image_height//texrows

	for row in range(texrows):
		for col in range(texcols):
			posx, posy = col * c_width, row * c_height
			crop_box = (posx, posy, posx+c_width, posy+c_height)
			crop_image = cImage.crop(crop_box)
			crop_image.save(f'{new_dir}/c_{row}_{col}.png')



re_gex = re.compile(r'(\d+)\s+(\d+)\s+([^\s]+)')
if __name__ == '__main__':
	file_path = 'file_list.txt'
	if len(sys.argv) > 1: 
		file_path = sys.argv[1].strip()
	if not os.path.exists(file_path):
		print('Fxkk========>>file:%s not found!!'%file_path)

	with open(file_path, 'r', encoding='utf-8') as reader:
		all_lines = reader.read().split('\n')
		for index, curline in enumerate(all_lines):
			if not curline.strip(): continue

			result = re_gex.search(curline)
			if not result:
				print('Fxkk=======>>format error!! line:%d'%(index+1))
				continue
			file_path = result.group(3)
			if not os.path.exists(file_path):
				err_info = 'line:%d, file:%s'%(index+1, file_path)
				print('Fxkk========>>file not found!!', err_info)
				continue

			texrows = int(result.group(1))
			texcols = int(result.group(2))
			
			split_image(file_path, texrows, texcols)
	#os.system('pause')
