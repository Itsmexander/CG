from OpenGL.GL import *
from OpenGL.GLUT import *
import imgui
from imgui.integrations.glut import GlutRenderer

culling_on = GL_FALSE
cull_face_choice = 1
front_face_choice = 1

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if culling_on:
        glEnable(GL_CULL_FACE)
    else:
        glDisable(GL_CULL_FACE)

    if cull_face_choice == 1:
        cullFaceMode = GL_BACK
    elif cull_face_choice == 2:
        cullFaceMode = GL_FRONT
    else:
        cullFaceMode = GL_FRONT_AND_BACK

    if front_face_choice == 1:
        frontFaceMode = GL_CCW
    else:
        frontFaceMode = GL_CW

    glFrontFace(frontFaceMode)
    glCullFace(cullFaceMode)

    glBegin(GL_QUADS)
    glColor3f(1.0, 0.5, 0.5)
    glVertex2f(-0.9, -0.4)
    glVertex2f(-0.1, -0.4)
    glVertex2f(-0.1,  0.4)
    glVertex2f(-0.9,  0.4)

    glColor3f(0.5, 1.0, 0.5)
    glVertex2f(0.1, -0.4)
    glVertex2f(0.1,  0.4)
    glVertex2f(0.9,  0.4)
    glVertex2f(0.9, -0.4)
    glEnd()

    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())

    glutSwapBuffers()

wireframe = False
def keyboard(key, x, y):
    global wireframe

    key = key.decode("utf-8")
    if key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)        
    elif key == 'q':
        impl.shutdown()
        sys.exit(0)

def idle():
    glutPostRedisplay()

def draw_gui():
    global front_face_choice, cull_face_choice, culling_on

    impl.process_inputs()    
    imgui.new_frame()                    # Start the Dear ImGui frame   
    imgui.begin("Control")               # Create a window
    if culling_on:
        _, culling_on = imgui.checkbox("glEnable(GL_CULL_FACE)", culling_on)
    else:
        _, culling_on = imgui.checkbox("glDisable(GL_CULL_FACE)", culling_on)
    imgui.text("glCullFace(...)")
    bit_1 = cull_face_choice & 1
    bit_2 = (cull_face_choice >> 1) & 1
    bit_3 = (cull_face_choice >> 2) & 1
    if imgui.radio_button("GL_BACK", bit_1): 
        bit_1 = not bit_1
        if bit_1: 
            bit_2 = bit_3 = 0
    imgui.same_line()
    if imgui.radio_button("GL_FRONT", bit_2): 
        bit_2 = not bit_2
        if bit_2:
            bit_1 = bit_3 = 0
    imgui.same_line()
    if imgui.radio_button("GL_FRONT_AND_BACK", bit_3): 
        bit_3 = not bit_3
        if bit_3:
            bit_1 = bit_2 = 0
    cull_face_choice = (bit_3 << 2) | (bit_2 << 1) | bit_1

    imgui.text("glFrontFace(...)")
    bit_1 = front_face_choice & 1
    bit_2 = (front_face_choice >> 1) & 1
    if imgui.radio_button("GL_CCW", bit_1): 
        bit_1 = not bit_1
        if bit_1: bit_2 = 0
    imgui.same_line()
    if imgui.radio_button("GL_CW", bit_2): 
        bit_2 = not bit_2
        if bit_2: bit_1 = 0
    front_face_choice = (bit_2 << 1) | bit_1

    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.end()

def gl_gui_init():
    global impl
    glClearColor(0.0, 0.0, 0.0, 0.0)

    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlutRenderer()
    impl.user_keyboard_func(keyboard)
    
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow("Cull Face Example")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    gl_gui_init()
    glutMainLoop()

if __name__ == "__main__":
    main()