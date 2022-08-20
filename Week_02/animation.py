import sys
from OpenGL.GL import *
from OpenGL.GLUT import *

degree = 0
def myIdle():
    global degree
    degree = degree + 0.001
    glutPostRedisplay()

def myDisplay():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 1, 0)
    glRotatef(degree, 0.5, 1, 0.5)
    glutWireTeapot(0.8)
    glFlush()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
glutInitWindowSize(512, 512)
glutInitWindowPosition(50, 100)
glutCreateWindow("A Simple Animation")
glutDisplayFunc(myDisplay)
glutIdleFunc(myIdle)    
glutMainLoop()