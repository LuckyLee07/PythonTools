# -*- coding: UTF-8 -*-
from get_git_log import *


g_authors = ['ouyanghao', 'zhouguinan', 'chenlinlin', 'tansiyi']
g_authors += ['guanhaihong', 'huangshikun', 'jiangweifang', 'wangchun', 'liukehao']
def author_check(author):
	for author_ in g_authors:
		if author.find(author_) != -1: 
			return True
	return False


def rename_file(basepath, srcfile, dstfile):
	srcpath = os.path.join(basepath, srcfile)
	dstpath = os.path.join(basepath, dstfile)
	if not os.path.exists(srcpath):
		print('Rename: file not found ======>>> ', srcpath)
		return
	shutil.copyfile(srcpath, dstpath)


def copy_file(srcpath, dstpath, fname):
    from_file = os.path.join(srcpath, fname)
    to_file = os.path.join(dstpath, fname)

    fpath, fname = os.path.split(to_file)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    
    if not os.path.exists(from_file):
    	print('Copy: file not found ======>>> ', from_file)
    	return
    shutil.copyfile(from_file, to_file)


def do_crud_file(basefile, mode, do_opt=False):
    src_path = 'G:/env1_trunk/bin_externel/res'
    dst_path = 'G:/MiniGame_CN/AssetRuntime/Assets/Resources'
    
    #if basefile in g_files: return
    #g_files.append(basefile)

    if mode == 'D':
        #print('Deleted ===>> ', basefile)
        if not do_opt: return

        dst_file = os.path.join(dst_path, basefile)
        if os.path.exists(dst_file):os.remove(dst_file)
    elif mode[0] == 'R':
    	basefile = basefile.replace('res/','')
    	srcfile, dstfile = basefile.split('\t')
    	#print('Rename ===>> ', dstfile, srcfile)
    	if not do_opt: return
    	rename_file(dst_path, srcfile, dstfile)
    elif basefile.endswith('.csv'):
        print('CSVFile ===>> ', basefile)
        if not do_opt: return
        dst_path = 'G:/MiniGame_CN/AssetRuntime/Script'
    else:
        #print('Move File ===>> ', basefile)
        if not do_opt: return
        copy_file(src_path, dst_path, basefile)

diff_csv = ['horse', 'horseability', 'itemdef', 'monster', 'recycle', 'roleskin', 'spraypaint', 'storehorse', 'storeprop']
if __name__ == '__main__':
	#gitlog_file_init('git_log.txt', 10000)
	with open('git_log.txt', 'r', encoding='utf-8') as reader:
		data_all_logs = reader.read()
		results = re_commit_list.findall(data_all_logs)
		results.reverse() #以最开始的提交处理
		results = results[1000:-1]
		for index, match in enumerate(results):
			commit_obj = parse_sigle_log(match)
			if commit_obj['merge']: continue
			if author_check(commit_obj['author']):
				date = commit_obj['date']
				if commit_obj['files'].find('.csv')!=-1:
					print(index, date, commit_obj['author'])
					
				files = commit_obj['files'].split('\n')
				files = [f for f in files if f.strip()]
				for index, mode_file in enumerate(files):
					mode, basefile = mode_file.split('\t',1)
					if not basefile.startswith('res/'):
						continue
					do_crud_file(basefile[4:], mode)