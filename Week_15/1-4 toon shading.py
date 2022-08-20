import sys, os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd
import math as m
import imgui
from imgui.integrations.glut import GlutRenderer
from gl_helpers import *

I, light_pos, eye_pos, eye_at = [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 0, 0]
Kd1, Kd2, Ks = [0.01, 0.01, 0.01], [1.0, 1.0, 1.0], [0.8, 0.8, 0.8]
scene_vao, fog_density, shininess, clear_color = None, 0.075, 50, [0.8, 1.0, 1.0]
rot_y, rot_x = 1, 1
diffuse_threshold,specular_threshold,edge_threshold = 0.5, 0.3, 0.3

def draw_gui():
    global clear_color, I, Kd1, Kd2, Ks, shininess, fog_density, diffuse_threshold, specular_threshold, edge_threshold
    global rot_y, rot_x
    impl.process_inputs()
    imgui.new_frame()                 # Start the Dear ImGui frame 
    imgui.set_next_window_position(win_w-300, 10, imgui.FIRST_USE_EVER)
    imgui.begin("Control")            # Create a window
    imgui.push_item_width(200)
    _, I = imgui.color_edit3("Light Intensity", *I)
    _, Kd1 = imgui.color_edit3("Kd1", *Kd1)
    _, Kd2 = imgui.color_edit3("Kd2", *Kd2)    
    _, Ks = imgui.color_edit3("Ks", *Ks)  
    _, shininess = imgui.slider_float("Shininess", shininess, 1, 256)    
    _, diffuse_threshold = imgui.slider_float("diffuse_threshold", diffuse_threshold, 0.0, 1.0)
    _, specular_threshold = imgui.slider_float("specular_threshold", specular_threshold, 0.0, 1.0)
    _, edge_threshold = imgui.slider_float("edge_threshold", edge_threshold, 0.0, 1.0)

    _, rot_y = imgui.slider_float("Rotate Y", rot_y, -180, 180)  
    _, rot_x = imgui.slider_float("Rotate X", rot_x, -180, 180)
    _, clear_color = imgui.color_edit3("Clear Color", *clear_color)    
    imgui.pop_item_width()

    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    impl.set_current_gui_params(imgui.get_window_position(), imgui.get_window_size())        
    imgui.end()

def reshape(w, h):
    global win_w, win_h, proj_mat

    win_w, win_h = w, h
    glViewport(0, 0, w, h)
    proj_mat = Perspective(45, w/h, 0.01, 40)


def display():
    glClearColor(*clear_color, 0)    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    model_mat = Rotate(rot_y, 0, 1, 0) @ Rotate(rot_x, 1, 0, 0)
    view_mat = LookAt(*eye_pos, *eye_at, 0, 1, 0)

    #model_mat = model_mat @ Translate(view_center[0], view_center[1], view_center[2])
    #model_mat = model_mat @ arcball_rotation


    glUseProgram(prog_id)
    glUniformMatrix4fv(glGetUniformLocation(prog_id, "model_mat"), 1, GL_TRUE, model_mat)
    glUniformMatrix4fv(glGetUniformLocation(prog_id, "view_mat"), 1, GL_TRUE, view_mat)
    glUniformMatrix4fv(glGetUniformLocation(prog_id, "proj_mat"), 1, GL_TRUE, proj_mat)
    glUniform3fv(glGetUniformLocation(prog_id, "Kd1"), 1, Kd1)
    glUniform3fv(glGetUniformLocation(prog_id, "Kd2"), 1, Kd2)
    glUniform3fv(glGetUniformLocation(prog_id, "Ks"), 1, Ks)
    glUniform3fv(glGetUniformLocation(prog_id, "I"), 1, I)
    glUniform1f(glGetUniformLocation(prog_id, "shininess"), shininess)
    glUniform3fv(glGetUniformLocation(prog_id, "light_pos"), 1, light_pos)
    glUniform3fv(glGetUniformLocation(prog_id, "eye_pos"), 1, eye_pos)
    glUniform1f(glGetUniformLocation(prog_id, "diffuse_threshold"), diffuse_threshold)
    glUniform1f(glGetUniformLocation(prog_id, "specular_threshold"), specular_threshold)
    glUniform1f(glGetUniformLocation(prog_id, "edge_threshold"), edge_threshold)

    glBindVertexArray(scene_vao)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)

    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())

    glutSwapBuffers()

def print_shader_info_log(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))
        os._exit()

