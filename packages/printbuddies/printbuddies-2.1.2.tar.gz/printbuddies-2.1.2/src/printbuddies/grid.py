from typing import Any, Iterable, Mapping, Sequence

import rich
import rich.console
import rich.style
import rich.table

from .gradient import ColorType, Gradient


class Grid:
    """Convert a sequence of mappings to a `rich` table."""

    def __init__(
        self,
        data: Sequence[Mapping[str, str]],
        title: str | None = None,
        caption: str | None = None,
        style: rich.style.StyleType = "turquoise4",
        header_style: rich.style.StyleType = "deep_pink1",
        title_style: rich.style.StyleType = "italic deep_pink2",
        caption_style: rich.style.StyleType = "italic deep_pink4",
        row_colors: Iterable[ColorType] = ["pink1", "cornflower_blue"],
        gradient_rows: bool = True,
        cast_values_to_strings: bool = False,
        title_justify: rich.console.JustifyMethod = "center",
        caption_justify: rich.console.JustifyMethod = "center",
        show_header: bool = True,
    ):
        """
        If `gradient_rows` is `True`, `row_colors` will be applied as a gradient across rows instead of alternating colors.

        If `cast_values_to_strings` is `True`, all values in `data` will be casted to strings before being added to the table.

        This class has a `__rich__` method, so it can be printed directly with `rich.print(Grid(data))` or `rich.console.Console().print(Grid(data))`
        """
        headers = data[0].keys()
        gradient = Gradient(row_colors)
        if gradient_rows:
            row_colors = [
                color.as_style() for color in gradient.get_sequence(len(data))
            ]
        else:
            row_colors = [color.as_style() for color in gradient]
        if cast_values_to_strings:
            data = [{k: str(v) for k, v in datum.items()} for datum in data]
        self.table = rich.table.Table(
            *headers,
            show_lines=True,
            style=style,
            header_style=header_style,
            title_style=title_style,
            caption_style=caption_style,
            row_styles=row_colors,
            title=title,
            caption=caption,
            show_header=show_header,
            title_justify=title_justify,
            caption_justify=caption_justify,
        )
        for datum in data:
            self.table.add_row(*datum.values())

    def __rich__(self) -> rich.table.Table:
        return self.table
