from datetime import timedelta
from typing import Any, Callable, Iterable, Optional, Sequence

import rich.progress
from noiftimer import Timer
from rich.console import Console
from rich.progress import ProgressType
from rich.style import StyleType
from rich.text import Text

from .gradient import Gradient


def get_bar_column() -> rich.progress.BarColumn:
    return rich.progress.BarColumn(
        style="sea_green1",
        complete_style="deep_pink1",
        finished_style="cornflower_blue",
        pulse_style="deep_pink1",
    )


def get_task_progress_column(
    *args: Any, **kwargs: Any
) -> rich.progress.TaskProgressColumn:
    return rich.progress.TaskProgressColumn(
        "{task.percentage:>3.0f}%", style="light_coral", markup=False, *args, **kwargs
    )


class TimerColumn(rich.progress.TimeRemainingColumn):
    def __init__(self, elapsed_only: bool = False, *args: Any, **kwargs: Any):
        self.elapsed_only = elapsed_only
        super().__init__(*args, **kwargs)

    def get_time_remaining(self, task: rich.progress.Task) -> str:
        if self.elapsed_when_finished and task.finished:
            task_time = task.finished_time
        else:
            task_time = task.time_remaining
        if not task.total or not task_time:
            return ""
        time_remaining = Timer.format_time(task_time)
        if time_remaining == "<1s":
            time_remaining = "0s"
        return time_remaining

    def get_time_elapsed(self, task: rich.progress.Task) -> str:
        elapsed = task.finished_time if task.finished else task.elapsed
        if not elapsed:
            return ""
        delta = timedelta(seconds=max(0, int(elapsed)))
        time_elapsed = Timer.format_time(delta.total_seconds())
        if time_elapsed == "<1s":
            time_elapsed = "0s"
        return time_elapsed

    def render(self, task: rich.progress.Task) -> Text:
        timing = self.get_time_elapsed(task)
        if not self.elapsed_only and (time_remaining := self.get_time_remaining(task)):
            timing += f" <-> {time_remaining}"
            return Text().from_markup(Gradient().apply(timing))
        return Text().from_markup(f"[pink1]{timing}")


class Progress(rich.progress.Progress):
    """Renders an auto-updating progress bar(s).

    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (Optional[float], optional): Number of times per second to refresh the progress information or None to use default (10). Defaults to None.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        redirect_stdout: (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr: (bool, optional): Enable redirection of stderr. Defaults to True.
        get_time: (Callable, optional): A callable that gets the current time, or None to use Console.get_time. Defaults to None.
        disable (bool, optional): Disable progress display. Defaults to False
        expand (bool, optional): Expand tasks table to fit width. Defaults to False.

        description_last (bool, optional): When using the default columns, the description column will be after the bar instead of before.
    """

    def __init__(
        self,
        *columns: str | rich.progress.ProgressColumn,
        console: Console | None = None,
        auto_refresh: bool = True,
        refresh_per_second: float = 10,
        speed_estimate_period: float = 30,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        get_time: Callable[[], float] | None = None,
        disable: bool = False,
        expand: bool = False,
        description_last: bool = False,
    ) -> None:
        super().__init__(
            *columns,
            console=console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            transient=transient,
            redirect_stdout=redirect_stdout,
            redirect_stderr=redirect_stderr,
            get_time=get_time,
            disable=disable,
            expand=expand,
        )
        if not columns and description_last:
            description = self.columns[0]
            self.columns = self.columns[1:] + (description,)

    @classmethod
    def get_default_columns(cls) -> tuple[rich.progress.ProgressColumn, ...]:
        return (
            rich.progress.TextColumn("[pink1]{task.description}"),
            get_bar_column(),
            get_task_progress_column(),
            TimerColumn(),
            rich.progress.TextColumn("[pink1]{task.fields[suffix]}"),
        )

    def add_task(
        self,
        description: str,
        start: bool = True,
        total: float | None = 100,
        completed: int = 0,
        visible: bool = True,
        suffix: str = "",
        **fields: Any,
    ) -> rich.progress.TaskID:
        fields |= {"suffix": suffix}
        return super().add_task(description, start, total, completed, visible, **fields)


def track(
    sequence: Sequence[ProgressType] | Iterable[ProgressType],
    description: str = "Yeehaw...",
    total: Optional[float] = None,
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "sea_green1",
    complete_style: StyleType = "deep_pink1",
    finished_style: StyleType = "cornflower_blue",
    pulse_style: StyleType = "deep_pink1",
    update_period: float = 0.1,
    disable: bool = False,
    show_speed: bool = True,
) -> Iterable[ProgressType]:
    """Track progress by iterating over a sequence.

    Args:
        sequence (Iterable[ProgressType]): A sequence (must support "len") you wish to iterate over.
        description (str, optional): Description of task show next to progress bar. Defaults to "Working".
        total: (float, optional): Total number of steps. Default is len(sequence).
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        console (Console, optional): Console to write to. Default creates internal Console instance.
        refresh_per_second (float): Number of times per second to refresh the progress information. Defaults to 10.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.finished".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
        update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.
        disable (bool, optional): Disable display of progress.
        show_speed (bool, optional): Show speed if total isn't known. Defaults to True.
    Returns:
        Iterable[ProgressType]: An iterable of the values in the sequence.

    """

    columns: list[rich.progress.ProgressColumn] = (
        [rich.progress.TextColumn("[pink1][progress.description]{task.description}")]
        if description
        else []
    )
    columns.extend(
        (
            rich.progress.BarColumn(
                style=style,
                complete_style=complete_style,
                finished_style=finished_style,
                pulse_style=pulse_style,
            ),
            get_task_progress_column(show_speed=show_speed),
            TimerColumn(elapsed_when_finished=True, elapsed_only=True),
        )
    )
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    with progress:
        yield from progress.track(
            sequence, total=total, description=description, update_period=update_period
        )
