import itertools
import string
from dataclasses import dataclass
from typing import Sequence, SupportsIndex

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

    @property
    def valid_characters(self) -> str:
        """Characters a color step can be applied to."""
        return string.ascii_letters + string.digits + string.punctuation

    def _get_step_sizes(self, num_steps: int) -> RGB:
        """Returns a `RGB` object representing the step size for each color channel."""
        return (self.stop - self.start) / num_steps

    def _get_blended_color(self, step: int, step_sizes: RGB) -> RGB:
        """Returns a `RGB` object representing the color at `step`."""
        return self.start + (step_sizes * step)

    def _get_num_steps(self, text: str) -> int:
        """Returns the number of steps the blend should be divided into."""
        return len([ch for ch in text if ch in self.valid_characters]) - 1

    def apply(self, text: str) -> str:
        """Apply the blend to ascii letters, digits, and punctuation in `text`."""
        num_steps = self._get_num_steps(text)
        if num_steps < 0:  # no valid characters
            return text
        elif num_steps == 0:  # one valid character, just apply start color
            return f"{self.start}{text}[/]"
        step_sizes = self._get_step_sizes(num_steps)
        blended_text = ""
        step = 0
        for ch in text:
            if ch in self.valid_characters:
                blended_text += f"{self._get_blended_color(step, step_sizes)}{ch}[/]"
                step += 1
            else:
                blended_text += ch
        return blended_text


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

    def __init__(self, colors: Sequence[ColorType] = ["pink1", "turquoise2"]):
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

    def _batch_text(self, text: str, n: int) -> list[str]:
        """Split `text` into `n` chunks.

        All chunks will be the same size, except potentially the last chunk."""
        batch_size = int(len(text) / n)
        if batch_size == 0:
            return [ch for ch in text]
        batched_text = [
            text[i * batch_size : (i * batch_size) + batch_size] for i in range(n - 1)
        ]
        lastdex = n - 1
        batched_text.append(text[lastdex * batch_size :])
        return batched_text

    def apply(self, text: str) -> str:
        """Format `text` such that, when printed with `rich`,
        the displayed text changes colors according to this instance's color list."""
        blenders = self._get_blenders()
        batches = self._batch_text(text, len(blenders))
        return "".join(
            blender.apply(batch) for blender, batch in zip(blenders, batches)
        )
