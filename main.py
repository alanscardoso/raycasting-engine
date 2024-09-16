import glfw
from OpenGL.GL import *

glfw.init()
window = glfw.create_window(640, 480, "Raycasting Engine", None, None)
glfw.make_context_current(window)    

while not glfw.window_should_close(window):
    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    draw_player()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()