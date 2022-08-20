import sys
from OpenGL.GL import *
from OpenGL.GLUT import *

def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

def printInt(value):
	print("Got an integer: %d\n" % value)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
	glutCreateWindow("glutTimerFunc Example 01")
	glutDisplayFunc(display)
	glutTimerFunc(2000, printInt, 123)
	glutTimerFunc(3000, printInt, 456)
	glutTimerFunc(4000, printInt, 789)
	glutMainLoop()

if __name__ == "__main__":
	main()