import os
import re
import json
import time
import xlrd
import xlwt
#import xlsxwriter
from bs4 import BeautifulSoup
from xlutils.copy import copy

preurl = 'https://www.wcaworld.com'

def parse_profile(profile):
	profile_infos = [] # list to sort
	all_rows = profile.find_all('div', class_='profile_row');
	for rowinfo in all_rows:
		all_divs = rowinfo.find_all('div');
		dataKey = all_divs[0].text.strip();
		dataVal = all_divs[1].text.strip();
		profile_infos.append({dataKey: dataVal})
	return profile_infos;

def parse_contact(profile):
	profile_infos = [] # list to sort
	all_rows = profile.find_all('div', class_='profile_row');
	for rowinfo in all_rows:
		all_divs = rowinfo.find_all('div');
		dataKey = all_divs[0].text.strip();
		dataVal = all_divs[1].text.strip();
		profile_infos.append({dataKey: dataVal})
	return profile_infos;


def parse_html(country, city, xmlfile=None):
	#pattern = re.compile(r'\d+_\.html');
	rootdir = os.path.join(country, city);

	all_comp_files = [] #city with files
	with open('%s/%s.csv'%(country, city), 'r') as reader:
		alllines = reader.read().split('\n');
		alllines = [l for l in alllines if l];
		for line in alllines:
			idx, href, comp = line.split(',',2);
			compobj = {'id':idx,'href':href.strip(),'comp':comp.strip()};
			all_comp_files.append(compobj);
	
	company_infos = [];
	scity, ecity = '%s - '%city, ' (%s)'%city;
	for idx, compobj in enumerate(all_comp_files):
		company_info = {}
		company_infos.append(company_info);

		#print(idx+1, '------------------------------')
		#print('Country/City:', country, '/', city);
		
		company_info['city'] = city;
		company_info['country'] = country;

		filepath = os.path.join(rootdir, '%s_.html'%compobj['id']);
		company_info['id'] = idx + 1;

		compname = compobj['comp'].replace(scity, '')
		compname = compname.replace(ecity, '');

		company_info['href'] = compobj['href'];
		#print('Info Link:', company_info['href'])

		if not os.path.exists(filepath): 
			company_info['compname'] = compname;
			#print('Company Name:', company_info['compname'])
			continue

		with open(filepath, 'r', encoding='utf-8') as reader:
			soup = BeautifulSoup(reader.read(), 'html.parser')
			compname = soup.find('div', class_='company');
			company_info['compname'] = compname.text.strip();
			#print('Company Name:', company_info['compname'])

			enrolled = soup.find('p', class_='announce-display');
			enrolled = enrolled.text.replace('Proudly Enrolled Since:', '');
			company_info['enrolled'] = enrolled.strip();
			#print(company_info['enrolled'])

			all_rows = soup.find_all('div', class_='row');
			for idx, rowobj in enumerate(all_rows):
				profile = rowobj.find('div', class_='profile_headline');
				if profile and profile.text == 'Contact Details:':
					company_info['contact_detail'] = parse_contact(rowobj);

			profile = soup.find('div', id='contactperson');
			company_info['contact_person'] = parse_profile(profile);

	write_toxls('Vietnam.xls', company_infos);

	for idx, company_info in enumerate(company_infos):
		print(idx+1, '------------------------------')
		print('Country:', company_info['country'])
		print('City:', company_info['city'])
		print('Company Name:', company_info['compname'])
		print('Info Link:', company_info['href'])

		if company_info.get('enrolled'):
			print(company_info['enrolled'])
			print('Contact Details:')
			print(company_info['contact_detail']);
			print('Office Contacts:')
			print(company_info['contact_person']);


def get_style(name,height,format,bold=False,halign=None,valign=None):
	style = xlwt.XFStyle()
	if format.strip()!='':
		style.num_format_str = format;
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4;
	font.height = height;
	style.font = font;

	alignment = xlwt.Alignment()
	#HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	if halign: alignment.horz = halign

	#VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
	alignment.vert = xlwt.Alignment.VERT_CENTER
	if valign: alignment.vert = valign
	style.alignment = alignment
	
	return style;


def get_href_style(name,height,format,bold=False,halign=None):
	style = get_style(name, height, format, bold, halign);
	style.font.underline = True;
	style.font.colour_index  = 4;
	
	return style;

def set_colstyle(sheet, cIndex, width, height=None):
	col = sheet.col(cIndex);
	col.width = width;
	if height: col.height = height;

def write_toxls(xlsPath, companys):
	newbook = xlwt.Workbook(encoding='utf-8')
	newsheet = newbook.add_sheet('Sheet1', cell_overwrite_ok=True)
	set_colstyle(newsheet, 0, 256*15)
	set_colstyle(newsheet, 1, 256*15)
	set_colstyle(newsheet, 2, 256*40)
	set_colstyle(newsheet, 3, 256*35)
	set_colstyle(newsheet, 4, 256*20)

	set_colstyle(newsheet, 5, 256*50)
	set_colstyle(newsheet, 6, 256*50)

	headers = ['Country','City','Company','InfoLink','Enrollment','Contact Details', 'Office Contacts']
	for col, value in enumerate(headers):
		newsheet.write(0, col, value, get_style('Arial',300,'',True))

	rows = len(companys);
	row_style = get_style('Arial',240,'',False);
	for row in range(1, rows):
		company_info = companys[row-1];
		newsheet.row(row).height_mismatch = True;
		newsheet.row(row).height = 20 * 65;

		newsheet.write(row, 0, company_info['country'], row_style)
		newsheet.write(row, 1, company_info['city'], row_style)
		
		horz_align = xlwt.Alignment.HORZ_LEFT;
		name_style = get_style('Arial',240,'',False, horz_align);
		newsheet.write(row, 2, company_info['compname'], name_style)

		href_link = company_info['href'];
		if href_link.startswith('/'): href_link = preurl + href_link;
		hyper_link = 'HYPERLINK("{0}";" {1}")'.format(href_link,company_info['href']);
		href_style = get_href_style('Arial',240,'',False, horz_align);
		newsheet.write(row, 3, xlwt.Formula(hyper_link), href_style)
		
		if company_info.get('enrolled'):
			newsheet.write(row, 4, company_info['enrolled'], row_style)

			row_data = '';
			vert_align = xlwt.Alignment.VERT_JUSTIFIED;
			contact_style = get_style('Arial',240,'',False, horz_align, vert_align);
			for datainfo in company_info['contact_detail']:
				for key, value in datainfo.items():
					row_data += key + value + '\n';
			newsheet.write(row, 5, row_data[:-1], contact_style);

			#newsheet.write(row, 6, company_info['contact_person'])
	newbook.save(xlsPath)


def read_write_xls(cpath):
	wb = xlrd.open_workbook(cpath, formatting_info=True)
	sheet = wb.sheet_by_index(0)
	rows = sheet.nrows
	cols = sheet.ncols
	#merge = sheet.merged_cells
	
	cp_wb = copy(wb);
	sheet_wtf = cp_wb.get_sheet(0);
	patt = re.compile(r'\d+([\w\s]+)')
	row_style = get_style('Arial',240,'',False);
	for r in range(0, rows):
		company = sheet.cell_value(r,3);
		result = patt.match(company);
		if result:
			sheet_wtf.write(r, 3, result.group(1), row_style)
		#if r > 10: break
	cp_wb.save('JC LIST_1.xls')

if __name__ == '__main__':
	read_write_xls('JC LIST1.xls')

