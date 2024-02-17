from PyNeon import neonwindow as nw
from PyNeon import neongraphics as ng
# os getcwd is optional
from os import getcwd

'''
in this example you'll learn to load textures for a rect in pyneon
We'll also check collision, textured rectangle with normal rectangle
'''

# Create a window (TITLE, (SIZE))
nw.setupWindow("Drawing rect in PyNeon", (800, 400))

# initialize font device (SYSFONTNAME, SIZE)
nw.initSysFontDevice('Arial', 20)

# Rects
rect1 = ng.defineTexturedRectangle((0, 0), (35, 35), f'{getcwd()}\\examples\\images\\myimage.png') # The color paramter is gone and image path instead.
rect2 = ng.defineRectangle((40, 40), (35, 35), (0, 0, 0))

# Main loop

while True:
    # Fill the background with white
    nw.clearWindow((255, 255, 255))

    # SHow the rects (PARENT, RECT)

    ng.drawRectangleTo(nw.getScreen(), rect1)
    ng.drawRectangleTo(nw.getScreen(), rect2)

    # move the first rect
    
    ng.moveRectangleBy(rect1, (2, 2))

    # check collision
    if ng.areRectColliding(rect1, rect2):
        print("Collision detected!")

    # Update the window (FRAMERATE(OPTIONAL)) framerate is 40 as default
    nw.update()

# Run it and see the results