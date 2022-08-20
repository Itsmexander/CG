import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd
import math as m
import time

win_w, win_h = 1024, 768
prog_id = None


def reshape(w, h):
    global win_w, win_h

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, win_w/win_h, 0.01, 50)

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

tick, frame_cnt = 0, 0
def idle():
    global tick, frame_cnt
    tick += 1
    frame_cnt += 1
    glutPostRedisplay()

def display():
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), tick, end='\r')
        start_time = time.time()
        frame_cnt = 0    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    eye_pos = centroid + (0, 0, 1.5*max(bbox))
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)


    # glRotatef(tick,0,1,0)
    
    glUseProgram(prog_id)
    glDrawArrays(GL_TRIANGLES,0,n_vertices)

    glutSwapBuffers()

def printShaderInfoLog(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not result:
        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))
        exit()

def printProgramInfoLog(program, prompt=""):
    result = glGetProgramiv(program, GL_LINK_STATUS)

    if not result:
        print("%s: %s" % (prompt, glGetProgramInfoLog(program).decode("utf-8")))
        exit()

def compileProgram(vertex_code, fragment_code):
    prog_id = glCreateProgram()
    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vert_id, vertex_code)
    glShaderSource(frag_id, fragment_code)

    glCompileShader(vert_id)
    printShaderInfoLog(vert_id, "Vertex Shader")
    glCompileShader(frag_id)
    printShaderInfoLog(frag_id, "Fragment Shader")

    glAttachShader(prog_id, vert_id)
    glAttachShader(prog_id, frag_id)

    glLinkProgram(prog_id)
    printProgramInfoLog(prog_id, "Link Program")
    return prog_id

def gl_init_models():
    global start_time
    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global prog_id

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = np.ones((n_vertices, 3), np.float32)
    normals = np.zeros((n_vertices, 3), np.float32)
    positions[:, 0:3] = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals[:, 0:3] = df.values[:, 6:9]
    uvs = df.values[:, 9:11]


#glsl shader
    vert_code = b'''
#version 120
out vec4 color;
void main()
{
    gl_Position = gl_Vertex;
    //gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
    vec3 normal = gl_Normal;
    color = vec4( 0.5*(normal + 1),0);
}
                '''
    frag_code = b'''
#version 120
in vec4 color;
void main()
{
    gl_FragColor = color;
}
    '''
    prog_id = compileProgram(vert_code,frag_code)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, uvs)
    
    start_time = time.time() - 0.0001

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Bunny GLSL")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    gl_init_models()
    glutMainLoop()

if __name__ == "__main__":
    main()