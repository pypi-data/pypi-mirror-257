from PyNeon import neonwindow as nw
from PyNeon import neongraphics as ng
from PyNeon import neonutils as nu

'''
In this example you'll learn about event handling in PyNeon.
We'll be making a counter.
'''

# Create a window (TITLE, (SIZE))
nw.setupWindow("Event handling in PyNeon", (800, 400))

# initialize font device (SYSFONTNAME, SIZE)
nw.initSysFontDevice('Arial', 20)

# counter var
counter = 0

# on event function (event)
def onEvent(event):
    global counter
    # Check if event is quit
    if nu.isEventQuit(event):
        quit()
    
    # Increase the counter by using space
    if nu.isSpecialKey(event, nu.SpecialKeys.SPACE):
        counter += 1
    # decrease it by using the 'd'key
    elif nu.isKey(event, 'd'):
        counter -= 1

# change the on event function
nw.setOnEvent(onEvent)

# Main loop

while True:
    # Fill the background with white
    nw.clearWindow((255, 255, 255))

    # Draw the counter (PARENT, DEVICE, TEXT, POS, COLOR (optional))

    ng.drawText(nw.getScreen(), nw.getFontDevice(), f'Counter: {counter}', (0, 0)) # color is black (0, 0, 0) as default

    # Update the window (FRAMERATE(OPTIONAL)) framerate is 40 as default
    nw.update()

# Run it and see the results