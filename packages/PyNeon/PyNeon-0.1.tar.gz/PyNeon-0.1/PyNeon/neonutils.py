from pygame.locals import *

def isEventQuit(event: object) -> None:
    '''
Checks if user is quiting
    '''
    return event.type == QUIT

class SpecialKeys:
    RETURN = K_RETURN
    RIGHT_ARROW = K_RIGHT
    LEFT_ARROW = K_LEFT
    UP_ARROW = K_UP
    DOWN_ARROW = K_DOWN
    SPACE = K_SPACE
    LEFT_CONTROL = K_LCTRL
    RIGHT_CONTROL = K_RCTRL
    LEFT_ALT = K_LALT
    RIGHT_ALT = K_RALT
    LEFT_SHIFT = K_LSHIFT
    RIGHT_SHIFT = K_RSHIFT
    ESCAPE = K_ESCAPE
    BACKSPACE = K_BACKSPACE
    
def isSpecialKey(event: object, key: SpecialKeys) -> None:
    '''
Checks if a special like backspace is pressed
Use the SpecialKeys class for this func.
    '''
    return event.type == KEYDOWN and event.key == key

def isKey(event: object, key: str) -> None:
    '''
Checks if a key is pressed, ('a', '2', etc...).
    '''
    return event.type == KEYDOWN and event.key == globals()[f'K_{key}']

def Int3(a: int, b: int, c: int) -> None:
    '''
This function is not required for 3 sized tuples, you can use normal tuples too.
However it is primary so you should consider using it.
    '''
    return (a, b, c)

def Int2(a: int, b: int) -> None:
    '''
This function is not required for 2 sized tuples, you can use normal tuples too.
However it is primary so you should consider using it.
    '''
    return (a, b)
