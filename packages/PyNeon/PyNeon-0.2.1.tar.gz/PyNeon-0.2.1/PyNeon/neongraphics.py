from pygame import init, draw, Rect, image, transform
from typing import Tuple, Union
from .neonutils import Int2, Int3
from .neonwindow import Font

class Rectangle:
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        self.color = color
        self._rect = Rect(*pos, *size)

class TexturedRectangle(Rectangle):
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], imagePath: str) -> None:
        super().__init__(pos, size, ())
        self._rectimage = transform.scale(image.load(imagePath), size)
        self._rect = self._rectimage.get_rect()
        self._rect.move(*pos)

def defineRectangle(position: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int]) -> Rectangle:
    '''
Function to draw a rectangle.
Use the getScreen() function's return as the parent,
Int2 for pos and size
Int3 for color.
In the update 0.3.0
This function returns a rect class instance that can be maniplulated using functions.
    '''

    rect = Rectangle(pos=position, size=size, color=color)
    return rect

def defineTexturedRectangle(position: Tuple[int, int], size: Tuple[int, int], imagePath: str) -> Rectangle:
    '''
Function to draw a textured rectangle (Rectangle with a image).
Use the getScreen() function's return as the parent,
Int2 for pos and size
Int3 for color.
In the update 0.3.0
This function returns a rect class instance that can be maniplulated using functions.
    '''

    rect = TexturedRectangle(pos=position, size=size, imagePath=imagePath)
    return rect



def drawRectangleTo(parent: object, rect: Union[TexturedRectangle, Rectangle]) -> None:
    '''
Draws the specified rect to the specified screen.
    '''

    if isinstance(rect, TexturedRectangle):
        parent.blit(rect._rectimage, rect._rect)
        return
    
    draw.rect(parent, rect.color, rect._rect)

def moveRectangle(rectangle: Union[TexturedRectangle, Rectangle], newPosition: Tuple[int, int]) -> None:
    '''
Moves the rectangle to new position.
NOTE: If you don't want the set the x and y instead you want to change x and y, Use the `moveRectangleBy` function.
    '''
    rectangle._rect.x, rectangle._rect.y = newPosition

def moveRectangleBy(rectangle: Union[TexturedRectangle, Rectangle], moveBy: Tuple[int, int]) -> None:
    '''
Changes the rectangle's x and y by the `moveBy` parameter
NOTE: If you don't want the change the x and y instead you want to set x and y, Use the `moveRectangle` function.
    '''
    moveRectangle(rectangle, (rectangle._rect.x + moveBy[0], rectangle._rect.y + moveBy[1]))

def areRectColliding(rect1: Union[TexturedRectangle, Rectangle], rect2: Union[TexturedRectangle, Rectangle]) -> None:
    '''
Checks if rects are colliding
    '''
    return rect1._rect.colliderect(rect2._rect)



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