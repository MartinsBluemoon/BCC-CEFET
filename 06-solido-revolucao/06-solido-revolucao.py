import sys, ctypes, math
import sdl2, sdl2.ext
from OpenGL import GL

def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"Cilindro",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL)
    if not window:
        print(sdl2.SDL_GetError())
        return -1

    context = sdl2.SDL_GL_CreateContext(window)

    GL.glMatrixMode(GL.GL_PROJECTION | GL.GL_MODELVIEW)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glLoadIdentity()
    GL.glOrtho(-400, 400, -300, 300, -300, 300)

    draw(window)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

def draw(window):
    mouse_x, mouse_y = ctypes.c_int(0), ctypes.c_int(0)

    while handle_events():
        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        sdl2.mouse.SDL_GetMouseState(ctypes.byref(mouse_x), ctypes.byref(mouse_y))
        mouse_rotation(mouse_x, mouse_y, draw_cylinder)
        sdl2.SDL_GL_SwapWindow(window)
        sdl2.SDL_Delay(10)

def handle_events():
    for event in sdl2.ext.get_events():
        if event.type == sdl2.SDL_QUIT:
            return False
    return True

def mouse_rotation(mouse_x, mouse_y, draw_function):
    GL.glPushMatrix()
    angle_x = mouse_y.value / 600 * 360
    angle_y = - mouse_x.value / 800 * 360
    GL.glRotatef(angle_x, 1, 0, 0)
    GL.glRotatef(angle_y, 0, 1, 0)
    draw_function()
    GL.glPopMatrix()

def draw_cylinder(radius = 150, size = 150, sides_number = 5):
    size_angle = 2 * math.pi / sides_number
    circle_points = [(radius * math.cos(t * size_angle), radius * math.sin(t * size_angle)) for t in range(sides_number + 1)]

    GL.glBegin(GL.GL_LINE_STRIP)
    for point_index in range(sides_number + 1):
        GL.glColor3f(1, 1, 1)
        GL.glVertex2f(*circle_points[point_index])
    GL.glEnd()

    for point_index in range(sides_number + 1):
        theta = 0
        GL.glBegin(GL.GL_LINE_STRIP)
        while theta <= 2 * math.pi + math.pi / 6:
            x = math.cos(theta)
            z = math.sin(theta)
            GL.glVertex3d(
                circle_points[point_index][0] * x,
                circle_points[point_index][1],
                circle_points[point_index][0] * -z - 1,
            )
            theta = theta + math.pi / 6
        GL.glEnd()

if __name__ == "__main__":
    sys.exit(run())