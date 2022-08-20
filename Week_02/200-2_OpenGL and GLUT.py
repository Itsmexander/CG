import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import pi,sin,cos


def display():
    glClearColor(1.0, 1.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glVertex3f( 0.5,  0.5, 0.0)
    glVertex3f(-0.5,  0.5, 0.0)
    glEnd()
    
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    for i in range(256):
        theta = 2*i*pi/256
        y = 0.5*sin(theta)
        x = 0.5*cos(theta)
        glVertex2f(x,y)
    glEnd()
    glFlush()

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-4/3,4/3,-1,1) 

def main():

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Program Template")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)



    glutMainLoop()



if __name__ == "__main__":

    main()