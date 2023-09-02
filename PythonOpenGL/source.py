import glfw
from OpenGL.GL import *

# 顶点着色器
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

# 片段着色器
fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

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
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)

    # 创建片段着色器
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)

    # 创建着色器程序
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    # 设置顶点数据
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # 渲染循环
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # 清空缓冲区
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 绘制三角形
        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        # 交换缓冲区
        glfw.swap_buffers(window)

    # 清理资源
    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteProgram(shader_program)
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # 关闭窗口
    glfw.terminate()

if __name__ == '__main__':
    main()