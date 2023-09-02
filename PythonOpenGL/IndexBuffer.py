from OpenGL.GL import *
import numpy as np

class IndexBuffer:
	def __init__(self, data, size):
		self.__ibo = glGenBuffers(1)
		self.bind()
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, data.tobytes(), GL_STATIC_DRAW)
		self.unbind()

	def bind(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__ibo)

	def unbind(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

	def __del__(self):
		glDeleteBuffers(1, [self.__ibo])