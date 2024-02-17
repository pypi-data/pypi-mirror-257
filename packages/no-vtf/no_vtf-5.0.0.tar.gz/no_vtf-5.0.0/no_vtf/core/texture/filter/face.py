# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import Final

from no_vtf.core.texture import Texture
from no_vtf.typing import mypyc_attr

from .filter import TextureFilter


@mypyc_attr(allow_interpreted_subclasses=True)
class FaceFilter(TextureFilter[Texture]):
    def __init__(self, *, faces: slice, strict: bool = False) -> None:
        self.faces: Final = faces
        self.strict: Final = strict

    def __call__(self, textures: Sequence[Texture]) -> Sequence[Texture]:
        if not textures:
            return []

        face_counts = {texture.face.count for texture in textures if texture.face}
        if not face_counts:
            return [] if self.strict else textures

        if len(face_counts) != 1:
            raise ValueError("Face count must be the same for all filtered textures")

        indices = range(*self.faces.indices(next(iter(face_counts))))

        textures_filtered: list[Texture] = []
        for index in indices:
            textures_filtered.extend(
                texture
                for texture in textures
                if (texture.face and texture.face.index == index)
                or (not self.strict and not texture.face)
            )
        return textures_filtered
