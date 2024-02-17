# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import Final

from no_vtf.core.texture import Texture
from no_vtf.typing import mypyc_attr

from .filter import TextureFilter


@mypyc_attr(allow_interpreted_subclasses=True)
class SliceFilter(TextureFilter[Texture]):
    def __init__(self, *, slices: slice, strict: bool = False) -> None:
        self.slices: Final = slices
        self.strict: Final = strict

    def __call__(self, textures: Sequence[Texture]) -> Sequence[Texture]:
        if not textures:
            return []

        slice_counts = {texture.slice.count for texture in textures if texture.slice}
        if not slice_counts:
            return [] if self.strict else textures

        if len(slice_counts) != 1:
            raise ValueError("Slice count must be the same for all filtered textures")

        indices = range(*self.slices.indices(next(iter(slice_counts))))

        textures_filtered: list[Texture] = []
        for index in indices:
            textures_filtered.extend(
                texture
                for texture in textures
                if (texture.slice and texture.slice.index == index)
                or (not self.strict and not texture.slice)
            )
        return textures_filtered
