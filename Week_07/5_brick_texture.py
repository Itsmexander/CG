import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from math import sin, pi
zoom = 0

def reshape(w, h):
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.1, 50)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5.0, 4.0, 7.0-6*abs(sin(zoom)), 5.0, 4.0, 0.0, 0.0, 1.0, 0.0)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex3f( 0.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 0.0, 8.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(10.0, 8.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()

def idle():
    global zoom
    zoom += 0.01
    if int(zoom / pi) % 2:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glutSetWindowTitle(b"Texture Mapping with GL_LINEAR")
    else:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glutSetWindowTitle(b"Texture Mapping with GL_NEAREST")
    glutPostRedisplay()

def gl_init():
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    filename = "../texture_map/brick_wall_small.jpg"
    try:
        im = Image.open(filename)
    except:
        print("Error:", sys.exc_info()[0])
        raise
    w = im.size[0]
    h = im.size[1]
    image = im.tobytes("raw", "RGB", 0)
    tex_id = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Texture Mapping with")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()