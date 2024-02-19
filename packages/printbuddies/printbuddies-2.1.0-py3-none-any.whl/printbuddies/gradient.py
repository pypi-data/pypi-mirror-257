import itertools
import string
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Sequence, SupportsIndex

from rich.color import Color
from typing_extensions import Self

from .colormap import Tag


@dataclass
class RGB:
    """
    Dataclass representing a 3 channel RGB color that is converted to a `rich` tag when casted to a string.

    >>> color = RGB(100, 100, 100)
    >>> str(color)
    >>> "[rgb(100,100,100)]"
    >>> from rich.console import Console
    >>> console = Console()
    >>> console.print(f"{color}Yeehaw")

    Can also be initialized using a color name from https://rich.readthedocs.io/en/stable/appendix/colors.html

    >>> color = RGB(name="magenta3")
    >>> print(color)
    >>> "[rgb(215,0,215)]"

    Supports addition and subtraction of `RGB` objects as well as scalar multiplication and division.

    >>> color1 = RGB(100, 100, 100)
    >>> color2 = RGB(25, 50, 75)
    >>> print(color1 + color2)
    >>> "[rgb(125,150,175)]"
    >>> print(color2 * 2)
    >>> "[rgb(50,100,150)]"
    """

    # Typing these as floats so `Gradient` can fractionally increment them
    # When casted to a string, the values will be rounded to integers
    r: float = 0
    g: float = 0
    b: float = 0
    name: str = ""

    def __post_init__(self):
        if self.name:
            self.r, self.g, self.b = Color.parse(self.name).get_truecolor()

    def __str__(self) -> str:
        return f"[rgb({round(self.r)},{round(self.g)},{round(self.b)})]"

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.r - other.r, self.g - other.g, self.b - other.b)

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.r + other.r, self.g + other.g, self.b + other.b)

    def __truediv__(self, val: float) -> Self:
        return self.__class__(self.r / val, self.g / val, self.b / val)

    def __mul__(self, val: float) -> Self:
        return self.__class__(self.r * val, self.g * val, self.b * val)

    def __eq__(self, other: object) -> bool:
        return all(getattr(self, c) == getattr(other, c) for c in "rgb")

    def as_style(self) -> str:
        """Returns a `rich` style compatible string."""
        return self.__str__().strip("[]")


ColorType = RGB | tuple[int, int, int] | str | Tag


class _Blender:
    """
    Apply a color blend from a start color to a stop color across text when printed with the `rich` package.
    """

    def __init__(
        self,
        start: RGB,
        stop: RGB,
    ):
        self.start = start
        self.stop = stop

    def _get_step_sizes(self, num_steps: int) -> RGB:
        """Returns a `RGB` object representing the step size for each color channel."""
        return (self.stop - self.start) / num_steps

    def _get_blended_color(self, step: int, step_sizes: RGB) -> RGB:
        """Returns a `RGB` object representing the color at `step`."""
        return self.start + (step_sizes * step)

    def get_sequence(self, num_steps: int) -> list[RGB]:
        """Returns a sequence of `RGB` color objects representing a blend from `self.start` to `self.stop`."""
        step_sizes = self._get_step_sizes(num_steps)
        # add 1 b/c num_steps is the space between colors
        num_colors = num_steps + 1
        return [self._get_blended_color(step, step_sizes) for step in range(num_colors)]


valid_characters = string.ascii_letters + string.digits + string.punctuation


@lru_cache(None)
def is_valid_character(character: str) -> bool:
    return character in valid_characters


