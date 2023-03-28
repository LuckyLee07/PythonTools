# -*- coding: UTF-8 -*-
import os
import re
import sys
import subprocess

local_symbol_path = r"E:/MiniWorldPdb/LocalSymbols"
windows_symbol_path = r"E:/MiniWorldPdb/SystemSymbols"
sym_path = f'{local_symbol_path};{windows_symbol_path}'

cdb_exe_path = r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\cdb.exe"

def run_command(sym_path, dmp_file):
    cdb_command = ".reload; !analyze -v;"
    cdb_command += ".printf\"\\n==================== 当前异常现场 ====================\\n\"; .excr;"
    cdb_command += ".printf\"\\n==================== 异常线程堆栈 ====================\\n\"; kv;"
    cdb_command += ".printf\"\\n==================== 所有线程堆栈 ====================\\n\"; ~* kv;"
    cdb_command += "q"
    arguments = ['-z', dmp_file, '-y', sym_path, '-c', cdb_command]
    output = subprocess.check_output([cdb_exe_path] + arguments)
    #new_output = output.decode().split(r'\n')
    print(type(output), output)
    print(output.decode('utf-8'))
    print(output.decode('utf-8').split(r'\n'))

dump_path = '4aa2801ae04ca4bb593ea18ca068e346.dmp'
dump_path = '13c15fa77211894ee494130dd36f84.dmp'
if __name__ == '__main__':
	#run_command(sym_path, dump_path)
	
	with open('../dump.txt', 'r') as reader:
		all_lines = reader.read().split(r'\n')
		for index, line in enumerate(all_lines):
			print(index, '==========>>>>>', line)