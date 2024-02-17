# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools

from typing import Literal

import numpy as np
import numpy.typing as npt
import PIL.BlpImagePlugin
import PIL.Image

from no_vtf.core.image import ImageWithRawData
from no_vtf.functional import Deferred


def decode_dxt1_rgb(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8, Literal["rgb"]]:
    def thunk() -> npt.NDArray[np.uint8]:
        rgba_uint8 = _decode_dxt_generic(
            encoded_image, logical_width, logical_height, n=1, pixel_format="DXT1"
        )
        rgb_uint8: npt.NDArray[np.uint8] = rgba_uint8[..., :3]
        return rgb_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgb"
    )


def decode_dxt1_rgba(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, n=1, pixel_format="DXT1"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def decode_dxt3(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, n=2, pixel_format="DXT3"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def decode_dxt5(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, n=3, pixel_format="DXT5"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def _decode_dxt_generic(
    encoded_image: bytes, logical_width: int, logical_height: int, *, n: int, pixel_format: str
) -> npt.NDArray[np.uint8]:
    physical_width, physical_height = _dxt_physical_dimensions(logical_width, logical_height)

    # reference for "n" and "pixel_format": Pillow/src/PIL/DdsImagePlugin.py
    pil_image = PIL.Image.frombytes(  # pyright: ignore [reportUnknownMemberType]
        "RGBA", (physical_width, physical_height), encoded_image, "bcn", n, pixel_format
    )

    rgba_uint8: npt.NDArray[np.uint8] = np.array(pil_image)
    rgba_uint8 = rgba_uint8[:logical_height, :logical_width, :]
    return rgba_uint8


def _dxt_physical_dimensions(logical_width: int, logical_height: int) -> tuple[int, int]:
    physical_width = _dxt_physical_length(logical_width)
    physical_height = _dxt_physical_length(logical_height)
    return physical_width, physical_height


def _dxt_physical_length(logical_length: int) -> int:
    physical_length = (max(logical_length, 4) + 3) // 4 * 4
    return physical_length
