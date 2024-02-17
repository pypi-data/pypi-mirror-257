# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import Final

from no_vtf.core.texture import Texture
from no_vtf.typing import mypyc_attr

from .filter import TextureFilter


@mypyc_attr(allow_interpreted_subclasses=True)
class FrameFilter(TextureFilter[Texture]):
    def __init__(self, *, frames: slice, strict: bool = False) -> None:
        self.frames: Final = frames
        self.strict: Final = strict

    def __call__(self, textures: Sequence[Texture]) -> Sequence[Texture]:
        if not textures:
            return []

        frame_counts = {texture.frame.count for texture in textures if texture.frame}
        if not frame_counts:
            return [] if self.strict else textures

        if len(frame_counts) != 1:
            raise ValueError("Frame count must be the same for all filtered textures")

        indices = range(*self.frames.indices(next(iter(frame_counts))))

        textures_filtered: list[Texture] = []
        for index in indices:
            textures_filtered.extend(
                texture
                for texture in textures
                if (texture.frame and texture.frame.index == index)
                or (not self.strict and not texture.frame)
            )
        return textures_filtered
