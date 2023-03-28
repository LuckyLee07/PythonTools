# -*- coding: UTF-8 -*-
import os
import re
import json
import shutil


diff_csv = ['horse', 'horseability', 'itemdef', 'monster', 'recycle', 'roleskin', 'spraypaint', 'storehorse', 'storeprop']

g_file_filter = []
def file_check_OK(curfile):
    global g_file_filter;
    if g_file_filter:
        for file in g_file_filter:
            if curfile.find(file) !=-1:
                return False
        return True
    with open('filter_files.txt', 'r') as reader:
        all_lines = reader.read().split('\n')
        files = [l for l in all_lines if l.replace(',','')]
        g_file_filter = [f.strip() for f in files if f.strip()]


def compare_file(leftPath, rightPath, ftype, copyflag=None):
    c_add, c_diff, c_sums = 0, 0, 0;
    for (root, dirs, files) in os.walk(leftPath):

        if ftype == '.csv' and root != leftPath: 
            continue #csv只遍历第一层
        files = [f for f in files if f.endswith(ftype)]
        
        for file in files: #遍历读取文件
            c_sums += 1

            filepathL = os.path.join(root, file)
            if not file_check_OK(filepathL): continue

            with open(filepathL, 'rb') as reader1:
                contentL = reader1.read();

                filepathR = filepathL.replace(leftPath, rightPath);
                if not os.path.exists(filepathR):
                    c_add += 1
                    print("Add =====>>>", filepathR)
                    if copyflag: 
                    	dirx, file_ = os.path.split(filepathR);
                    	if not os.path.exists(dirx): os.mkdir(dirx);
                    	shutil.copyfile(filepathL,filepathR);
                    continue
                    
                with open(filepathR, 'rb') as reader2:
                    contentR = reader2.read();

                if contentL != contentR:
                    c_diff += 1
                    print("Diff =====>>>", filepathL)
                    if copyflag: shutil.copyfile(filepathL,filepathR);

    print('Fxkk=========>>> add:%d'%c_add, '===>>> diff:%d'%c_diff , ' ===>> total:%d'%c_sums);


#src_path, dst_path = dst_path, src_path
if __name__ == '__main__':
    re_gex = re.compile(r"[\w_]+:\s+'([^\']+)'[^\w]+[\w_]+:\s+'([^\']+)'[^\w]+[\w_]+:\s+'([^\']+)'[^\w]+")
    with open('diff_path.txt', 'r', encoding='utf-8') as reader:
        results = re.findall(r'\{(.+?)\}', reader.read(), re.DOTALL)
        file_types = ('.csv', '.png', 'omod', '.jta', '.emo', '.ent', '.gif', '.prefab')
        for ret_obj in results:
            result = re_gex.search(ret_obj)
            key_name = result.group(1)
            src_path = result.group(2)
            dst_path = result.group(3)
            if key_name == 'csvdef': continue 
            #if key_name == 'entity': continue

            copy_file = None#True
            #if key_name == 'particle': copy_file = True
            compare_file(src_path, dst_path, file_types, copy_file)
    
    ##---------------播报背景框Copy---------------
    src_path = 'G:/env1_trunk/bin_externel/res/miniui/miniworld'
    dst_path = 'G:/MiniGame_CN/AssetRuntime/Assets/Resources/miniui/miniworld'
    for file in os.listdir(src_path):
        if file.startswith('t_shop'):
            src_file = os.path.join(src_path, file)
            dst_file = os.path.join(dst_path, file)
            shutil.copyfile(src_file, dst_file)