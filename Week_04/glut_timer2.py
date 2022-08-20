import sys
from OpenGL.GL import *
from OpenGL.GLUT import *

def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

def printAndReschedule(interval):
	print("I'm printing this every %d milliseconds" % interval)
	glutTimerFunc(interval, printAndReschedule, interval)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
	glutCreateWindow("glutTimerFunc Example 02")
	glutDisplayFunc(display)
	glutTimerFunc(0, printAndReschedule, 3000)
	glutTimerFunc(0, printAndReschedule, 10000)
	glutTimerFunc(0, printAndReschedule, 15000)
	glutMainLoop()

if __name__ == "__main__":
	main()