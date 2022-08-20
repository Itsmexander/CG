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
models = {}

def reshape(w, h):
    global win_w, win_h
    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, w/h, 1, 100)

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
        os._exit(0)
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
    gluLookAt(*(centroid+(9, 13, max(bbox)*1.6)),1,-7,-5 , 0, 1, 0)

    #bunny 30 models
    glPushMatrix()
    glScalef(0.5,0.5,0.5)
    for i in range(0,5):
        for j in range(0,6):
            glTranslatef(2,0,0)
            glCallList(models["bunny"])
        glTranslatef(-12,0,-2.3)
    glPopMatrix()
    
    #horse 1 model
    glPushMatrix()
    glTranslatef(2.4,0,-5.8)
    glRotatef(90,0,1,0)
    glScalef(0.9,0.9,0.9)
    glCallList(models["horse"])
    glPopMatrix()

    #monkey 1 model
    glPushMatrix()
    glTranslatef(4.4,0,-6.5)
    glCallList(models["monkey"])
    glPopMatrix()

    
    glutSwapBuffers()

#เอาโมเดลมาวาดและนำไปเก็บค่าในdisplay list
def compile_list_on_model(model_filename,kd):
    df = pd.read_csv(model_filename, delim_whitespace=True, comment='#',
                     header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    n_vertices = len(positions)

    #กำหนดตำแหน่งแสง
    light_pos = np.array((9,13,1.6))
    Il = np.array((1.0,1.0,1.0))

    # L = light_pos - positions
    # L = L * 1/np.linalg.norm(L,axis=1).reshape(-1, 1)

    # N = normals
    # NdotL = np.sum(N*L,axis).reshape(-1,1)

    # Il = np.array((1.0,1.0,1.0))

    # diffuse = kd * NdotL * Il



    
    #ส่วนที่ทำการวาดและเก็บไว้ในdisplay list
    list_id = glGenLists(1)
    glNewList(list_id, GL_COMPILE)

    glBegin(GL_TRIANGLES)
    for i in range(n_vertices):
        # glColor3fv(0.5 * (normals[i] + 1))
        L = light_pos - np.array(positions[i])
        L = L / np.linalg.norm(L)

        N = np.array(normals[i])
        NdotL = max(np.dot(N,L),0.0)


        diffuse = kd * NdotL * Il

        glColor3fv(diffuse)
        # glColor3fv(0.5 * (normals[i] + 1))
        glVertex3fv(positions[i])
    
    glEnd()
    glEndList()
    return list_id, centroid, bbox

def gl_init_models():
    global centroid, bbox, start_time

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    kdBunny = np.array((1.0,0.0,1.0))
    models["bunny"], centroid, bbox = \
        compile_list_on_model("../models/bunny_uv.tri",kdBunny)
    kdHorse = np.array((1.0,0.5,0.0))
    models["horse"], _, _ = compile_list_on_model("../models/horse_uv.tri",kdHorse)
    kdMonkey = np.array((0.5,1.0,0.5))
    models["monkey"], _, _ = compile_list_on_model("../models/monkey.tri",kdMonkey)
    start_time = time.time() - 0.0001

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Bunny exercise")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    gl_init_models()
    glutMainLoop()

if __name__ == "__main__":
    main()