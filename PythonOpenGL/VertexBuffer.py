from OpenGL.GL import *
import numpy as np

class VertexBuffer:
	def __init__(self, data, size):
		self.__vbo = glGenBuffers(1)
		self.bind()
		glBufferData(GL_ARRAY_BUFFER, size, data.tobytes(), GL_STATIC_DRAW)
		#glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)
		self.unbind()

	def bind(self):
		glBindBuffer(GL_ARRAY_BUFFER, self.__vbo)

	def unbind(self):
		glBindBuffer(GL_ARRAY_BUFFER, 0)

	def __del__(self):
		glDeleteBuffers(1, [self.__vbo])