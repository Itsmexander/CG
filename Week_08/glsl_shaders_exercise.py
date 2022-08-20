from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

prog_id = None

def printShaderInfoLog(shader, prompt=""):
    pass

def printProgramInfoLog(program, prompt=""):
    pass

def compileProgram(vertex_code, fragment_code):
    pass

def gl_init():
    global prog_id

    glEnable(GL_DEPTH_TEST)

    vert_code = '''
#version 120
void main()
{
    gl_Position = gl_Vertex;
}
                '''
    frag_code = ''' 
#version 120
void main()
{
    gl_FragColor = vec4(0, 1, 1, 0);
}
                '''                
    prog_id = compileProgram(vert_code, frag_code)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.01, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
    glUseProgram(prog_id)
    glColor3f(1, 1, 0)
    glutSolidTeapot(1)
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(50, 50)    
    glutCreateWindow("GLSL Shaders Exercise")
    glutDisplayFunc(display)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()    