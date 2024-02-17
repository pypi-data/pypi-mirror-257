# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

import contextlib
import functools
import inspect
import pathlib
import re
import sys
import traceback

from collections.abc import Callable, Sequence
from typing import Final, Generic, Literal, Optional, TypedDict, TypeVar, cast, overload

import click
import click_option_group

import no_vtf

from ._alive_progress import alive_bar
from ._click import (
    GroupedOption,
    HelpFormatter,
    OptionGroup,
    Slice,
    apply_param_default,
    echo,
    posix_tty_style,
)
from .core.image import ImageChannels, ImageDataTypes, ImageDynamicRange
from .core.image.io.file import FileIOWriteOptions
from .core.image.io.image import AnyImageIO, ImageIO, ImageIOWriteOptions
from .core.image.io.raw import AnyRawIO, RawIOWriteOptions
from .core.image.modifier import ImageModifier
from .core.image.modifier.hdr_to_ldr_modifier import HdrToLdrModifier
from .core.pipeline import ImageIOMapping, Pipeline, Quantity, Receipt
from .core.texture import Texture
from .core.texture.filter import (
    FaceFilter,
    FrameFilter,
    MipmapFilter,
    ResolutionFilter,
    SliceFilter,
    TextureCombinedFilter,
    TextureFilter,
)
from .filesystem import InputPaths, OutputDirectories
from .task_runner import ParallelRunner, SequentialRunner, TaskRunner
from .vtf import Vtf2TgaLikeNamer, VtfDecoder, VtfExtractor, VtfTexture

_T = TypeVar("_T", bound=Texture)
_T_co = TypeVar("_T_co", bound=Texture, covariant=True)

_FORMAT_SKIP: Final[Literal["skip"]] = "skip"


class _PipelineIO(TypedDict, total=False):
    image_io_write: Optional[ImageIOMapping]
    image_io_readback: Optional[ImageIOMapping]
    raw_io_write: Optional[AnyRawIO]
    raw_io_readback: Optional[AnyRawIO]


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf - Valve Texture Format Converter
    Copyright (C) b5327157

    https://git.sr.ht/~b5327157/no_vtf/
    https://pypi.org/project/no-vtf/
    https://developer.valvesoftware.com/wiki/no_vtf

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, version 3 only.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    echo(inspect.cleandoc(credits))
    ctx.exit()


def _show_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    echo(no_vtf.__version__)
    ctx.exit()


click.Context.formatter_class = HelpFormatter


