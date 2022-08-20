import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for i in range(n_vertices):
        glColor3fv(0.5 * (normals[i] + 1))
        glVertex3fv(positions[i])
    glEnd()
    glutSwapBuffers() #add glutSwapbuffers
    glFlush()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1,1,-1,1)

def idle():
    glRotate(1, 0, 1, 0)
    glutPostRedisplay()

wireframe, animation = False, False
def keyboard(key, x, y):
    global wireframe, animation

    key = key.decode("utf-8")
    if key == ' ':
        animation = not animation
        glutIdleFunc(idle if animation else None)
    elif key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)
    elif key == 'q':
        exit(0)
    glutPostRedisplay()

def my_init():
    global n_vertices, positions, colors, normals, uvs

    df = pd.read_csv("../models/monkey.tri", delim_whitespace=True, comment='#',
                     header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    n_vertices = len(positions)
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE) #chang glut_single to glut_double
    glutInitWindowSize(800, 800)
    glutCreateWindow("Double Framebuffer Exercise")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    my_init()
    glutMainLoop()    

if __name__ == "__main__":
    main()