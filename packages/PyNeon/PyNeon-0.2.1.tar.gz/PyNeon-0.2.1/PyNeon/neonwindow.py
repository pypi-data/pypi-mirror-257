import pygame as p
from .neonutils import isEventQuit
from typing import Tuple, Union

p.init()
_fdevice = None

class Font:
    ARIAL = 'arial'
    SERIF = 'serif'
    SANS_SERIF = 'sans serif'

    def __init__(self, font) -> None:
        self._font = font

def initSysFontDevice(fontName: Union[str, Font], fontSize: int) -> None:
    '''
Initialises the font device for text rendering
    '''
    globals()['_fdevice'] = Font(p.font.SysFont(fontName, fontSize))

def _onEvent(event: object):
    '''
This function is used when an event is occured (key press, exit, e.g..).
By default it only check if the exit event is occured using the neonutils
    '''

    if isEventQuit(event):
        quit()

_window = None
_on_event = _onEvent
_clock = p.time.Clock()

def setupWindow(windowTitle: str, windowSize: Tuple[float, float]) -> None:
    '''
This function is required to make a game in PyNeon.
It sets up the window for you.
    '''
    globals()['_window'] = p.display.set_mode(windowSize)
    p.display.set_caption(windowTitle)

def getScreen() -> object:
    '''
Returns the screen as a object, primarly used for creating shapes. 
    '''

    return _window

def clearWindow(color: Tuple[int, int, int]) -> None:
    '''
Clears window and fills it with the specified color.
    '''
    if _window is None:
        raise Exception("Please setup the window first.")
    
    _window.fill(color)

def getSize() -> Tuple[int, int]:
    if _window is None:
        raise Exception("Please setup the window first.")
    
    return _window.get_width(), _window.get_height()

def setOnEvent(callback: callable) -> None:
    '''
Changes the on event func.
The new func should take a argument with any name as the event arg.

Use the neonutils module to handle events.
    '''
    globals()['_on_event'] = callback

def update(framerate: int=40) -> None:
    '''
This function is required to run a pyneongraphics game.
Remember to setup the window with the `setupWindow` function before calling this function.
    '''

    if _window is None:
        raise Exception("Please setup the window first.")
    
    for ev in p.event.get():
        _on_event(ev)
    
    _clock.tick(framerate)
    p.display.flip()

def getFontDevice(additionalFont=None, sysfont=True) -> Font:
    '''
Returns the font device for drawing text.
    '''
    if _fdevice is None:
        raise Exception("Please initialize font device first!")

    if additionalFont:
        size = _fdevice._font.get_height()
        fn = Font(p.font.SysFont(additionalFont, size) if sysfont else p.font.Font(additionalFont, size))
        
        return fn
    else:
        return _fdevice