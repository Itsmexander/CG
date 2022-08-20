#OpenGL Transformations labweek03
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd

models = {}
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*(centroid+(5.5, 5, max(bbox)*0.6)), *centroid, 0, 1, 0) #distance 3-5
    glRotatef(degree, 0, 1, 0)

    #floor 
    glPushMatrix()
    glColor3f(0.752941,0.752941,0.752941)
    glScalef(8,3,20)
    glBegin(GL_POLYGON)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f( 0.5, 0.0, -0.5)
    glVertex3f( 0.5, 0.0, 0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glEnd()
    glPopMatrix()

    #big teapot 1 Origin
    glPushMatrix()
    glRotatef(20, 0, 1, 0)
    glCallList(models["teapotOrigin"])
    glPopMatrix()

    #teapot2
    glPushMatrix()
    glRotatef(180, 0, 1, 0)
    glTranslatef(0.5,0,-2.3)
    glScalef(0.5,0.5,0.5)
    glCallList(models["teapotOrigin"])
    glPopMatrix()

    #teapot3
    glPushMatrix()
    glRotatef(70, 0, 1, 0)
    glTranslatef(3.0,0,-1.4)
    glScalef(0.8,0.8,0.8)
    glCallList(models["teapotOrigin"])
    glPopMatrix()
    
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(45, w/h, 1, 50) #perspective projection

degree = 0
def idle():
    global degree
    degree = degree + 0.04
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

def compile_list_on_model(model_filename):
    df = pd.read_csv(model_filename, delim_whitespace=True, comment='#',
                     header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    n_vertices = len(positions)

    list_id = glGenLists(1)
    glNewList(list_id, GL_COMPILE)

    glBegin(GL_TRIANGLES)
    for i in range(n_vertices):
        glColor3fv(0.5 * (normals[i] + 1))
        glVertex3fv(positions[i])
    
    glEnd()
    glEndList()
    return list_id, centroid, bbox

def gl_init_models():
    global centroid, bbox 
    glClearColor(0.0, 0.0, 0.0, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    
    # model teapot.tri
    models["teapotOrigin"], centroid, bbox = compile_list_on_model("D:/6210451390/icg/models/teapot.tri")

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600) # setting window size 800X600
    glutCreateWindow("Show Normals")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    gl_init_models()
    glutMainLoop()    

if __name__ == "__main__":
    main()