class Gradient(list[RGB]):
    """
    Apply an arbitrary number of color gradients to strings when using `rich`.

    When applied to a string, each character will increment in color from a start to a stop color.

    Colors can be specified by either
    a 3 tuple representing RGB values,
    a `pocketchange.RGB` object,
    a `pocketchange.Tag` object,
    or a color name from https://rich.readthedocs.io/en/stable/appendix/colors.html.

    Tuple:
    >>> gradient = Gradient([(255, 0, 0), (0, 255, 0)])

    `pocketchange.RGB`:
    >>> gradient = Gradient([RGB(255, 0, 0), RGB(0, 255, 0)])

    `pocketchange.Tag`:
    >>> colors = pocketchange.ColorMap()
    >>> gradient = Gradient([colors.red, colors.green])

    Name:
    >>> gradient = Gradient(["red", "green"])

    Usage:
    >>> from pocketchange import Gradient
    >>> from rich.console import Console
    >>>
    >>> console = Console()
    >>> gradient = Gradient(["red", "green"])
    >>> text = "Yeehaw"
    >>> gradient_text = gradient.apply(text)
    >>> # This produces:
    >>> print(gradient_text)
    >>> "[rgb(128,0,0)]Y[/][rgb(102,25,0)]e[/][rgb(76,51,0)]e[/][rgb(51,76,0)]h[/][rgb(25,102,0)]a[/][rgb(0,128,0)]w[/]"
    >>>
    >>> # When used with `console.print`, each character will be a different color
    >>> console.print(gradient_text)
    >>>
    >>> # `Gradient` inherits from `list` so colors may be appended, inserted, or extended
    >>> gradient.append("blue")
    >>> print(gradient.apply(text))
    >>> "[rgb(128,0,0)]Y[/][rgb(64,64,0)]e[/][rgb(0,128,0)]e[/][rgb(0,128,0)]h[/][rgb(0,64,64)]a[/][rgb(0,0,128)]w[/]"
    >>> print(gradient)
    >>> [RGB(r=128, g=0, b=0, name='red'), RGB(r=0, g=128, b=0, name='green'), RGB(r=0, g=0, b=128, name='blue')]
    >>>
    >>> Gradient(gradient + gradient[1::-1])
    >>> [RGB(r=128, g=0, b=0, name='red'), RGB(r=0, g=128, b=0, name='green'), RGB(r=0, g=0, b=128, name='blue'), RGB(r=0, g=128, b=0, name='green'), RGB(r=128, g=0, b=0, name='red')]

    """

    def __init__(self, colors: Iterable[ColorType] = ["pink1", "turquoise2"]):
        colors_ = [self._parse(color) for color in colors]
        super().__init__(colors_)

    def _parse(self, color: ColorType) -> RGB:
        if isinstance(color, RGB):
            return color
        elif isinstance(color, str):
            return RGB(name=color)
        elif isinstance(color, Tag):
            return RGB(name=color.name)
        return RGB(*color)

    def get_num_valid_characters(self, text: str) -> int:
        return len([ch for ch in text if is_valid_character(ch)])

    def __setitem__(self, index: int, color: ColorType):  # type:ignore
        super().__setitem__(index, self._parse(color))

    def append(self, color: ColorType):
        super().append(self._parse(color))

    def insert(self, index: SupportsIndex, color: ColorType):
        super().insert(index, self._parse(color))

    def extend(self, colors: list[ColorType]):  # type:ignore
        super().extend([self._parse(color) for color in colors])

    def _get_blenders(self) -> list[_Blender]:
        return [_Blender(colors[0], colors[1]) for colors in itertools.pairwise(self)]

    def _blend_sequences(self, sequences: Sequence[list[RGB]]) -> list[RGB]:
        """Takes a list of color steps and returns a flattened list of them.

        Colors at the start of inner sequences are replaced with a midpoint
        between the end of the previous sequence and the current sequence's next color.
        """
        sequence: list[RGB] = []
        for i, sub_sequence in enumerate(sequences):
            # Replace duplicate colors at boundaries with a middle color
            if 0 < i < len(sequences):
                previous_color = sequence[-1]
                next_color = sub_sequence[1]
                sub_sequence[0] = previous_color + ((next_color - previous_color) * 0.5)
            sequence.extend(sub_sequence)
        return sequence

    def get_sequence(self, num_steps: int) -> list[RGB]:
        """Return a list of colors representing a gradient across all the colors of this instance."""
        blenders = self._get_blenders()[:num_steps]
        num_blenders = len(blenders)
        steps_per_blender = int(num_steps / num_blenders)
        sequence = self._blend_sequences(
            [blender.get_sequence(steps_per_blender) for blender in blenders]
        )
        # sequence of colors should be one longer than num_steps
        # sometimes there's more b/c odd numbers
        # remove extras from the middle so gradient ends at last color
        # instead of before
        extra_steps = len(sequence) - num_steps - 1
        for _ in range(extra_steps):
            sequence.pop(int(len(sequence) * 0.5))
        return sequence

    def apply(self, text: str) -> str:
        """Format `text` such that, when printed with `rich`, the displayed text changes colors according to this instance's color list."""
        num_valid_characters = self.get_num_valid_characters(text)
        # number of steps should be one less than the number of characters
        if num_valid_characters < 0:  # no valid characters
            return text
        elif num_valid_characters == 0:  # one valid character, just apply start color
            return f"{self._get_blenders()[0].start}{text}[/]"
        sequence = self.get_sequence(num_valid_characters - 1)
        gradient_text = ""
        i = 0
        for ch in text:
            if is_valid_character(ch):
                gradient_text += f"{sequence[i]}{ch}[/]"
                i += 1
            else:
                gradient_text += ch
        return gradient_text
