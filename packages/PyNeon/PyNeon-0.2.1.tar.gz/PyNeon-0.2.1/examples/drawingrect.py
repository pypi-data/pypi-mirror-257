from PyNeon import neonwindow as nw
from PyNeon import neongraphics as ng

'''
in this example you'll learn to draw a rect in pyneon
We'll be also moving the rect
You can also use the neonwindow.getSize function that returns a tuple as the window size to make the rect bounce.
'''

# Create a window (TITLE, (SIZE))
nw.setupWindow("Drawing rect in PyNeon", (800, 400))

# initialize font device (SYSFONTNAME, SIZE)
nw.initSysFontDevice('Arial', 20)

# Rect
rect = ng.defineRectangle((0, 0), (35, 35), (0, 0, 0))

# Main loop

while True:
    # Fill the background with white
    nw.clearWindow((255, 255, 255))

    # SHow the rect (PARENT, RECT)

    ng.drawRectangleTo(nw.getScreen(), rect)

    # move it
    
    ng.moveRectangleBy(rect, (2, 2))

    # Update the window (FRAMERATE(OPTIONAL)) framerate is 40 as default
    nw.update()

# Run it and see the results