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
varying vec3 color;
void main()
{
   gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
}'''
    frag_code = b'''
#version 140
varying vec3 color;
void main()
{
   gl_FragColor = vec4(1, 0, 1, 1);
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
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)
    glutSwapBuffers()

frame_cnt, tick = 0, 0
def idle():
    global frame_cnt, tick

    frame_cnt += 1
    tick += 1
    glutPostRedisplay()

def init_model():
    global n_vertices, positions, normals, uvs, centroid, bbox, eye_pos
    global start_time

    glClearColor(0.01, 0.01, 0.2, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    df = pd.read_csv("../models/armadillo.tri", delim_whitespace=True,   
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    eye_pos = centroid + (0, 0, 1.2*max(bbox))

    positions = df.values[:, 0:3]
    normals = df.values[:, 3:6]
    uvs = df.values[:, 6:8]

    n_vertices = len(positions)
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
    glutCreateWindow("VAO and VBO Exercise")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    init_model()
    create_shaders()
    glutMainLoop()

if __name__ == "__main__":
    main()