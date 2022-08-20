import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd
import math as m
import time
import os

win_w, win_h = 1024, 768

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
        os.exit(0)
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

    #ตำแหน่งตา
    eye_pos = np.array((0,3,3))
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)
    #ตำแหน่งแหล่งกำเนิดแสง
    light_pos = np.array((3,4,20))
    #ความเข้มแสง ค่าสีของแสง
    Il = np.array((1.0,1.0,1.0)) 

    Ka = np.array((0.1, 0.1, 0.1), dtype=np.float32)#ambient สีเทาอ่อน
    Kd = np.array((1, 0, 0), dtype=np.float32)#diffuse สีแดง
    Ks = np.array((1, 1, 0), dtype=np.float32) #specular สะท้อนสีเหลือง
    shininess = 50
    N = normals
    L = light_pos - positions
    L = L * 1/np.linalg.norm(L,axis=1).reshape(-1,1)

    NdotL = np.sum(N * L, axis=1).reshape(-1,1)

    V = eye_pos - positions
    V = V * 1/np.linalg.norm(V,axis=1).reshape(-1,1)
    H = L+V
    H = H * 1/np.linalg.norm(H,axis=1).reshape(-1,1)
    NdotH = np.sum(N * H, axis=1).reshape(-1,1)

    ambient = Ka*Il
    diffuse_reflection = Kd*NdotL*Il
    specular_reflection = Ks*pow(NdotH,shininess)*Il


    colors[:, :] = ambient + diffuse_reflection + specular_reflection

    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)
    glutSwapBuffers()

def gl_init_models():
    global start_time
    global n_vertices, positions, colors, normals, uvs, centroid, bbox

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True, 
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    start_time = time.time() - 0.0001

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Illumination with Client-side Verterx Arrays")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    gl_init_models()
    glutMainLoop()

if __name__ == "__main__":
    main()