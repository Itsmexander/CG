import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd
import math as m

t_value = 0
x_value = 0


def reshape(w, h):
    glViewport(0, 0, w, h)	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.1, 50)

def display():
    global cw,zw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye_pos = np.array((0,1,2))
    eye_at = centroid

    gluLookAt(*eye_pos, *eye_at, 0, 1, 0)

    #////////////////// rotate light
    glPushMatrix()
    glRotatef(t_value, 0, 1, 0)
    glRotatef(x_value, 1, 0, 0)#แสงหมุนรอบแกนx

    light_pos = [3,4,20,1]
    light_ka_kd_ks = [1,1,1,1]
    

    glLightfv(GL_LIGHT0,GL_POSITION,light_pos)
    glLightfv(GL_LIGHT0,GL_AMBIENT,light_ka_kd_ks)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,light_ka_kd_ks)
    glLightfv(GL_LIGHT0,GL_SPECULAR,light_ka_kd_ks)
    

    mat_ambient = [0.05, 0.05, 0.05, 1.0]
    mat_diffuse = [0.86, 0.65, 0.13, 1.0]
    mat_specular = [1.0, 1.0, 0.0, 1.0]
    mat_se = 50

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_se)
    glPopMatrix()
    #////////////////

    
    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, uvs)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)     
    glutSwapBuffers()

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

x_pos = 0
y_pos = 0
def motion(x,y):
    global x_pos,y_pos,t_value,x_value
    speed = 4
    if(x_pos == 0 and y_pos == 0):
        x_pos = x
        y_pos = y
    # print("x_post : %d y_pos : %d"%(x_pos,y_pos))
    if x > x_pos:
        t_value += speed
        x_pos = x
        # y_pos = y
    elif x < x_pos:
        t_value -= speed
        x_pos = x
        # y_pos = y
    
    if y > y_pos:
        x_value += speed
        # x_pos = x
        y_pos = y
    elif y < y_pos:
        x_value -= speed
        # x_pos = x
        y_pos = y
    #  # print("x : %d y : %d"%(x,y))
   

    glutPostRedisplay()


def idle():
    global t_value
    t_value += 1
    glutPostRedisplay()

def gl_init():
    global n_vertices, positions, colors, normals, uvs, centroid, bbox

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    al = [0.1, 0.1, 0.1, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, al)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutCreateWindow("OpenGL Light Control with Mouse")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMotionFunc(motion) #call back function แบบ เมาส์กดแล้วลาก
    glutKeyboardFunc(keyboard)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()