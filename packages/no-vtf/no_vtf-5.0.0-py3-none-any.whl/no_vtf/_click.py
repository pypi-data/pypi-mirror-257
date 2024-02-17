# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import os
import re

from collections.abc import Sequence
from typing import IO, AnyStr, Final, Optional, TextIO, TypeVar, Union

import click
import click_option_group

_T = TypeVar("_T")


class HelpFormatter(click.HelpFormatter):
    def write_usage(self, prog: str, args: str = "", prefix: Optional[str] = None) -> None:
        prog = click.style(prog, fg=127, bold=True)
        args = click.style(args, bold=True)
        super().write_usage(prog, args, prefix)

    def write_heading(self, heading: str) -> None:
        heading = click.style(heading, underline=True)
        super().write_heading(heading)


class OptionGroup(click_option_group.OptionGroup):
    def get_help_record(self, ctx: click.Context) -> Optional[tuple[str, str]]:
        help_record = super().get_help_record(ctx)
        if not help_record:
            return None

        name, help_ = help_record
        name = click.style(name, fg=172, bold=True)
        return name, help_


class GroupedOption(click_option_group.GroupedOption):
    _dim_pattern: Final[re.Pattern[str]] = re.compile(r"(?<=\s)\[[^\[\]\s]+\]", re.ASCII)

    def get_help_record(self, ctx: click.Context) -> Optional[tuple[str, str]]:
        help_record = super().get_help_record(ctx)
        if help_record is None:
            return None

        def dim_repl(match: re.Match[str]) -> str:
            return click.style(match.group(), dim=True)

        opts, opt_help = help_record
        opt_help = self._dim_pattern.sub(dim_repl, opt_help)
        return opts, opt_help


class Slice(click.ParamType):
    name = "slice"

    def get_metavar(self, param: click.Parameter) -> str:
        return "INDEX|[START]:[STOP][:STEP]"

    def convert(
        self,
        value: Union[str, slice],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> slice:
        if isinstance(value, slice):
            return value

        slice_indices = self._to_slice_indices(value, param, ctx)

        start = slice_indices[0]
        if len(slice_indices) == 1:
            if start is None:
                self.fail("Index is empty.", param, ctx)
            if start >= 0:
                return slice(start, start + 1)
            else:
                stop = start + 1 if start != -1 else None
                return slice(start, stop)

        stop = slice_indices[1]
        if len(slice_indices) == 2:
            return slice(start, stop)

        step = slice_indices[2]
        if len(slice_indices) == 3:
            if step == 0:
                self.fail("Slice step cannot be zero.", param, ctx)
            return slice(start, stop, step)

        self.fail(f"Too many values in {value!r}.", param, ctx)

    def _to_slice_indices(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[Optional[int]]:
        slice_indices: list[Optional[int]] = []
        for slice_index in value.split(":"):
            if not slice_index:
                slice_indices.append(None)
            else:
                try:
                    slice_indices.append(int(slice_index))
                except ValueError:
                    self.fail(f"{slice_index!r} is not a valid integer.", param, ctx)
        return slice_indices


def get_param_default(
    params: Sequence[click.core.Parameter], param_name: str, param_type: type[_T]
) -> _T:
    for param in params:
        if param.name == param_name:
            default = param.default
            if callable(default):
                default = default()

            if not isinstance(default, param_type):
                raise ValueError(f"{type(default) = } {param_type = }")

            return default

    raise ValueError(f"No such parameter: {param_name}")


def apply_param_default(
    params: Sequence[click.core.Parameter],
    param_name: str,
    param_type: type[_T],
    value: Optional[_T],
) -> _T:
    return value if value is not None else get_param_default(params, param_name, param_type)


def posix_tty_style(
    text: str,
    *,
    io: TextIO,
    fg: Optional[Union[int, tuple[int, int, int], str]] = None,
    bg: Optional[Union[int, tuple[int, int, int], str]] = None,
    bold: Optional[bool] = None,
    dim: Optional[bool] = None,
    underline: Optional[bool] = None,
    overline: Optional[bool] = None,
    italic: Optional[bool] = None,
    blink: Optional[bool] = None,
    reverse: Optional[bool] = None,
    strikethrough: Optional[bool] = None,
    reset: bool = True,
) -> str:
    if os.name == "posix" and io.isatty():
        return click.style(
            text,
            fg=fg,
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset,
        )

    return text


def echo(
    message: str,
    file: Optional[IO[AnyStr]] = None,
    nl: bool = True,
    err: bool = False,
    color: Optional[bool] = None,
) -> None:
    message = click.style("", reset=True) + message
    click.echo(message, file, nl, err, color)
