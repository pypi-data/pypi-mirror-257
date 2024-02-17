# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal

import numpy as np
import numpy.typing as npt

from no_vtf.core.image import ImageWithRawData
from no_vtf.functional import Deferred

from .ndarray import image_bytes_to_ndarray


def decode_rgb_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgb"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgb")


def decode_rgba_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_argb_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (1, 2, 3, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_bgr_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgb"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (2, 1, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgb")


def decode_bgra_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (2, 1, 0, 3), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_abgr_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (3, 2, 1, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_rgba_uint16_be(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint16, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint16, ">")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.uint16), channels="rgba"
    )


def decode_rgba_uint16_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint16, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint16, "<")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.uint16), channels="rgba"
    )


def decode_rgba_float16_be(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.float16, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.float16, ">")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.float16), channels="rgba"
    )


def decode_rgba_float16_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.float16, Literal["rgba"]]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.float16, "<")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.float16), channels="rgba"
    )


def decode_l_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["l"]]:
    data = Deferred(lambda: image_bytes_to_ndarray(encoded_image, width, height, (0,), np.uint8))
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="l")


def decode_a_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["a"]]:
    data = Deferred(lambda: image_bytes_to_ndarray(encoded_image, width, height, (0,), np.uint8))
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="a")


def decode_la_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["la"]]:
    la_uint8 = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)
    )
    return ImageWithRawData(
        raw=encoded_image, data=la_uint8, dtype=np.dtype(np.uint8), channels="la"
    )


def decode_uv_uint8(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgb"]]:
    def thunk() -> npt.NDArray[np.uint8]:
        rg_uint8 = image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)
        b_uint8: npt.NDArray[np.uint8] = np.zeros(rg_uint8.shape[:-1], dtype=np.uint8)
        rgb_uint8: npt.NDArray[np.uint8] = np.dstack((rg_uint8, b_uint8))
        return rgb_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgb"
    )


def decode_bgra_uint4_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8, Literal["rgba"]]:
    def thunk() -> npt.NDArray[np.uint8]:
        bgra_uint4 = image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)

        br_uint8 = np.bitwise_and(np.left_shift(bgra_uint4, 4), 0xF0)
        ga_uint8 = np.bitwise_and(bgra_uint4, 0xF0)

        r_uint8 = br_uint8[..., [1]]
        g_uint8 = ga_uint8[..., [0]]
        b_uint8 = br_uint8[..., [0]]
        a_uint8 = ga_uint8[..., [1]]

        rgba_uint8: npt.NDArray[np.uint8] = np.dstack((r_uint8, g_uint8, b_uint8, a_uint8))
        return rgba_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )
