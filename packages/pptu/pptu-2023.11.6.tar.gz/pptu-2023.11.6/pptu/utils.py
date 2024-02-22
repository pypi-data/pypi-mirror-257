from __future__ import annotations

import argparse
import re
import sys
import shutil
import itertools
from typing import (
    TYPE_CHECKING, Any, IO, Iterable, Literal, NoReturn, overload
)

import humanize
import oxipng
import toml
from pathlib import Path
from bs4 import BeautifulSoup
from requests.utils import CaseInsensitiveDict
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    ProgressColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.text import Text
from wand.image import Image

from .constants import PROG_NAME, PROG_VERSION


if TYPE_CHECKING:
    from rich.progress import Task

    from .uploaders import Uploader


class Config:
    def __init__(self, file: Path):
        try:
            self._config = CaseInsensitiveDict(toml.load(file))
        except FileNotFoundError:
            shutil.copy(
                Path(__file__).resolve().parent.with_name('config.example.toml'), file
            )
            eprint(
                f"Config file doesn't exist, created to: [cyan]{file}[/]", fatal=True)  # noqa: E501

    def get(self, tracker: Uploader | Literal["default"], key: str, default: Any = None) -> Any:
        value = None
        if tracker != "default":
            value = self._config.get(tracker.name, {}).get(key) or self._config.get(tracker.abbrev, {}).get(key)

        if value is False:
            return value
        defa = self._config.get("default", {}).get(key)
        if not value and defa is False:
            return defa

        return value or defa or default


class RParse(argparse.ArgumentParser):
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs.setdefault("formatter_class", lambda prog: CustomHelpFormatter(prog))
        super().__init__(*args, **kwargs)

    def _print_message(self, message: str, file: IO[str] | None = None) -> None:
        if message:
            if message.startswith("usage"):
                message = f"[bold cyan]{PROG_NAME}[/] {PROG_VERSION}\n\n{message}"
                message = re.sub(r"(-[a-z]+\s*|\[)([A-Z]+)(?=]|,|\s\s|\s\.)", r"\1[bold color(231)]\2[/]", message)
                message = re.sub(r"((-|--)[a-z]+)", r"[green]\1[/]", message)
                message = message.replace("usage", "[yellow]USAGE[/]")
                message = message.replace("positional arguments", "[yellow]POSITIONAL ARGUMENTS[/]")
                message = message.replace("options", "[yellow]FLAGS[/]", 1)
                message = message.replace(" file ", "[bold magenta] file [/]", 2)
                message = message.replace(self.prog, f"[bold cyan]{self.prog}[/]")
            message = f"[not bold default]{message.strip()}[/]"
            print(message)


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs.setdefault("max_help_position", 80)
        super().__init__(*args, **kwargs)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ", ".join(action.option_strings) + " " + args_string


class CustomTransferSpeedColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        speed = task.finished_speed or task.speed
        if speed is None:
            return Text("--", style="progress.data.speed")
        data_speed = humanize.naturalsize(int(speed), binary=True)
        return Text(f"{data_speed}/s", style="progress.data.speed")


def flatten(L: Iterable[Any]) -> list[Any]:
    # https://stackoverflow.com/a/952952/492203
    return [item for sublist in L for item in sublist]


def print(  # noqa: A001
    text: Any = "", highlight: bool = False, file: IO[str] = sys.stdout, flush: bool = False, **kwargs: Any
) -> None:
    with Console(highlight=highlight) as console:
        console.print(text, **kwargs)
        if flush:
            file.flush()


def wprint(text: str) -> None:
    if text.startswith("\n"):
        text = text.lstrip("\n")
        print()
    print(f"[bold color(231) on yellow]WARNING:[/] [yellow]{text}[/]")


@overload
def eprint(text: str, fatal: Literal[False] = False, exit_code: int = 1) -> None:
    ...


@overload
def eprint(text: str, fatal: Literal[True], exit_code: int = 1) -> NoReturn:
    ...


def eprint(text: str, fatal: bool = False, exit_code: int = 1) -> None | NoReturn:
    if text.startswith("\n"):
        text = text.lstrip("\n")
        print()
    print(f"[bold color(231) on red]ERROR:[/] [red]{text}[/]")
    if fatal:
        sys.exit(exit_code)
    return None


def load_html(text: str) -> BeautifulSoup:
    return BeautifulSoup(text, "lxml-html")


def first_or_else(iterable, default):
    item = next(iter(iterable or []), None)
    if item is None:
        return default
    return item


def first_or_none(iterable):
    return first_or_else(iterable, None)


def find(pattern, string, group=None, flags=0):
    if group:
        if m := re.search(pattern, string, flags=flags):
            return m.group(group)
    else:
        return first_or_none(re.findall(pattern, string, flags=flags))


def first(iterable):
    return next(iter(iterable))


def generate_thumbnails(snapshots: list[Path], width: int = 300, file_type: str = "png", *, progress_obj: Progress | None = None) -> list[Path]:
    width = int(width)
    print(f"Using thumbnail width: [bold cyan]{width}[/]")

    thumbnails = []

    with progress_obj or Progress(
        TextColumn("[progress.description]{task.description}[/]"),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(elapsed_when_finished=True),
    ) as progress:
        for snap in progress.track(snapshots, description="Generating thumbnails"):
            thumb = snap.with_name(f"{snap.stem}_thumb_{width}.{file_type}")
            if not thumb.exists():
                with Image(filename=snap) as img:
                    img.resize(width, round(img.height / (img.width / width)))
                    img.depth = 8
                    img.save(filename=thumb)
                if file_type == "png":
                    oxipng.optimize(thumb)
            thumbnails.append(thumb)

    return thumbnails


def pluralize(count, singular, plural=None, include_count=True):
    plural = plural or f"{singular}s"
    form = singular if count == 1 else plural
    return f"{count} {form}" if include_count else form


def as_lists(*args):
    """Convert any input objects to list objects."""
    for item in args:
        yield item if isinstance(item, list) else [item]


def as_list(*args):
    """
    Convert any input objects to a single merged list object.

    Example:
    >>> as_list('foo', ['buzz', 'bizz'], 'bazz', 'bozz', ['bar'], ['bur'])
    ['foo', 'buzz', 'bizz', 'bazz', 'bozz', 'bar', 'bur']
    """
    if args == (None,):
        return []
    return list(itertools.chain.from_iterable(as_lists(*args)))
