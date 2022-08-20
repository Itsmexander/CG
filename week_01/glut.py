# -*- coding: utf-8 -*-
from __future__ import absolute_import

import OpenGL.GLUT as glut
import imgui
import time

from . import compute_fb_scale
from .opengl import ProgrammablePipelineRenderer
from imgui.core import Vec2


class GlutRenderer(ProgrammablePipelineRenderer):
    def __init__(self, attach_callbacks=True):
        super(GlutRenderer, self).__init__()

        if attach_callbacks:
            glut.glutSpecialFunc(self.special_callback)
            glut.glutMouseFunc(self.mouse_callback)
            glut.glutMotionFunc(self.motion_callback)
            glut.glutPassiveMotionFunc(self.passive_callback)
            glut.glutKeyboardFunc(self.keyboard_callback)
            glut.glutKeyboardUpFunc(self.keyboard_up_callback)
            glut.glutMouseWheelFunc(self.wheel_callback)
            glut.glutReshapeFunc(self.reshape_callback)

        self.io.display_size = glut.glutGet(glut.GLUT_WINDOW_WIDTH), glut.glutGet(glut.GLUT_WINDOW_HEIGHT)

        self._map_keys()
        self._gui_time = None
        self.start_time = time.time()
        self.mouse = {"x": -1, "y": -1, 
                      glut.GLUT_LEFT_BUTTON: glut.GLUT_UP, 
                      glut.GLUT_MIDDLE_BUTTON: glut.GLUT_UP, 
                      glut.GLUT_RIGHT_BUTTON: glut.GLUT_UP, }
        self.user_special_callback = None
        self.user_mouse_callback = None
        self.user_motion_callback = None
        self.user_passive_callback = None
        self.user_keyboard_callback = None
        self.user_wheel_callback = None
        self.user_reshape_callback = None
        self.current_gui_position = Vec2(x=0, y=0)
        self.current_gui_size = Vec2(x=0, y=0)

    def user_special_func(self, cb):
        self.user_special_callback = cb
    def user_mouse_func(self, cb):
        self.user_mouse_callback = cb
    def user_motion_func(self, cb):
        self.user_motion_callback = cb
    def user_passive_motion_func(self, cb):
        self.user_passive_callback = cb
    def user_keyboard_func(self, cb):
        self.user_keyboard_callback = cb
    def user_wheel_func(self, cb):
        self.user_wheel_callback = cb
    def user_reshape_func(self, cb):
        self.user_reshape_callback = cb
    def set_current_gui_params(self, position, size):
        self.current_gui_position, self.current_gui_size = position, size

    def _map_keys(self):
        key_map = self.io.key_map

        key_map[imgui.KEY_TAB] = ord('\t')
        key_map[imgui.KEY_LEFT_ARROW] = glut.GLUT_KEY_LEFT
        key_map[imgui.KEY_RIGHT_ARROW] = glut.GLUT_KEY_RIGHT
        key_map[imgui.KEY_UP_ARROW] = glut.GLUT_KEY_UP
        key_map[imgui.KEY_DOWN_ARROW] = glut.GLUT_KEY_DOWN
        key_map[imgui.KEY_PAGE_UP] = glut.GLUT_KEY_PAGE_UP
        key_map[imgui.KEY_PAGE_DOWN] = glut.GLUT_KEY_PAGE_DOWN
        key_map[imgui.KEY_HOME] = glut.GLUT_KEY_HOME
        key_map[imgui.KEY_END] = glut.GLUT_KEY_END
        key_map[imgui.KEY_DELETE] = glut.GLUT_KEY_DELETE
        key_map[imgui.KEY_BACKSPACE] = ord('\b')
        key_map[imgui.KEY_ENTER] = ord('\n')
        key_map[imgui.KEY_ESCAPE] = 27
        key_map[imgui.KEY_A] = ord('a')
        key_map[imgui.KEY_C] = ord('c')
        key_map[imgui.KEY_V] = ord('v')
        key_map[imgui.KEY_X] = ord('x')
        key_map[imgui.KEY_Y] = ord('y')
        key_map[imgui.KEY_Z] = ord('z')

    def get_key_modifiers(self):
        io = self.io

        mod = glut.glutGetModifiers()
        io.key_shift = mod & glut.GLUT_ACTIVE_SHIFT
        io.key_ctrl  = mod & glut.GLUT_ACTIVE_CTRL
        io.key_alt   = mod & glut.GLUT_ACTIVE_ALT

    def special_callback(self, key, x, y):
        io = self.io

        if self.user_special_callback: self.user_special_callback(key, x, y)
        io.keys_down[key] = True

    def keyboard_callback(self, key, x, y):
        io = imgui.get_io()

        if self.user_keyboard_callback and \
           not (self.current_gui_position.x <= x <= self.current_gui_position.x + self.current_gui_size.x and \
           self.current_gui_position.y <= y <= self.current_gui_position.y + self.current_gui_size.y): self.user_keyboard_callback(key, x, y)

        key = ord(key)
        if 0 < key < 0x10000:
            io.add_input_character(key)
        else:
            io.keys_down[key] = True
        self.get_key_modifiers()

    def keyboard_up_callback(self, key, x, y):
        io = imgui.get_io()

        key = ord(key)
        io.keys_down[key] = False

    def reshape_callback(self, width, height):
        self.io.display_size = width, height
        if self.user_reshape_callback: self.user_reshape_callback(width, height)

    def mouse_callback(self, button, state, x, y):
        self.mouse[button] = state
        self.mouse["prev_x"], self.mouse["prev_y"] = self.mouse["x"], self.mouse["y"]
        self.mouse["x"], self.mouse["y"] = x, y
        if self.user_mouse_callback and \
           not (self.current_gui_position.x <= x <= self.current_gui_position.x + self.current_gui_size.x and \
           self.current_gui_position.y <= y <= self.current_gui_position.y + self.current_gui_size.y):
            self.user_mouse_callback(button, state, x, y)

    def motion_callback(self, x, y):
        self.mouse["prev_x"], self.mouse["prev_y"] = self.mouse["x"], self.mouse["y"]
        self.mouse["x"], self.mouse["y"] = x, y
        if self.user_motion_callback and \
           not (self.current_gui_position.x <= x <= self.current_gui_position.x + self.current_gui_size.x and \
           self.current_gui_position.y <= y <= self.current_gui_position.y + self.current_gui_size.y):
            self.user_motion_callback(x, y)

    def passive_callback(self, x, y):
        self.mouse["x"], self.mouse["y"] = x, y
        if self.user_passive_callback and \
           not (self.current_gui_position.x <= x <= self.current_gui_position.x + self.current_gui_size.x and \
           self.current_gui_position.y <= y <= self.current_gui_position.y + self.current_gui_size.y): self.user_passive_callback(x, y)

    def wheel_callback(self, button, dir, x, y):
        self.io.mouse_wheel = dir
        if self.user_wheel_callback and self.current_gui_position and self.current_gui_size and \
           not (self.current_gui_position.x <= x <= self.current_gui_position.x + self.current_gui_size.x and \
           self.current_gui_position.y <= y <= self.current_gui_position.y + self.current_gui_size.y): self.user_wheel_callback(button, dir, x, y)

    def process_inputs(self):
        io = imgui.get_io()

        window_size = glut.glutGet(glut.GLUT_WINDOW_WIDTH), glut.glutGet(glut.GLUT_WINDOW_HEIGHT)
        fb_size = glut.glutGet(glut.GLUT_WINDOW_WIDTH), glut.glutGet(glut.GLUT_WINDOW_HEIGHT)

        io.display_size = window_size
        io.display_fb_scale = compute_fb_scale(window_size, fb_size)
        io.delta_time = 1.0/60

        if glut.glutGetWindow():
            io.mouse_pos = self.mouse["x"], self.mouse["y"]
        else:
            io.mouse_pos = -1, -1

        io.mouse_down[0] = self.mouse[glut.GLUT_LEFT_BUTTON] == glut.GLUT_DOWN
        io.mouse_down[1] = self.mouse[glut.GLUT_RIGHT_BUTTON] == glut.GLUT_DOWN
        io.mouse_down[2] = self.mouse[glut.GLUT_MIDDLE_BUTTON] == glut.GLUT_DOWN

        current_time = time.time() - self.start_time

        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        self._gui_time = current_time
