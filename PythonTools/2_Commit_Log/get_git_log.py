# -*- coding: UTF-8 -*-
import os
import re
import shutil
import subprocess

re_commit_list = re.compile(r'(commit\s\w+.*?)\n(?=commit\s\w+|\Z)', re.S|re.M)
re_commit_sobj = re.compile(r'commit\s(?P<cid>\w+)\n(?P<merge>Merge:[\s\w]+)?Author:\s(?P<author>.*?)\nDate:\s(?P<date>.*?)\n')
re_commit_other = re.compile(r'^\n?(?P<msg>(.+\n)+)?(?P<files>[AMDR][\s\S]+)?')


def gitlog_file_init(dstfile, count):
	# 先切换到git仓库所在的目录
	curr_dir = os.getcwd()
	repo_dir = r'G:/env1_trunk/bin_externel'
	if os.path.isdir(repo_dir): os.chdir(repo_dir)

	cmd = ['git', 'log', '-n', '%d'%count, '--name-status']
	output_log = subprocess.check_output(cmd).decode('utf-8')

	os.chdir(curr_dir)
	with open(dstfile, 'w', encoding='utf-8') as wtf:
		wtf.write(output_log); wtf.flush()


def parse_sigle_log(commit):
	result = re_commit_sobj.search(commit)
	if not result: return
	
	cid = result.group('cid').strip()
	date = result.group('date').strip()
	author = result.group('author')
	merge = result.group('merge')
	commit_obj = {'cid':cid,'date':date,'author':author, 'merge':merge}

	flex = ('A','M','D','R')
	msg_and_file = match.replace(result.group(),'')
	file_lines = [l for l in msg_and_file.split('\n') if l.startswith(flex)]
	file_info = '\n'.join(file_lines)
	msgs_info = msg_and_file.replace(file_info, '').rstrip()
	commit_obj['msg'] = msgs_info
	commit_obj['files'] = file_info#len(file_lines)>0 and file_info or None
	return commit_obj


if __name__ == '__main__':
	#gitlog_file_init('git_log.txt', 10000)
	with open('git_log.txt', 'r', encoding='utf-8') as reader:
		data_all_logs = reader.read()
		results = re_commit_list.findall(data_all_logs)
		results.reverse() #以最开始的提交处理
		for index, match in enumerate(results):
			commit_obj = parse_sigle_log(match)
			#if commit_obj['merge']: continue
			print(index, commit_obj['cid'], commit_obj['date'], commit_obj['author'])