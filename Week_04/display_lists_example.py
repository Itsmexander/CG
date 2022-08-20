import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd
import math as m
import time

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
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)    
    glRotatef(tick, 1, 0.33, 0.66)
    glCallList(theTorus)
    glutSwapBuffers()

def torus(numc, numt, radius=0.3):
    twopi = 2 * m.pi
    for i in range(numc):
        glBegin(GL_QUAD_STRIP)
        for j in range(numt+1):
            for k in range(1, -1, -1):
                s = (i + k) % numc + 0.5
                t = j % numt

                x = (1+radius*m.cos(s*twopi/numc))*m.cos(t*twopi/numt)
                y = (1+radius*m.cos(s*twopi/numc))*m.sin(t*twopi/numt)
                z = radius*m.sin(s*twopi/numc)
                sx = -m.sin(s*twopi/numc)*m.cos(t*twopi/numt)
                sy = -m.sin(s*twopi/numc)*m.sin(t*twopi/numt)
                sz = m.cos(s*twopi/numc)
                tx = -m.sin(t*twopi/numt)
                ty = m.cos(t*twopi/numt)
                tz = 0
                nx = ty*sz - tz*sy
                ny = tz*sx - tx*sz
                nz = tx*sy - ty*sx
                N = np.array((nx, ny, nz), dtype=np.float32)
                N = N / np.linalg.norm(N)
                glColor3fv(0.5*(N+1))
                glVertex3f(x, y, z)
        glEnd()

def gl_init():
    global start_time, theTorus

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    theTorus = glGenLists(1)
    glNewList(theTorus, GL_COMPILE)
    torus(16, 40)
    glEndList()
    start_time = time.time() - 0.0001

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Display Lists Example")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()