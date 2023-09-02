#version 330 core
layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in vec2 a_texcoords;

out vec3 v_color;
out vec2 v_texcoords;

void main()
{
    v_color = a_color;
    v_texcoords = a_texcoords;
    gl_Position = vec4(a_position, 1.0);
}