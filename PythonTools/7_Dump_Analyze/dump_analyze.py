# -*- coding: UTF-8 -*-
import os
import re
import sys
import subprocess

#命令行：cdb -lines -z file.dump

source_path = r'G:\MiniGame_CN\Source'
local_symbol_path = r"E:/MiniWorldPdb/LocalSymbols"
windows_symbol_path = r"E:/MiniWorldPdb/SystemSymbols"
sym_path = f'{local_symbol_path};{windows_symbol_path}'

cdb_exe_path = r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\cdb.exe"

def run_command(sym_path, source_path, dmp_file):
    cdb_command = ".reload; !analyze -v;"
    cdb_command += ".printf\"\\n==================== 当前异常现场 ====================\\n\"; .excr;"
    cdb_command += ".printf\"\\n==================== 异常线程堆栈 ====================\\n\"; kb;"
    #cdb_command += ".printf\"\\n==================== 所有线程堆栈 ====================\\n\"; ~* kv;"
    cdb_command += "q"
    arguments = ['-z', dmp_file, '-y', sym_path, "-srcpath", source_path,'-c', cdb_command, '-lines', '50']
    output = subprocess.check_output([cdb_exe_path] + arguments, encoding='gbk')
    
    output = output.replace('F:\\minichina\\MiniGame\\', '')
    output = output.replace('C:\\Program Files (x86)\\Microsoft Visual Studio\\2019', 'VS2019')
    output = re.sub(r' *\([^)\n]*?\) *', ' ', output)
    output = re.sub(r'\[[^@]+\\w+ @ \d+\]', ' ', output)
    #print('<<<=============.reload; !analyze -v;=============>>>')
    
    with open('dump_file.txt', 'w', encoding='utf-8') as wtf:
        wtf.write(output); wtf.flush()


g_dumps_path = {
    '1.24.11' : ['659e8caf-11d7-49f5-b1cd-a876b6ad60e3.dmp']
}

if __name__ == '__main__':

    dump_path = g_dumps_path['1.24.11'][0]
    #run_command(sym_path, source_path, dump_path)
    
    g_re_gex = re.compile(r'Stack trace(.+)?quit:', re.S|re.M)  
    with open('dump_file.txt', 'r', encoding='utf-8') as reader:
        content = reader.read()
        match_result = g_re_gex.search(content)
        if not match_result:
            print('Trace not found =====>>>', dump_path)
        
        stack_trace = match_result.group() if match_result else ''
        all_lines = stack_trace.split('\n')
        for index, cur_line in enumerate(all_lines):
            #new_line = re.sub(r'\(Inline\)[-\s]+', '', cur_line)
            #new_line = re.sub(r'\w{8}\s\w{8}\s{5}\w{8}\s\w{8}\s\w{8}\s', '', new_line)
            
            new_line = re.sub(r' *\([^)\n]*?\) *', ' ', cur_line)
            new_line = re.sub(r'(\+0x\w+)\s+(?:\[|\\)[^@]+\\([.\w]+)\s*@\s*(\d+)\]', r'(*) (\2 : \3\1)', new_line)
            all_lines[index] = new_line
        
        new_stack = '\n'.join(all_lines)
        content = content.replace(stack_trace, new_stack)

        print(content)
        