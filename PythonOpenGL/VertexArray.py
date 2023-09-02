from OpenGL.GL import *
from VertexArrayLayout import *

class VertexArray:
	def __init__(self):
		self.__vao = glGenVertexArrays(1)
		self.bind()

	def add_buffer(self, buffer, layout):
		buffer.bind()

		offset = 0
		stride = layout.get_stride()
		elements = layout.get_elements()
		# 绑定 buffer 对象中的数据
		for idx, element in enumerate(elements):
			glEnableVertexAttribArray(idx)

			glVertexAttribPointer(idx, element.count, element.dtype, 
				element.normalized, stride, ctypes.c_void_p(offset))
			offset += element.get_size()

	def bind(self):
		glBindVertexArray(self.__vao)

	def unbind(self):
		glBindVertexArray(0)

	def __del__(self):
		glDeleteVertexArrays(1, [self.__vao])
		
	def gid(self):
		return self.__vao