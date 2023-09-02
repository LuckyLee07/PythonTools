import os
import re
import json
import time
from bs4 import BeautifulSoup

preurl = 'https://www.wcaworld.com'

def parse_profile(profile):
	profile_infos = [] # list to sort
	all_rows = profile.find_all('div', class_='profile_row');
	for rowinfo in all_rows:
		all_divs = rowinfo.find_all('div');
		dataKey = all_divs[0].text.strip();
		dataVal = all_divs[1].text.strip();
		profile_infos.append({dataKey: dataVal})
	print('Office Contacts:');
	print(profile_infos)

	return profile_infos;

def parse_contact(profile):
	profile_infos = [] # list to sort
	all_rows = profile.find_all('div', class_='profile_row');
	for rowinfo in all_rows:
		all_divs = rowinfo.find_all('div');
		dataKey = all_divs[0].text.strip();
		dataVal = all_divs[1].text.strip();
		profile_infos.append({dataKey: dataVal})
	print('Contact Details:');
	print(profile_infos)
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
	
	company_info = {};
	scity, ecity = '%s - '%city, ' (%s)'%city;
	for idx, compobj in enumerate(all_comp_files):
		print(idx+1, '------------------------------')
		print('Country/City:', country, '/', city);

		filepath = os.path.join(rootdir, '%s_.html'%compobj['id']);
		company_info['id'] = idx + 1;
		compname = compobj['comp'].replace(scity, '').replace(ecity, '');

		if compobj['href'][0] == '/':
			print('Href:', preurl + compobj['href'])
		else:
			print('Info Link:', compobj['href'])

		if not os.path.exists(filepath): 
			company_info['compname'] = compname;
			print('Company Name:', company_info['compname'])
			continue

		with open(filepath, 'r', encoding='utf-8') as reader:
			soup = BeautifulSoup(reader.read(), 'html.parser')
			compname = soup.find('div', class_='company');
			company_info['compname'] = compname.text.strip();
			print('Company Name:', company_info['compname'])

			enrolled = soup.find('p', class_='announce-display');
			print(enrolled.text.strip())

			all_rows = soup.find_all('div', class_='row');
			for idx, rowobj in enumerate(all_rows):
				profile = rowobj.find('div', class_='profile_headline');
				if profile and profile.text == 'Contact Details:':
					company_info['contact_detail'] = parse_contact(rowobj);

			profile = soup.find('div', id='contactperson');
			company_info['contact_person'] = parse_profile(profile);



if __name__ == '__main__':
	country = 'Vietnam';
	citys = ['Da Nang']#,'Hai Duong','Haiphong','Hanoi','Ho Chi Minh City','Quinhon','QuyNhon','Thanh Hoa','Vinh Phuc'];

	time.sleep(5)

	for idx, city in enumerate(citys):
		parse_html(country=country, city=city);
		#booklist.append('{0},{1},{2},{3}'.format(idx,country,city,count))

	#with open('{0}/__List__.csv'.format(country), 'w') as wtf:
	#	for line in booklist: wtf.write(line+'\n');

