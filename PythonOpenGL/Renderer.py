import glfw
import array
from OpenGL.GL import *

from Shader import Shader
from VertexBuffer import VertexBuffer
from VertexArray import VertexArray
from VertexArrayLayout import VertexArrayLayout
from IndexBuffer import IndexBuffer
from Texture import Texture


class Renderer:
	def __init__(self, width, height):
		# 初始化GLFW
	    if not glfw.init(): return

	    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

	    # 创建窗口
	    self.window = glfw.create_window(width, height, "My OpenGL Window", None, None)
	    if not self.window:
	        glfw.terminate()
	        raise Exception("Failed to create GLFW window")

	    glfw.make_context_current(self.window)

	    glClearColor(0.2, 0.3, 0.3, 1.0)


	def pre_render(self):
		# 创建顶点着色器
	    vertex_shader = Shader(GL_VERTEX_SHADER, 'shaders/basic.vs')
	    # 创建片段着色器
	    fragment_shader = Shader(GL_FRAGMENT_SHADER, 'shaders/basic.fs')

	    # 创建着色器程序
	    self.shader_program = glCreateProgram()
	    glAttachShader(self.shader_program, vertex_shader.gid())
	    glAttachShader(self.shader_program, fragment_shader.gid())
	    glLinkProgram(self.shader_program)

		#del vertex_shader,del fragment_shader


	    # 设置顶点数据
	    vertices = [
	        # positions          # colors           # texture coords
			 0.5,  0.5, 0.0,     1.0, 0.0, 0.0,     1.0, 1.0,   # top right
			 0.5, -0.5, 0.0,     0.0, 1.0, 0.0,     1.0, 0.0,   # bottom right
			-0.5, -0.5, 0.0,     0.0, 0.0, 1.0,     0.0, 0.0,   # bottom left
			-0.5,  0.5, 0.0,     1.0, 1.0, 0.0,     0.0, 1.0    # top left 
    	]
	    vertices = array.array('f', vertices)

	    layout = VertexArrayLayout()
	    layout.push(3, GL_FLOAT, False) # position
	    layout.push(3, GL_FLOAT, False) 	# color
	    layout.push(2, GL_FLOAT, False) # texcoord
	    #layout.push(3, GL_UNSIGNED_BYTE, True) # color

	    self.vao = VertexArray()
	    data_size = vertices.itemsize * len(vertices)
	    self.vbo = VertexBuffer(vertices, data_size)
	    self.vao.add_buffer(self.vbo, layout)

	    self.vao.bind()
	    indices = [0, 1, 3, 1, 2, 3]
	    indices = array.array('f', indices)
	    data_size = indices.itemsize * len(indices)
	    self.ibo = IndexBuffer(indices, data_size)
	    self.vao.unbind()

	    self.texture = Texture('res/textures/cute_cat.png')


	def after_render(self):
		# 先释放vbo再释放vao
		del self.vbo
		del self.vao
		# 先释放program再释放shader
		glDeleteProgram(self.shader_program)
		


	def render(self):
		# 绘制三角形
		glUseProgram(self.shader_program)

		self.vao.bind()
		glDrawArrays(GL_TRIANGLES, 0, 3)
		self.vao.unbind()
		
		glUseProgram(0)

	def draw_indexed(self):
		# 1. 激活着色器程序
		glUseProgram(self.shader_program)

		# 2. 绑定VAO和索引缓冲对象
		self.vao.bind()
		self.ibo.bind()

		# 3. 调用glDrawElements函数
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)

		# 4. 解绑定VAO和索引缓冲对象
		self.ibo.unbind()
		self.vao.unbind()

		# 5. 关闭着色器程序
		glUseProgram(0)
		
	def run(self): # 渲染循环
		self.pre_render()
		while not glfw.window_should_close(self.window):
			self.process_input()

			# 清空缓冲区
			glClear(GL_COLOR_BUFFER_BIT)

			self.render() # 主渲染逻辑
			#self.draw_indexed()

			# 交换缓冲区
			glfw.swap_buffers(self.window)

			glfw.poll_events()

		self.after_render()

		# 关闭窗口
		glfw.terminate()

	def process_input(self):
		if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
			glfw.set_window_should_close(self.window, True)
		
