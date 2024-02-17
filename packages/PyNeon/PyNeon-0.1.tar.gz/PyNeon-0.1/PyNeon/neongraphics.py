from pygame import init, draw
from typing import Tuple, Union
from .neonutils import Int2, Int3
from .neonwindow import Font

def drawRectangle(parent, position: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int]) -> None:
    '''
Function to draw a rectangle.
Use the getScreen() function's return as the parent,
Int2 for pos and size
Int3 for color.
    '''

    draw.rect(parent, color, (position, size))

def drawText(parent: object, device: Font, text: str, pos: Tuple[int, int], color: Tuple[int, int, int]=(0, 0, 0)) -> None:
    '''
Function to draw text onto a screen.

Params:
    parent: The window where to draw the text
    device: PyNeon.neonwindow.Font, The font device:
        Use the neonwindow.initSysFontDevice to initialize font device.
        And the neonwindow.getFontDevice to get the for device
    text: str, The text to render
    pos: tuple[int, int], The position where to render the text
    color: tuple[int, int, int], Optional( 255,255,255: black) The text color (normal tuple or neonutils.Int3)
    '''
    text = device._font.render(text, None, color)
    textRect = text.get_rect()
    textRect.x, textRect.y = pos

    parent.blit(text, textRect)