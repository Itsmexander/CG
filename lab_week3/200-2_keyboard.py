#keyboard labweek03
#creat func to use i,j,k,l (key) to control move triangle.
#creat triangle shape 2d in the middle of the screen.
#when press the spacebar key, triangle rotates clockwise.
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd

def display():
    # global xpos,ypos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(xpos, ypos, 0) #modeling transformation
    glRotate(degree, 0, 0, 1) #modeling transformation
    
    glBegin(GL_TRIANGLES)
    glColor3f( 1.0, 1.0, 0.0)
    glVertex3f( -0.5, -0.5, 0.0)

    glColor3f( 1.0, 0.0, 1.0)
    glVertex3f( 0.5, -0.5, 0.0)

    glColor3f( 0.0, 1.0, 1.0)
    glVertex3f( 0.0, 0.5, 0.0)
    
    glEnd()
    glutSwapBuffers()

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-w/h,w/h,-1,1)
    print(w,h)

xpos = 0
ypos = 0
degree = 0

#animation ratate when pressing spacebar key
#triangle make rotation cloclwise.
def idle():
    global degree
    degree = degree + speedRotate
    glutPostRedisplay()

animationRotate = False
speedRotate = 0.05 #value rotate speed for glRotate degree. 
speedMove = 0.02  #value move speed for glTranslatef xpost, ypost.

def keyboard(key, x, y):
    global xpos, ypos, animationRotate, degree, speedMove
    key = key.decode("utf-8")
    if key == 'j':
        xpos = xpos - speedMove
    elif key == 'l':
        xpos = xpos + speedMove
    elif key == 'i':
        ypos = ypos + speedMove
    elif key == 'k':
        ypos = ypos - speedMove
    elif key == ' ':
        animationRotate = not animationRotate
        glutIdleFunc(idle if animationRotate else None)
        
    elif key == 'r':
        ypos = 0
        xpos = 0
        degree = 0
    glutPostRedisplay()

def my_init():
    glEnable(GL_DEPTH_TEST)

def main():

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800,600)
    glutCreateWindow("Keyboard")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    my_init()
    glutMainLoop()



if __name__ == "__main__":

    main()