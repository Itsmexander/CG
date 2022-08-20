from OpenGL.GL import *
from glfw.GLFW import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

culling_on = GL_FALSE
cull_face_choice = 1
front_face_choice = 1

def display_cb():
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

def keyboard_cb(window, key, scancode, action, mods):
    if key in (GLFW_KEY_ESCAPE, GLFW_KEY_Q) and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

def gl_init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
def main():
    global front_face_choice, cull_face_choice, culling_on

    if not glfwInit():
        glfwTerminate()
        exit()
    glfwDefaultWindowHints()
    window = glfwCreateWindow(800, 800, "Cull Face Example", None, None)
    glfwMakeContextCurrent(window)
    gl_init()

    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlfwRenderer(window)
    glfwSetKeyCallback(window, keyboard_cb)
    imgui.set_next_window_position(500, 200)
    imgui.set_next_window_collapsed(True)

    while not glfwWindowShouldClose(window):
        glfwPollEvents()
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
        
        display_cb()
        imgui.render()
        impl.render(imgui.get_draw_data())

        glfwSwapBuffers(window)

    impl.shutdown()
    glfwTerminate()

if __name__ == "__main__":
    main()