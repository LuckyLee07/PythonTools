import glfw
import array
from Shader import *
from VertexArray import *
from VertexBuffer import *

from OpenGL.GL import *

# 主程序
def main():
    # 初始化GLFW
    if not glfw.init():
        return

    # 创建窗口
    window = glfw.create_window(800, 600, "My OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    # 创建顶点着色器
    vertex_shader = Shader(GL_VERTEX_SHADER, 'shaders/basic.vs')

    # 创建片段着色器
    fragment_shader = Shader(GL_FRAGMENT_SHADER, 'shaders/basic.fs')

    # 创建着色器程序
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader.gid())
    glAttachShader(shader_program, fragment_shader.gid())
    glLinkProgram(shader_program)

    # 设置顶点数据
    verticesx = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ]
    vertices = array.array('f', verticesx)

    layout = VertexArrayLayout()
    layout.push(3, GL_FLOAT, False) # position
    #layout.push(4, GL_UNSIGNED_BYTE, True) # color
    #layout.push(2, GL_FLOAT, False) # texture coordinates

    vao = VertexArray()
    data_size = vertices.itemsize * len(vertices)
    vbo = VertexBuffer(vertices, data_size)
    vao.add_buffer(vbo, layout)

    # 渲染循环
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # 清空缓冲区
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 绘制三角形
        glUseProgram(shader_program)
        
        vao.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)
        vao.unbind()

        # 交换缓冲区
        glfw.swap_buffers(window)

    # 清理资源
    glDeleteProgram(shader_program)

    # 关闭窗口
    glfw.terminate()

if __name__ == '__main__':
    main()
