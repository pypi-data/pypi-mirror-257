from PyNeon import neonwindow as nw
from PyNeon import neongraphics as ng

# Create a window (TITLE, (SIZE))
nw.setupWindow("Hello World in PyNeon", (800, 400))

# initialize font device (SYSFONTNAME, SIZE)
nw.initSysFontDevice('Arial', 20)

# Main loop

while True:
    # Fill the background with white
    nw.clearWindow((255, 255, 255))

    # Draw the text (PARENT, DEVICE, TEXT, POS, COLOR (optional))

    ng.drawText(nw.getScreen(), nw.getFontDevice(), 'Hello world', (0, 0)) # color is black (0, 0, 0) as default

    # Update the window (FRAMERATE(OPTIONAL)) framerate is 40 as default
    nw.update()

# Run it and see the results