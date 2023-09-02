from OpenGL.GL import *
from PIL import Image

class Texture:
	def __init__(self, file_path):
		self.__id = glGenTextures(1)
		self.bind()
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

		self.image = Image.open(file_path)
		self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
		image_data = self.image.convert("RGBA").tobytes()
		
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
			self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
		glGenerateMipmap(GL_TEXTURE_2D)

	def bind(self, slot=0):
		#glActiveTexture(GL_TEXTURE0 + slot)
		glBindTexture(GL_TEXTURE_2D, self.__id)