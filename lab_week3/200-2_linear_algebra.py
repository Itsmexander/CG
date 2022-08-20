#linear_algebra labweek03
#normal vector
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd
import glm

degree_x = 0 #add
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*(centroid+(0, 10, max(bbox))), *centroid, 0, 1, 0)
    glRotatef(degree, 0, 1, 0)
    glRotatef(degree_x, 1, 0, 0) #add
    glBegin(GL_TRIANGLES)
    for i in range(n_vertices):
        glColor3fv(0.5 * (normals[i] + 1))
        glVertex3fv(positions[i])
    glEnd()

    for i in range(0,n_vertices,3):
        #1 Draw triangles superimposed on the model.
        glColor3f(1.0,1.0,1.0) #white line color
        glBegin(GL_LINE_STRIP)
        glVertex3fv(positions[i])
        glVertex3fv(positions[i+1])
        glVertex3fv(positions[i+2])
        glEnd()
        # 2 draw normal vectors 
        glBegin(GL_LINES)
        P = np.array((positions[i] + positions[i+1] + positions[i+2])/3)#find centroid of triangle
        glColor3f(0.0, 1.0, 0.0) #green color
        glVertex3fv(P)#tail vector o-----------
        vec1 = glm.vec3(positions[i+1]-positions[i]) #vector เส้นที่1
        vec2 = glm.vec3(positions[i+2]-positions[i]) #vector เส้นที่2
        vecCross = np.cross(vec1,vec2) #นำมาcrossเพื่อหาvector(ทิศทาง) ที่ตั้งฉาก
        norVec = vecCross / np.linalg.norm(vecCross)# ปรับขนาดทุกเส้นให้เท่ากับ 1
        Q = P+norVec #หัวลูกศร
        glColor3f(1.0, 0.0, 0.0) #red color
        glVertex3fv(Q)#head vector ----------->
        glEnd()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 1, 50)

degree = 0
def idle():
    global degree
    degree = degree + 1
    glutPostRedisplay()

wireframe, animation = False, False
def keyboard(key, x, y):
    global wireframe, animation, degree_x #add degree_x
    speed_move_x = 0.85 #add speed
    key = key.decode("utf-8")
    if key == ' ':
        animation = not animation
        glutIdleFunc(idle if animation else None)
    elif key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)
    elif key == 'q':
        exit(0)
    elif key == 'i':
        degree_x += speed_move_x
    elif key == 'k':
        degree_x -= speed_move_x
    glutPostRedisplay()

def my_init():
    global n_vertices, positions, colors, normals, uvs
    global centroid, bbox

    glClearColor(0.2, 0.8, 0.8, 1)
    df = pd.read_csv("../models/ashtray.tri", delim_whitespace=True, comment='#',
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
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glLineWidth(1)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutCreateWindow("Show Normals")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    my_init()
    glutMainLoop()    

if __name__ == "__main__":
    main()