import os
import re

reg_tmpl = r'standReportEvent\(\s*"%s",\s*"%s",\s*"%s",\s*"%s"'

script_path = 'G:/MiniGame_CN/AssetRuntime/Script'
def find_report_code(re_code):
    find_codes = ''
    find_result = False
    for (root, dirs, files) in os.walk(script_path):
        files = [f for f in files if f.endswith(('.lua'))]
        for script in files:
            filepath = os.path.join(root, script)
            if filepath.find('universe\\') != -1: continue
            
            with open(filepath, 'r', encoding='iso8859-1') as reader:
                content = reader.read()
                result = re_code.search(content)
                if result: 
                    find_result = True
                    find_codes = result.group()
                    print(result.group(), filepath)

    return find_result, find_codes

if __name__ == '__main__':
	with open('report.txt', 'r', encoding='utf-8') as reader:
		lines = reader.read().split('\n');
		lines = [l for l in lines if l];
		for index, line in enumerate(lines):
			texts = line.split('\t')[1:-1]
			new_reg = reg_tmpl%(texts[0], texts[1], texts[2], texts[3])
			result, retcode = find_report_code(re.compile(new_reg, re.M))
			if result: print('Fxkk========>>>', index)