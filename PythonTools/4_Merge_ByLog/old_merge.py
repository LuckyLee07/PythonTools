#--coding:utf8--
import re
import os
import shutil

def copy_file(srcpath, dstpath, fname):
    from_file = os.path.join(srcpath, fname)
    to_file = os.path.join(dstpath, fname)

    fpath, fname = os.path.split(to_file)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    
    shutil.copyfile(from_file, to_file)

g_files = []
def do_crud_file(basefile, mode):
    src_path = 'G:/env1_trunk/bin_externel/res'
    dst_path = 'G:/MiniGame_CN/AssetRuntime/Assets/Resources'
    #if basefile in g_files:  return
    g_files.append(basefile)

    if mode.lower() == 'deleted':
        print('Deleted ===>> ', basefile)
        dst_file = os.path.join(dst_path, basefile)
        if os.path.exists(dst_file): os.remove(dst_file)
    elif basefile.endswith('.csv'):
        print('CSVFile ===>> ', basefile)
    else:
        print('Move File ===>> ', basefile)
        copy_file(src_path, dst_path, basefile)

def diff_buzz(diff_file):
    with open(diff_file, 'r', encoding='utf-8') as reader:
        results = re.findall(r'diff --git a/.+ b/res/(.+)\n(\w+)', reader.read())
        for index, file_mode in enumerate(results):
            file, fmode = file_mode
            do_crud_file(file, fmode)


g_authors = ['ouyanghao', 'zhouguinan', 'chenlinlin', 'tansiyi']
g_authors += ['guanhaihong', 'huangshikun', 'jiangweifang', 'wangchun', 'liukehao']
def filter_author(author):
    for index, fname in enumerate(g_authors):
        if author.find(fname) != -1: 
            return True
    return False

def parse_commit_log(git_file):
    re_vision = re.compile(r'Revision:\s+(\w+)')
    re_author = re.compile(r'Author:\s+(.+)')
    re_ccdate = re.compile(r'Date:\s+(.+)')
    re_message = re.compile(r'Message:\s+(.+)(?=----)', re.S)
    re_modifile = re.compile(r'^----\s+(.+)', re.M|re.S)

    re_mode = re.compile(r'(\w+):\s+res/(.+)')
    re_gex = re.compile(r'(Revision:.+?)(?=Revision|\Z)', re.S)
    with open(git_file, 'r', encoding='utf-8') as reader:
        results = re_gex.findall(reader.read())
        results.reverse() #在列表本身进行倒序不返回新值
        for index, commit in enumerate(results):
            vision = re_vision.findall(commit)[0]
            author = re_author.findall(commit)[0]
            ccdate = re_ccdate.findall(commit)[0]
            message = re_message.findall(commit)[0]
            modifile = re_modifile.findall(commit)[0]
            if filter_author(author):
                if message.find('Merge branch') != -1: continue
                print(f'Fxkk=====>>>:{index}  Author:{author}')
                print('date:', ccdate, 'message:', message.strip())
                print(modifile.strip(), '\n')
                modi_files = re_mode.findall(modifile)
                for mode, cfile in modi_files:
                    do_crud_file(cfile, mode)


if __name__ == '__main__':
    #diff_buzz('diff_buzz.txt')
    parse_commit_log('git_commit.txt')

