from OpenGL.GL import *

class Shader:
	def __init__(self, ctype:int, fpath:str):
		self.__type = ctype
		self.__data = self.parse(fpath)
		self.compile()

	def parse(self, fpath:str) -> str:
		with open(fpath, 'r') as file:
			content = file.read()
		return content
	
	def gid(self) -> int:
		return self.__id;

	def __del__(self):
		glDeleteShader(self.__id)

	def compile(self) -> None:
		self.__id = glCreateShader(self.__type)
		glShaderSource(self.__id, self.__data)
		# 编译着色器代码
		glCompileShader(self.__id)
		# 检查编译结果
		success = glGetShaderiv(self.__id, GL_COMPILE_STATUS)
		if not success:
			info_log = glGetShaderInfoLog(self.__id).decode()
			print(f"Shader compilation failed: {info_log}")

	