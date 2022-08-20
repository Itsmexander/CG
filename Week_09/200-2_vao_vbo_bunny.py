import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd
import time

win_w, win_h = 1024, 768

def print_shader_info_log(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))
        sys.exit()

def print_program_info_log(shader, prompt=""):
    result = glGetProgramiv(shader, GL_LINK_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetProgramInfoLog(shader).decode("utf-8")))
        sys.exit()

def create_shaders():
    global prog_id
    global vao, vbo

    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)

    vert_code = b'''
#version 120
attribute vec3 position, color, normal;
attribute vec2 uv;
varying vec4 fragColor;
void main()
{
   gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(position,1);
   fragColor = vec4(0.5*(normal + 1),0);
   
}'''
    frag_code = b'''
#version 120
varying vec4 fragColor;
void main()
{
   gl_FragColor = fragColor;
}'''
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

    # Fix me!
    # Implement VAO and VBO here.

wireframe, pause = False, True
def keyboard(key, x, y):
    global wireframe, pause

    key = key.decode("utf-8")
    if key == ' ':
        pause = not pause
        glutIdleFunc(None if pause else idle)
    elif key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)
    elif key == 'q':
        exit(0)
    glutPostRedisplay()

def reshape(w, h):
    global win_w, win_h

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, win_w/win_h, 0.01, 10)

def display():
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), end='\r')
        start_time = time.time()
        frame_cnt = 0 

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)
    glRotatef(tick, 0, 1, 0)

    glUseProgram(prog_id)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(4)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, positions, GL_STATIC_DRAW)
    position_loc = glGetAttribLocation(prog_id, "position")
    if position_loc != -1:
        glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(position_loc)

    color_loc = glGetAttribLocation(prog_id, "color")
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)
    if color_loc != -1:
        glVertexAttribPointer(color_loc, 3, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(color_loc)

    normal_loc = glGetAttribLocation(prog_id, "normal")
    glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
    glBufferData(GL_ARRAY_BUFFER, normals, GL_STATIC_DRAW)
    if normal_loc != -1:
        glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(normal_loc)

    uv_loc = glGetAttribLocation(prog_id, "uv")
    glBindBuffer(GL_ARRAY_BUFFER, vbo[3])
    glBufferData(GL_ARRAY_BUFFER, uvs, GL_STATIC_DRAW)
    if uv_loc != -1:
        glVertexAttribPointer(uv_loc, 2, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(uv_loc)

    glDrawArrays(GL_TRIANGLES, 0, n_vertices)
    glutSwapBuffers()

frame_cnt, tick = 0, 0
def idle():
    global frame_cnt, tick

    frame_cnt += 1
    tick += 1
    glutPostRedisplay()

def init_model():
    global n_vertices, positions, normals, uvs, centroid, bbox, eye_pos, colors
    global start_time

    glClearColor(0.01, 0.01, 0.2, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    eye_pos = centroid + (0, 0, 1.2*max(bbox))

    n_vertices = len(df.values)
    positions = np.ones((n_vertices, 3), np.float32)
    normals = np.zeros((n_vertices, 3), np.float32)
    positions[:, 0:3] = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals[:, 0:3] = df.values[:, 6:9]
    uvs = df.values[:, 9:11]

    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)
    start_time = time.time() - 1e-4

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutInitWindowPosition(50, 0)    
    glutCreateWindow("VAO and VBO bunny")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    init_model()
    create_shaders()
    glutMainLoop()

if __name__ == "__main__":
    main()