def print_program_info_log(shader, prompt=""):
    result = glGetProgramiv(shader, GL_LINK_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetProgramInfoLog(shader).decode("utf-8")))
        os._exit()

def create_shaders():
    global prog_id, scene_vao, n_vertices
    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global eye_pos, light_pos

    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)

    vert_code = '''
#version 140
uniform mat4 model_mat, view_mat, proj_mat;
in vec3 position, color, normal;
in vec2 uv;
out vec3 v_position, v_color, v_normal;
void main() 
{
    gl_Position = proj_mat* view_mat * model_mat * vec4(position, 1);
    v_position = position;
    v_color = color;
    v_normal = normal;
}
'''

    frag_code = '''
#version 130
uniform vec3 Kd1, Kd2, Ks, I, light_pos, eye_pos;
uniform float shininess, diffuse_threshold, specular_threshold, edge_threshold;
in float fog;
in vec3 v_position, v_color, v_normal;
out vec4 Color;
void main() 
{   
    vec3 N = normalize(v_normal);
    vec3 L = normalize(light_pos - v_position);
    vec3 V = normalize(eye_pos - v_position);
    vec3 H = normalize(L + V);

    float diffuse = max(dot(N, L), 0);
    float specular = pow(max(dot(H, N), 0), shininess);
    float edge = max(dot(N, V), 0);
    vec3 diff_color, spec_color;
    if (diffuse < diffuse_threshold)
        diff_color = Kd1;
    else
        diff_color = Kd2;

    if (specular < specular_threshold)
        spec_color = vec3(0, 0, 0);
    else
        spec_color = Ks;
        
    if (edge < edge_threshold)
        edge = 0;
    else
        edge = 1;

    Color.rgb = edge * (mix(v_color, diff_color, 0.2) + spec_color);
}
'''
    glShaderSource(vert_id, vert_code)
    glShaderSource(frag_id, frag_code)

    glCompileShader(vert_id)
    glCompileShader(frag_id)
    print_shader_info_log(vert_id, "Vertex Shader")
    print_shader_info_log(frag_id, "Fragment Shader")

    prog_id = glCreateProgram()
    glAttachShader(prog_id, vert_id)
    glAttachShader(prog_id, frag_id)

    glLinkProgram(prog_id)
    print_program_info_log(prog_id, "Link error")

    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global light_pos, eye_pos

    df = pd.read_csv("../models/objects_and_floor.tri", delim_whitespace=True, comment='#',
                     header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    eye_pos = centroid + (0, 2, 10)
    light_pos = eye_pos

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    n_vertices = len(positions)

    glUseProgram(prog_id)
    scene_vao = glGenVertexArrays(1)
    glBindVertexArray(scene_vao)
    vbo = glGenBuffers(4)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, positions, GL_STATIC_DRAW)
    position_loc = glGetAttribLocation(prog_id, "position")
    glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 0, 
        c_void_p(0))
    glEnableVertexAttribArray(position_loc)
    color_loc = glGetAttribLocation(prog_id, "color")
    if color_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(color_loc, 3, GL_FLOAT, GL_FALSE, 0, 
            c_void_p(0))
        glEnableVertexAttribArray(color_loc)
    normal_loc = glGetAttribLocation(prog_id, "normal")
    if normal_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
        glBufferData(GL_ARRAY_BUFFER, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 0, 
            c_void_p(0))
        glEnableVertexAttribArray(normal_loc)
    uv_loc = glGetAttribLocation(prog_id, "uv")
    if uv_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[3])
        glBufferData(GL_ARRAY_BUFFER, uvs, GL_STATIC_DRAW)
        glVertexAttribPointer(uv_loc, 2, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(uv_loc)      

def idle():
    global rot_y

    if animation_on:
        rot_y += 0.1
    glutPostRedisplay()

wireframe, animation_on = False, False
def keyboard(key, x, y):
    global wireframe, animation_on

    key = key.decode("utf-8")
    if key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)        
    elif key == ' ':
        animation_on = not animation_on
    elif key.lower() == 'q':
        impl.shutdown()
        os._exit(0)
    glutPostRedisplay()

def initialize():
    global impl

    glEnable(GL_DEPTH_TEST)
    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlutRenderer()
    impl.user_keyboard_func(keyboard)
    impl.user_reshape_func(reshape)
    
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutInitWindowPosition(100, 50)
    glutCreateWindow("Fog")
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)    
    initialize()
    create_shaders()
    glutMainLoop()

if __name__ == "__main__":
    main()    