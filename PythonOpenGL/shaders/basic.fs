#version 330 core

in vec3 v_color;
in vec2 v_texcoords;

out vec4 FragColor;

uniform sampler2D u_texture;

void main()
{
    //FragColor = texture(u_texture, v_texcoord);
    FragColor = vec4(v_color.r, v_color.g, v_color.b, 1.0f);
}