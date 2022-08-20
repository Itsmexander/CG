import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import imgui
from imgui.integrations.glut import GlutRenderer

impl = None
check_box_val1 = True
check_box_val2 = False
float_val = 50
clear_color = [1, 1, 0.5]

def draw_gui():
    global check_box_val1, check_box_val2, float_val, clear_color  
    impl.process_inputs()
    imgui.new_frame()                    # Start the Dear ImGui frame   
    imgui.begin("Control")               # Create a window
    imgui.text("This is some useful text.")
    _, check_box_val1 = imgui.checkbox("Box 1", check_box_val1)
    _, check_box_val2 = imgui.checkbox("Box 2", check_box_val2)
    _, float_val = imgui.slider_float("Intensity", float_val, 0, 100)    
    _, clear_color = imgui.color_edit3("Clear Color", *clear_color)

    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.end()    

def display_cb():
    glClearColor(*clear_color, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex3f(-0.5, -0.5, 0)
    glVertex3f( 0.5, -0.5, 0)
    glVertex3f( 0, 0.5, 0)
    glEnd()    
    glFlush()

    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())

    glutSwapBuffers()

anim = False
def keyboard_cb(key, x, y):
    global anim

    key = key.decode("utf-8")
    if key == 'q':
        impl.shutdown()
        sys.exit(0)

def idle_cb():
    glutPostRedisplay()

def initialize():
    global impl
    show_versions()
    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlutRenderer()
    impl.user_keyboard_func(keyboard_cb)
    imgui.set_next_window_position(500, 10)
    imgui.set_next_window_collapsed(True)

def main():
    global impl, clear_color
    glutInit(sys.argv)
    glutInitContextVersion(3, 1)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    #glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(80, 0)
    glutInitWindowSize(800, 600)
    glutCreateWindow("A Simple GLUT Program with ImGui")
    glutDisplayFunc(display_cb)
    glutIdleFunc(idle_cb)
    initialize()

    glutMainLoop()

def show_versions():
    lists = [['Vendor', GL_VENDOR], ['Renderer',GL_RENDERER],
            ['OpenGL Version', GL_VERSION],
            ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    for x in lists:
        print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

if __name__ == "__main__":
    main()