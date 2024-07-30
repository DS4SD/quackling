#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from abc import ABC, abstractmethod
from typing import Iterator

from docling_core.types import BoundingBox, Document
from pydantic import BaseModel


class Chunk(BaseModel):
    path: str
    text: str


class ChunkWithMetadata(Chunk):
    page: int | None
    bbox: BoundingBox | None


class BaseChunker(BaseModel, ABC):

    @abstractmethod
    def chunk(self, dl_doc: Document, **kwargs) -> Iterator[Chunk]:
        raise NotImplementedError()
