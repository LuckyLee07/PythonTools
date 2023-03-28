from OpenGL.GL import *

def get_dtype_size(data_type):
	if data_type == GL_FLOAT:
		return 4
	elif data_type == GL_UNSIGNED_INT:
		return 4
	elif data_type == GL_UNSIGNED_BYTE:
		return 1
	else:
		return 0


class VertexBufferElement:
	def __init__(self, count, dtype, normalized):
		self.count = count  # 属性值数量
		self.dtype = dtype  # 属性值类型，如GL_FLOAT
		self.normalized = normalized  # 是否需要标准化

	def get_size(self):
		dtype_size = get_dtype_size(self.dtype)
		return self.count * dtype_size  #获取单个属性值的大小


class VertexArrayLayout:
	def __init__(self):
		self.__stride = 0
		self.__elements = []

	def get_stride(self):
		return self.__stride

	def get_elements(self):
		return self.__elements

	def push(self, size, data_type, normalized):
		element = VertexBufferElement(size, data_type, normalized)
		self.__elements.append(element)
		self.__stride += size * get_dtype_size(data_type)

	