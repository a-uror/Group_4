import glfw
from OpenGL.GL import *
import numpy as np

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCALE = 60.0
RADIUS_CM = 3.0
CENTER_X_CM = 0.0
CENTER_Y_CM = 2.0
GRID_SIZE = 10

# Simulate text rendering (GLFW doesn’t natively support text)
def render_text(x, y, text):
    """Placeholder for text rendering; prints to console."""
    # In a real application, use a font library like freetype for on-screen text
    print(f"Text at ({x}, {y}): {text}")

# Midpoint Circle Algorithm helper function
def plot_circle_points(x, y):
    """Plot eight symmetric points around the circle's center."""
    centerX = CENTER_X_CM * SCALE
    centerY = CENTER_Y_CM * SCALE
    glVertex2f(centerX + x, centerY + y)
    glVertex2f(centerX + y, centerY + x)
    glVertex2f(centerX + y, centerY - x)
    glVertex2f(centerX + x, centerY - y)
    glVertex2f(centerX - x, centerY - y)
    glVertex2f(centerX - y, centerY - x)
    glVertex2f(centerX - y, centerY + x)
    glVertex2f(centerX - x, centerY + y)

def plot_circle_pixels(radius_cm):
    """Draw a circle using the Midpoint Circle Algorithm."""
    radius = int(radius_cm * SCALE)
    x = 0
    y = radius
    p = 1 - radius
    plot_circle_points(x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(x, y)

# Draw the grid
def draw_grid():
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)  # Light gray
    for i in range(-GRID_SIZE, GRID_SIZE + 1):
        glVertex2f(i * SCALE, -GRID_SIZE * SCALE)
        glVertex2f(i * SCALE, GRID_SIZE * SCALE)
    for i in range(-GRID_SIZE, GRID_SIZE + 1):
        glVertex2f(-GRID_SIZE * SCALE, i * SCALE)
        glVertex2f(GRID_SIZE * SCALE, i * SCALE)
    glEnd()

# Draw the axes
def draw_axes():
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)  # X-axis (red)
    glVertex2f(-GRID_SIZE * SCALE, 0.0)
    glVertex2f(GRID_SIZE * SCALE, 0.0)
    glColor3f(0.0, 1.0, 0.0)  # Y-axis (green)
    glVertex2f(0.0, -GRID_SIZE * SCALE)
    glVertex2f(0.0, GRID_SIZE * SCALE)
    glEnd()
    glLineWidth(1.0)

# Label the axes (simulated due to no native text support)
def label_axes():
    glColor3f(1.0, 0.0, 0.0)  # X-axis labels (red)
    for i in range(-GRID_SIZE, GRID_SIZE + 1):
        if i != 0:
            render_text(i * SCALE - 5, -15, str(i))
    render_text(GRID_SIZE * SCALE - 20, -30, "X (cm)")

    glColor3f(0.0, 1.0, 0.0)  # Y-axis labels (green)
    for i in range(-GRID_SIZE, GRID_SIZE + 1):
        if i != 0:
            render_text(-20, i * SCALE - 5, str(i))
    render_text(-30, GRID_SIZE * SCALE - 20, "Y (cm)")

    glColor3f(1.0, 1.0, 1.0)  # Origin (white)
    render_text(-20, -20, "O")

# Draw circle annotations
def draw_circle_info():
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    info = f"Circle: Center ({CENTER_X_CM}, {CENTER_Y_CM}), Radius = {RADIUS_CM} cm"
    render_text(-GRID_SIZE * SCALE + 20, -GRID_SIZE * SCALE + 20, info)

    glBegin(GL_LINES)
    glVertex2f(CENTER_X_CM * SCALE, CENTER_Y_CM * SCALE)
    glVertex2f((CENTER_X_CM + RADIUS_CM) * SCALE, CENTER_Y_CM * SCALE)
    glEnd()

    render_text((CENTER_X_CM + RADIUS_CM / 2) * SCALE - 15, CENTER_Y_CM * SCALE + 15, "Radius")

# Main rendering function
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_grid()
    draw_axes()
    label_axes()

    # Draw the circle
    glPointSize(3.0)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.8, 1.0)  # Light blue
    plot_circle_pixels(RADIUS_CM)
    glEnd()

    # Draw the center point
    glPointSize(7.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glVertex2f(CENTER_X_CM * SCALE, CENTER_Y_CM * SCALE)
    glEnd()
    glPointSize(1.0)

    draw_circle_info()

def main():
    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    # Create a window
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Midpoint Circle Drawing", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Set up the viewport and projection
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_WIDTH / 2, WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, WINDOW_HEIGHT / 2, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Set clear color
    glClearColor(0.0, 0.0, 0.1, 1.0)  # Dark blue background

    # Main loop
    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Clean up
    glfw.terminate()

if __name__ == "__main__":
    main()