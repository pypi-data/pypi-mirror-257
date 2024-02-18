from enum import Enum

class Color(Enum):
    WHITE = 0
    BLACK = 1

class SH1106oled:
    def __init__(self, width: int, height: int, SDA_pin: int, SCL_pin: int) -> None: ...
    def clear(self) -> None: ...
    def fill(self, color: Color) -> None: ...
    def drawRectangle(
        self, color: Color, startPos: tuple[int, int], stopPos: tuple[int, int]
    ) -> None: ...
    def drawLine(
        self,
        color: Color,
        startPos: tuple[int, int],
        stopPos: tuple[int, int],
        width: int,
    ) -> None: ...
    def drawText(
        self,
        color: Color,
        text: str,
        size: int,
        centerPos: tuple[int, int],
    ) -> None: ...
