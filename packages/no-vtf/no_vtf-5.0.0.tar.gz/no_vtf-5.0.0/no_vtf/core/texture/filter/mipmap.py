# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import Final, Literal, Union

from no_vtf.core.texture import Texture
from no_vtf.typing import mypyc_attr

from .filter import TextureFilter


@mypyc_attr(allow_interpreted_subclasses=True)
class MipmapFilter(TextureFilter[Texture]):
    def __init__(
        self,
        *,
        mipmap_levels: slice,
        last: Union[Literal["original"], Literal["filtered"]] = "original",
        strict: bool = False,
    ) -> None:
        self.mipmap_levels: Final = mipmap_levels
        self.last: Final = last
        self.strict: Final = strict

    def __call__(self, textures: Sequence[Texture]) -> Sequence[Texture]:
        if not textures:
            return []

        mipmap_counts = {texture.mipmap.count for texture in textures if texture.mipmap}
        if not mipmap_counts:
            return [] if self.strict else textures

        length: int
        if self.last == "original":
            if len(mipmap_counts) != 1:
                raise ValueError("Mipmap count must be the same for all filtered textures")

            length = next(iter(mipmap_counts))
        else:
            length = max(texture.mipmap.index for texture in textures if texture.mipmap) + 1

        indices = range(*self.mipmap_levels.indices(length))

        textures_filtered: list[Texture] = []
        for index in indices:
            textures_filtered.extend(
                texture
                for texture in textures
                if (texture.mipmap and texture.mipmap.index == index)
                or (not self.strict and not texture.mipmap)
            )
        return textures_filtered
