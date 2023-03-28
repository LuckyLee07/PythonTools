# -*- coding: UTF-8 -*-
import os
import re
import json
import shutil
from PIL import Image


re_tex0 = re.compile(r'<\w*Texture.+/>') #只针对单行
re_tex1 = re.compile(r'[^\n]*<(\w*Texture).+?</\1>', re.DOTALL)
def parse_xml_file(base_path):
	all_result = []
	for (root, dirs, files) in os.walk(base_path):
		if root.find('universe') !=-1: continue #过滤海外的
		files = [f for f in files if f.endswith('.xml')]

		for file in files: #遍历读取xml文件
			filepath = os.path.join(root, file)
			with open(filepath, 'r', encoding='utf-8') as reader:
				content = reader.read();
				content = re_tex0.sub('', content)
				for tex_match in re_tex1.finditer(content):
					str_tex = tex_match.group()
					if str_tex.find('<UVAnimation') != -1:
						all_result.append(str_tex)

	return all_result


re_anim = re.compile(r'<UVAnimation\s+texrows="(?P<texrows>\d+)"\s+texcols="(?P<texcols>\d+)"\s*/>')
re_file = re.compile(r'<(?P<type>\w*Texture)\s+name="(?P<name>[^"]+)"\s+file="(?P<file>[^"]+)"\s*(?P<abs_x>abs_x="\d+")?\s*(?P<abs_y>abs_y="\d+")?.*>*')

def parse_tex_str(tex_str, index):
	result1 = re_anim.search(tex_str)
	result2 = re_file.search(tex_str)
	if not result1 or not result2: return

	ctype = result2.group('type')
	cname = result2.group('name')
	cfile = result2.group('file')
	tex_obj = {'type':ctype, 'name':'name', 'file':cfile}

	tex_obj['abs_x'] = result2.group('abs_x')
	tex_obj['abs_y'] = result2.group('abs_y')
	tex_obj['texrows'] = int(result1.group('texrows'))
	tex_obj['texcols'] = int(result1.group('texcols'))
	return tex_obj


def split_image(texfile, texrows, texcols, splitFlag=False):
	dir_, file = os.path.split(texfile)
	new_dir = file.replace('.png', '')
	new_dir = os.path.join('animation',new_dir)
	if not os.path.exists(new_dir):
		os.mkdir(new_dir)
	texfile = os.path.join(res_path, texfile)

	cImage = Image.open(texfile)
	image_width = cImage.size[0]
	image_height = cImage.size[1]
	c_width = image_width//texcols
	c_height = image_height//texrows

	frames = {}
	for row in range(texrows):
		for col in range(texcols):
			posx = col * c_width 
			posy = row * c_height
			if splitFlag: #切成小图
				crop_box = (posx, posy, posx+c_width, posy+c_height)
				crop_image = cImage.crop(crop_box)
				crop_image.save(f'{new_dir}/c_{row}_{col}.png')
			frame_obj = {'x':posx, 'y':posy, 'w':c_width, 'h':c_height, 'offX':0, 'offY':0}
			frame_obj['sourceW'] = image_width
			frame_obj['sourceH'] = image_height
			frames[f'c_{row}_{col}.png'] = frame_obj

	return {'file':file, 'frames':frames}


res_path = r'G:\env1_trunk\bin_externel\res'

if __name__ == '__main__':
	all_files = {}
	results = parse_xml_file(res_path)
	for index, tex_str in enumerate(results):
		result = parse_tex_str(tex_str, index+1)
		if not result: 
			#print(tex_str, '\n')
			continue
		file_path = result['file']
		if file_path.find('.xml') != -1:
			#print(tex_str, '\n')
			continue 

		t_row, t_col = result['texrows'], result['texcols']
		texture = all_files.get(file_path)
		if not texture: 
			all_files[file_path] = {'texrows':t_row, 'texcols':t_col}

	if not os.path.exists('animation'):
		os.mkdir('animation')

	index = 0
	json_data = []
	for file, row_col in all_files.items():
		index += 1
		src_file = os.path.join(res_path, file)
		dir_, file_name = os.path.split(file)
		dst_file = os.path.join('animation', file_name)
		if not os.path.exists(src_file): 
			print('NotFind=======>>>', index, file, texrows, texcols)
			continue
		texrows = row_col['texrows']
		texcols = row_col['texcols']
		#shutil.copyfile(src_file, dst_file)
		result = split_image(file, texrows, texcols)
		json_data.append(result)
		#print('Fxkk=========>>>', index, file, texrows,texcols)
	
	with open('json_data.json', 'w', encoding='utf-8') as wtf:
		wtf.write(json.dumps(json_data, indent=4))