@click.command(name="no_vtf", no_args_is_help=True)
@click.argument(
    "paths",
    metavar="[--] PATH...",
    type=click.Path(path_type=pathlib.Path, exists=True),
    required=True,
    nargs=-1,
)
@click_option_group.optgroup("Conversion mode", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--animate/--no-animate",
    cls=GroupedOption,
    help="Output animated image file (default) / output each frame individually",
    type=bool,
    default=True,
)
@click_option_group.optgroup.option(
    "--raw",
    cls=GroupedOption,
    help="Extract image data as-is (without decoding)",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup("\n  Extraction", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--mipmaps",
    "-m",
    cls=GroupedOption,
    help="Extract all mipmaps",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--low-res-img",
    cls=GroupedOption,
    help="Extract low resolution image",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--min-resolution",
    cls=GroupedOption,
    help="Minimum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--max-resolution",
    cls=GroupedOption,
    help="Maximum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--closest-resolution",
    cls=GroupedOption,
    help="Fallback to the closest resolution if no exact match",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--frames",
    cls=GroupedOption,
    help="Frames to extract",
    type=Slice(),
)
@click_option_group.optgroup.option(
    "--faces",
    cls=GroupedOption,
    help="Faces to extract",
    type=Slice(),
)
@click_option_group.optgroup.option(
    "--slices",
    cls=GroupedOption,
    help="Slices to extract",
    type=Slice(),
)
@click_option_group.optgroup(
    "\n  Image decoding (not used with --raw)",
    cls=OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--dynamic-range",
    cls=GroupedOption,
    help="Override LDR/HDR auto-detection",
    type=click.Choice(["ldr", "hdr"], case_sensitive=False),
)
@click_option_group.optgroup.option(
    "--overbright-factor",
    cls=GroupedOption,
    help="Multiplicative factor used for decoding compressed HDR textures",
    show_default=True,
    type=float,
    default=16.0,
)
@click_option_group.optgroup(
    "\n  Image postprocessing (not used with --raw)",
    cls=OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--hdr-to-ldr",
    cls=GroupedOption,
    help="Convert HDR from linear sRGB to sRGB and output as clipped LDR",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--separate-channels",
    cls=GroupedOption,
    help="Output the RGB/L and A channels separately",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup(
    "\n  Image output (not used with --raw)",
    cls=OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--ldr-format",
    "-f",
    cls=GroupedOption,
    help="LDR output format",
    metavar="SINGLE[|MULTI]",
    show_default=True,
    type=str,
    default="tiff|apng",
)
@click_option_group.optgroup.option(
    "--hdr-format",
    "-F",
    cls=GroupedOption,
    help="HDR output format",
    metavar="SINGLE[|MULTI]",
    show_default=True,
    type=str,
    default="exr",
)
@click_option_group.optgroup.option(
    "--fps",
    cls=GroupedOption,
    help="Frame rate used for animated image files",
    show_default=True,
    type=int,
    default=5,
)
@click_option_group.optgroup.option(
    "--compress/--no-compress",
    cls=GroupedOption,
    help="Control lossless compression",
    type=bool,
    default=None,
)
@click_option_group.optgroup("\n  Read/write control", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "write",
    "--always-write/--no-write",
    cls=GroupedOption,
    help="Write images",
    type=bool,
    default=None,
)
@click_option_group.optgroup.option(
    "readback",
    "--readback/--no-readback",
    cls=GroupedOption,
    help="Readback images",
    type=bool,
    default=False,
)
@click_option_group.optgroup("\n  Output destination", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--output-dir",
    "-o",
    "output_directory",
    cls=GroupedOption,
    help="Output directory",
    metavar="PATH",
    type=click.Path(path_type=pathlib.Path, exists=True, file_okay=False, dir_okay=True),
)
@click_option_group.optgroup.option(
    "--output-file",
    "-O",
    cls=GroupedOption,
    help="Output file",
    metavar="PATH",
    type=click.Path(path_type=pathlib.Path, file_okay=True, dir_okay=False),
)
@click_option_group.optgroup("\n  Miscellaneous", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--num-workers",
    cls=GroupedOption,
    help="Number of workers for parallel conversion",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--no-progress",
    cls=GroupedOption,
    help="Do not show the progress bar",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup("\n  Info", cls=OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.help_option("--help", "-h", cls=GroupedOption)
@click_option_group.optgroup.option(
    "--version",
    cls=GroupedOption,
    help="Show the version and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_version,
)
@click_option_group.optgroup.option(
    "--credits",
    cls=GroupedOption,
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main_command(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    output_file: Optional[pathlib.Path],
    ldr_format: str,
    hdr_format: str,
    dynamic_range: Optional[ImageDynamicRange],
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
    animate: bool,
    fps: int,
    separate_channels: bool,
    overbright_factor: float,
    hdr_to_ldr: bool,
    low_res_img: bool,
    compress: Optional[bool],
    raw: bool,
    write: Optional[bool],
    readback: bool,
    num_workers: Optional[int],
    no_progress: bool,
) -> None:
    """
    Convert Valve Texture Format files into standard image files.

    PATH can be either file, or directory (in which case it is recursively searched
    for .vtf files, symbolic links are not followed). Multiple paths may be provided.

    As the output path, it is possible to specify either file or directory.

    Specifying the output file is useful mostly for single-file conversions,
    with filters to ensure the output file will be written only once.

    If the output directory is not specified, images are output into the source directories
    (in-place conversion). Otherwise, directory tree for any found files will be reconstructed
    in the chosen directory.

    Output LDR/HDR format is selected by its common file name extension. It is recommended selecting
    one of the specifically supported image formats (PNG, APNG, TGA, TIFF, EXR). Other image formats
    have not been validated to work, but can be still selected. A secondary format specifically used
    to output animated image files can be selected after '|' (see default LDR format as an example).
    The "skip" format can be used to skip the write step entirely.

    For the specifically supported image formats, compression is configurable when saving the image.
    Lossless compression is enabled by default. Lossy compression is not used.

    The BGRA8888 format can store both LDR and compressed HDR images.
    The specific type is either auto-detected by looking at the input file name
    (roughly, if it contains "hdr" near the end), or can be set manually.

    It is possible to filter images to convert by min/max resolution (width & height),
    and by frames/faces/slices. The former supports exact or closest match. The latter
    supports selection by single index or via Python slicing:
    https://python-reference.readthedocs.io/en/latest/docs/brackets/slicing.html

    Face index mapping: right (0), left, back, front, up, down, sphere map (6).

    After applying filters, only the highest-resolution mipmap is converted by default.
    Alternatively, all mipmaps of the high-resolution image can be converted.

    Animated textures are converted into an animated multi-frame image file by default.
    Alternatively, they can also be converted into single-frame images with animation disabled.

    The RGB/L and A channels are packed into one file by default.
    When output separately, resulting file names will be suffixed with "_rgb", "_l" or "_a".

    By default, image files are only written if they do not exist already.
    Alternatively, they can be overwritten, or writing can be disabled entirely.

    Images can also be read back to verify they have been written properly.
    Readback will error if data to be written do not match what is in the file.

    Worker is spawned for each logical core to run the conversion in parallel.
    Number of workers can be overridden. If set to 1, conversion is sequential.
    Sequential conversion enables more verbose errors to be printed.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    Upon a recoverable error, conversion will proceed with the next file.
    """

    main(
        paths=paths,
        output_directory=output_directory,
        output_file=output_file,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        dynamic_range=dynamic_range,
        mipmaps=mipmaps,
        min_resolution=min_resolution,
        max_resolution=max_resolution,
        closest_resolution=closest_resolution,
        frames=frames,
        faces=faces,
        slices=slices,
        animate=animate,
        fps=fps,
        separate_channels=separate_channels,
        overbright_factor=overbright_factor,
        hdr_to_ldr=hdr_to_ldr,
        low_res_img=low_res_img,
        compress=compress,
        raw=raw,
        write=write,
        readback=readback,
        num_workers=num_workers,
        no_progress=no_progress,
    )


def main(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
    ldr_format: Optional[str] = None,
    hdr_format: Optional[str] = None,
    dynamic_range: Optional[ImageDynamicRange] = None,
    mipmaps: Optional[bool] = None,
    min_resolution: Optional[int] = None,
    max_resolution: Optional[int] = None,
    closest_resolution: Optional[bool] = None,
    frames: Optional[slice] = None,
    faces: Optional[slice] = None,
    slices: Optional[slice] = None,
    animate: Optional[bool] = None,
    fps: Optional[int] = None,
    separate_channels: Optional[bool] = None,
    overbright_factor: Optional[float] = None,
    hdr_to_ldr: Optional[bool] = None,
    low_res_img: Optional[bool] = None,
    compress: Optional[bool] = None,
    raw: Optional[bool] = None,
    write: Optional[bool] = None,
    readback: Optional[bool] = None,
    num_workers: Optional[int] = None,
    no_progress: Optional[bool] = None,
) -> None:
    if output_file and output_directory:
        raise ValueError("Output file and directory is mutually exclusive")

    params = main_command.params
    ldr_format = apply_param_default(params, "ldr_format", str, ldr_format)
    hdr_format = apply_param_default(params, "hdr_format", str, hdr_format)
    mipmaps = apply_param_default(params, "mipmaps", bool, mipmaps)
    closest_resolution = apply_param_default(params, "closest_resolution", bool, closest_resolution)
    animate = apply_param_default(params, "animate", bool, animate)
    fps = apply_param_default(params, "fps", int, fps)
    separate_channels = apply_param_default(params, "separate_channels", bool, separate_channels)
    overbright_factor = apply_param_default(params, "overbright_factor", float, overbright_factor)
    hdr_to_ldr = apply_param_default(params, "hdr_to_ldr", bool, hdr_to_ldr)
    low_res_img = apply_param_default(params, "low_res_img", bool, low_res_img)
    raw = apply_param_default(params, "raw", bool, raw)
    readback = apply_param_default(params, "readback", bool, readback)
    no_progress = apply_param_default(params, "no_progress", bool, no_progress)

    vtf_extension_pattern = re.compile(r"\.vtf$", re.ASCII | re.IGNORECASE)

    texture_filters = _get_filters(
        mipmaps=mipmaps,
        min_resolution=min_resolution,
        max_resolution=max_resolution,
        closest_resolution=closest_resolution,
        frames=frames,
        faces=faces,
        slices=slices,
    )

    texture_extractor = VtfExtractor(low_res_img=low_res_img)
    texture_filter = TextureCombinedFilter(texture_filters)
    texture_decoder = VtfDecoder(dynamic_range=dynamic_range, overbright_factor=overbright_factor)
    texture_namer = Vtf2TgaLikeNamer(include_mipmap_level=mipmaps, include_frame=(not animate))

    modifiers: list[ImageModifier[ImageDataTypes, ImageChannels, ImageDataTypes, ImageChannels]] = (
        []
    )
    if hdr_to_ldr:
        modifiers.append(HdrToLdrModifier())

    pipeline_io, io_initializer = _create_io(
        write=write,
        readback=readback,
        raw=raw,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        compress=compress,
        fps=fps,
    )

    pipeline = Pipeline(
        input_extension_pattern=vtf_extension_pattern,
        animate=animate,
        separate_channels=separate_channels,
        extractor=texture_extractor,
        filter=texture_filter,
        decoder=texture_decoder,
        modifiers=modifiers,
        namer=texture_namer,
        **pipeline_io,
    )

    input_paths = InputPaths(paths)
    if input_paths.has_directories():
        _resolve_directories(input_paths, not no_progress)

    if output_file:
        tasks = _get_tasks(pipeline, input_paths, output_file=output_file)
    else:
        tasks = _get_tasks(pipeline, input_paths, output_directory=output_directory)

    task_runner: TaskRunner
    if (num_workers is None and len(tasks) > 1) or (num_workers and num_workers > 1):
        task_runner = ParallelRunner(max_workers=num_workers, initializer=io_initializer)
    else:
        task_runner = SequentialRunner()

    exit_status, io_ready, io_done = _process_tasks(task_runner, tasks, not no_progress)

    if write is None and not readback and tasks and exit_status == 0 and io_ready and not io_done:
        message = (
            click.style("Warning", fg="yellow")
            + ": No file was written. Did you mean to use the "
            + click.style("--always-write", bold=True)
            + " option?"
        )
        echo(message, file=sys.stderr)

    sys.exit(exit_status)


def _get_filters(
    *,
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
) -> Sequence[TextureFilter[VtfTexture]]:
    texture_filters: list[TextureFilter[VtfTexture]] = []

    if frames:
        texture_filters.append(FrameFilter(frames=frames))
    if faces:
        texture_filters.append(FaceFilter(faces=faces))
    if slices:
        texture_filters.append(SliceFilter(slices=slices))
    if min_resolution is not None or max_resolution is not None:
        texture_filters.append(
            ResolutionFilter(
                min=min_resolution, max=max_resolution, closest_as_fallback=closest_resolution
            )
        )
    if not mipmaps:
        texture_filters.append(MipmapFilter(mipmap_levels=slice(-1, None), last="filtered"))

    return texture_filters


def _create_io(
    *,
    write: Optional[bool],
    readback: bool,
    raw: bool,
    ldr_format: str,
    hdr_format: str,
    compress: Optional[bool],
    fps: Optional[int],
) -> tuple[_PipelineIO, Optional[Callable[[], None]]]:
    base_write_defaults = FileIOWriteOptions()
    base_write_defaults.overwrite = write is True

    pipeline_io = _PipelineIO()
    io_initializer: Optional[Callable[[], None]] = None
    if not raw:
        ldr_format_split = ldr_format.split("|")
        hdr_format_split = hdr_format.split("|")

        non_skip_formats = [
            format_ for format_ in ldr_format_split + hdr_format_split if format_ != _FORMAT_SKIP
        ]
        io_initializer = functools.partial(ImageIO.initialize, non_skip_formats)
        io_initializer()

        ldr_format_single: Final = ldr_format_split[0]
        hdr_format_single: Final = hdr_format_split[0]

        ldr_format_multi: Final = (ldr_format_split[1:2] or ldr_format_split[0:1])[0]
        hdr_format_multi: Final = (hdr_format_split[1:2] or hdr_format_split[0:1])[0]

        image_io_write_defaults = ImageIOWriteOptions().merge(base_write_defaults)
        image_io_write_defaults.fps = fps
        image_io_write_defaults.compress = compress

        image_io: dict[tuple[Quantity, ImageDynamicRange], AnyImageIO] = {}
        if image_io_ldr_single := _create_image_io(ldr_format_single, image_io_write_defaults):
            image_io["single", "ldr"] = image_io_ldr_single
        if image_io_hdr_single := _create_image_io(hdr_format_single, image_io_write_defaults):
            image_io["single", "hdr"] = image_io_hdr_single
        if image_io_ldr_multi := _create_image_io(ldr_format_multi, image_io_write_defaults):
            image_io["multi", "ldr"] = image_io_ldr_multi
        if image_io_hdr_multi := _create_image_io(hdr_format_multi, image_io_write_defaults):
            image_io["multi", "hdr"] = image_io_hdr_multi

        pipeline_io["image_io_write"] = image_io if write is not False else None
        pipeline_io["image_io_readback"] = image_io if readback else None
    else:
        raw_io_write_defaults = RawIOWriteOptions().merge(base_write_defaults)
        raw_io = AnyRawIO(write_defaults=raw_io_write_defaults)

        pipeline_io["raw_io_write"] = raw_io if write is not False else None
        pipeline_io["raw_io_readback"] = raw_io if readback else None

    return pipeline_io, io_initializer


def _create_image_io(
    output_format: str,
    write_defaults: ImageIOWriteOptions,
    *,
    _unhandled_compression_formats: list[str] = [],
) -> Optional[AnyImageIO]:
    if output_format == _FORMAT_SKIP:
        return None

    image_io = AnyImageIO(image_io_format=output_format, write_defaults=write_defaults)

    if (
        write_defaults.compress is not None
        and ImageIOWriteOptions(image_io.write_defaults).compress is None
        and output_format not in _unhandled_compression_formats
    ):
        message = (
            click.style("Warning", fg="yellow")
            + ": Format "
            + click.style(image_io.image_io_format, bold=True)
            + " does not support compression control."
        )
        echo(message, file=sys.stderr)

        _unhandled_compression_formats.append(image_io.image_io_format)

    return image_io


def _resolve_directories(input_paths: InputPaths, show_progress: bool) -> None:
    progress_bar_manager = alive_bar(receipt=False) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for file in input_paths.search_in_directories("*.[vV][tT][fF]", add_results=True):
            if progress_bar:
                progress_bar.text = posix_tty_style(file.name, io=sys.stderr, bold=True)
                progress_bar()
        input_paths.remove_directories()


@overload
def _get_tasks(
    pipeline: Pipeline[_T], input_paths: InputPaths, *, output_directory: Optional[pathlib.Path]
) -> Sequence[_Task[_T]]: ...


@overload
def _get_tasks(
    pipeline: Pipeline[_T], input_paths: InputPaths, *, output_file: pathlib.Path
) -> Sequence[_Task[_T]]: ...


def _get_tasks(
    pipeline: Pipeline[_T],
    input_paths: InputPaths,
    *,
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
) -> Sequence[_Task[_T]]:
    output_directories = OutputDirectories(output_directory)

    tasks: list[_Task[_T]] = []
    for input_file, input_base_directory in input_paths:
        if output_file:
            task = _Task(pipeline=pipeline, input_file=input_file, output_file=output_file)
        else:
            output_directory = output_directories(input_file, input_base_directory)
            task = _Task(
                pipeline=pipeline, input_file=input_file, output_directory=output_directory
            )
        tasks.append(task)
    return tasks


def _process_tasks(
    task_runner: TaskRunner,
    tasks: Sequence[_Task[Texture]],
    show_progress: bool,
) -> tuple[int, bool, bool]:
    exit_status = 0
    io_ready = False
    io_done = False

    progress_bar_manager = alive_bar(len(tasks)) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        overwrite_warning_shown = False

        for task, result in task_runner(tasks):
            task = cast(_Task[Texture], task)
            if isinstance(result, Receipt):
                io_ready = result.io_ready or io_ready
                io_done = result.io_done or io_done

                if (
                    any(value > 1 for value in result.output_written.values())
                    and not overwrite_warning_shown
                ):
                    message = (
                        click.style("Warning", fg="yellow")
                        + ": During processing of "
                        + click.style(repr(task), bold=True)
                        + ", an output file was written to multiple times."
                        + " This can be avoided by using extraction filters."
                        + " This message will be shown only once."
                    )
                    echo(message, file=sys.stderr)

                    overwrite_warning_shown = True

                if progress_bar:
                    skipped = not result.io_done
                    progress_bar(skipped=skipped)
                    progress_bar.text = posix_tty_style(
                        str(task.input_file.name), io=sys.stderr, bold=True
                    )
            else:
                exit_status = 1

                exception: Exception = result
                formatted_exception = "".join(traceback.format_exception(exception))
                message = (
                    click.style("Error", fg="red")
                    + " while processing "
                    + click.style(repr(task), bold=True)
                    + f": {formatted_exception}"
                )
                echo(message, file=sys.stderr)

    return exit_status, io_ready, io_done


class _Task(Generic[_T_co]):
    @overload
    def __init__(
        self, *, pipeline: Pipeline[_T_co], input_file: pathlib.Path, output_directory: pathlib.Path
    ) -> None: ...

    @overload
    def __init__(
        self, *, pipeline: Pipeline[_T_co], input_file: pathlib.Path, output_file: pathlib.Path
    ) -> None: ...

    def __init__(
        self,
        *,
        pipeline: Pipeline[_T_co],
        input_file: pathlib.Path,
        output_directory: Optional[pathlib.Path] = None,
        output_file: Optional[pathlib.Path] = None,
    ) -> None:
        self.pipeline: Final = pipeline
        self.input_file: Final = input_file

        self._output_directory: Final = output_directory
        self._output_file: Final = output_file

    def __call__(self) -> Receipt:
        if self._output_file:
            return self.pipeline(self.input_file, output_file=self._output_file)
        else:
            assert self._output_directory
            return self.pipeline(self.input_file, output_directory=self._output_directory)

    def __str__(self) -> str:
        return f"{self.input_file}"

    def __repr__(self) -> str:
        return f"{str(self.input_file)!r}"
