from PyNeon import neonwindow as nw
from PyNeon import neongraphics as ng

'''
in this example you'll learn to check collisions in pyneon
'''

# Create a window (TITLE, (SIZE))
nw.setupWindow("Drawing rect in PyNeon", (800, 400))

# initialize font device (SYSFONTNAME, SIZE)
nw.initSysFontDevice('Arial', 20)

# Rects
rect1 = ng.defineRectangle((0, 0), (35, 35), (0, 0, 0))
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