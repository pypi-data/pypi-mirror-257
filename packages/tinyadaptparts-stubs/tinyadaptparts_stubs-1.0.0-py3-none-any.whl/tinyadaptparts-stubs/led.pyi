from enum import Enum

class LedState(Enum):
    ON = True
    OFF = False

class Led:
    def __init__(self, pin: int, state: LedState, path: str) -> None: ...
    def turnOn(self) -> None: ...
    def turnOff(self) -> None: ...
