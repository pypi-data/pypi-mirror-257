from enum import Flag

class PullOption(Flag):
    PULLDOWN = 0
    PULLUP = 1

class Button:
    def __init__(self, pin: int, pull: PullOption, path: str) -> None: ...
    def isPressed(self) -> bool: ...
