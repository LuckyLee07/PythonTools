import os
import re
import sys
import time
import requests

base_url = 'http://139.159.148.246:1128/'
search_params = 'search?types=[%s]&searchTextValues=[%%22%s%%22]'

headers = {
	'Host': '139.159.148.246:1128',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

def old_index_html(index_html):
	with open(index_html, 'r', encoding='utf-8') as reader:
		html_content = reader.read()
		new_str = '<a href=\'' + base_url
		new_content = re.sub(r'<a href=\'', new_str, html_content)

		new_index = index_html.replace('.h', '_1.h')
		with open(new_index, 'w', encoding='utf-8') as wtf:
			wtf.write(new_content); wtf.flush()


def get_dump_text(dump_obj, file_path, index):
	if os.path.exists(file_path): return True

	new_requrl = base_url + dump_obj['dumpId']
	try:
		req_obj = requests.get(new_requrl, headers=headers)
	except Exception as e: 
		print("Fxkk========>>> %d err:", index, file_path)
		return False
	else:
		print("Fxkk========>>> %d ok-:", index, file_path)
	
	resp_html = req_obj.content.decode('utf-8')
	with open(file_path, 'w', encoding='utf-8') as wtf:
		wtf.write(resp_html); wtf.flush()
	time.sleep(0.1)
	return True


def get_dump_list(s_content, s_type, force_update=False):
	file_path = 'index.html'
	if not os.path.exists(file_path) or force_update:
		new_requrl = base_url
		if s_content:
			new_params = search_params%(s_type, s_content)
			new_requrl = base_url + new_params

		req_obj = requests.get(new_requrl, headers=headers)
		resp_html = req_obj.content.decode('utf-8')
		time.sleep(0.1)
		with open(file_path, 'w', encoding='utf-8') as wtf:
			wtf.write(resp_html); wtf.flush()
	else:
		with open(file_path, 'r', encoding='utf-8') as reader:
			resp_html = reader.read()

	result_dumps = []
	dump_list = re.findall(r'<ol>(.+?)</ol>', resp_html, re.M|re.S)
	if len(dump_list) == 0:
		print('Fxkk ===>> 堆栈列表为空，查询字段为：%d_%s'%(s_type, s_content))
		return result_dumps
	
	dump_datas = re.findall(r'<li>\s+(.+?)</li>', dump_list[0], re.M|re.S)
	for dump_data in dump_datas:
		dump_text = dump_data.split('\n')[0]
		ret_groups = reg_dump2.match(dump_text).groups()
		dumpId, ver, env, channel, count, md5, date  = ret_groups
		#if env != '0': continue #国内现网
		dump_obj = {'dumpId':dumpId, 'ver':ver, 'count':int(count), 'md5':md5, 'date':date}
		result_dumps.append(dump_obj)
	return result_dumps


def filter_dump_list(dump_datas, base_path):
	filter_dumps = {}	
	for index, dump_obj in enumerate(dump_datas):
		file_name = '%s.html'%(dump_obj['md5'])
		file_path = os.path.join(base_path, file_name)

		success, d_index = False, 0
		while not success and d_index <= 5:
			d_index = d_index + 1 #默认轮询5次
			success = get_dump_text(dump_obj, file_path, index+1)
		if not success: continue

		with open(file_path, 'r', encoding='utf-8') as reader:
			result = reg_dump1.search(reader.read())
			if not result: 
				print('Fxkk ===>>> can\'t find main thread:', file_path)
				continue
		line_list = reg_dump3.findall(result.group())
		if len(line_list) == 0: 
			line_list.append(result.group())

		key_result = '\n'.join(line_list)
		if key_result in filter_dumps:
			curr_count = filter_dumps[key_result]['count']
			filter_dumps[key_result]['count'] = curr_count + dump_obj['count']
		else:
			filter_dumps[key_result] = dump_obj
	return filter_dumps


def new_index_html(list_html, datas):
	list_content = ''
	template_html = '''<!DOCTYPE 5>\n<html>\n\n<head>\n\t<title>Search Result</title>\n</head>\n\n'''
	template_html += '''<body>\n\n\t<h1>Search Result</h1>\n\t<ol>{0}\n\t<ol>\n</body>\n\n</html>'''
	
	sorted_datas = sorted(datas.items(), key=lambda x: x[1]['count'], reverse=True)
	for data_item in sorted_datas:
		data_item[1]['href1'] = base_url + data_item[1]['dumpId']
		data_item[1]['href2'] = base_url + data_item[1]['dumpId'].replace('view', 'file')
		new_li_obj = "\t\t<li>\n\t\t\t<a href='{href1}'>{ver}  {count}  {md5} {date}</a>\n"
		new_li_obj += "\t\t\t<a href='{href2}'>\n\t\t\t\t<button type='button'>download</button>\n\t\t\t</a>\n\t\t</li>\n"
		list_content += new_li_obj.format(**data_item[1])
		#print(data_item[1]['md5'], '==>', data_item[1]['count'])
	
	with open(list_html, 'w', encoding='utf-8') as wtf:
		html_content = template_html.format(list_content)
		wtf.write(html_content); wtf.flush()


reg_dump1 = re.compile(r'(Thread 0.+?)(?=Thread\s\d+)', re.M|re.S)
reg_dump2 = re.compile(r"<a href='(?P<dumpId>[\w?/-]+)'>(?P<ver>[.\w]+)\s+(?P<env>\d+)\s+(?P<channel>\d+)\s+(?P<count>\d+)\s+(?P<md5>\w+)\s+(?P<date>[^<]+)</a>")
reg_dump3 = re.compile(r'\d+\s*(?=libiworld|libEngine|libMiniBaseEngine|liblua|MiniGameApp).+', re.M)

if __name__ == '__main__':
	#old_index_html('index.html')
	
	search_type, search_keys = None, None
	search_type, search_keys = 3, '1.24.10'
	if len(sys.argv) > 1: search_type = sys.argv[1].strip()
	if len(sys.argv) > 2: search_keys = sys.argv[2].strip()
	
	results = get_dump_list(search_keys, search_type, True)
	if len(results) == 0: os.system('pause')
	print('Fxkk ===>> list size:', len(results))

	dir_path = 'downloads'
	if not os.path.isdir(dir_path): 
		os.mkdir(dir_path)
	new_results = filter_dump_list(results, dir_path)

	all_keys = new_results.keys()
	print('Fxkk ===>> new size:', len(all_keys))

	new_index_html('index_new.html', new_results)
	print('Fxkk ===>> new index:', 'index_new.html')