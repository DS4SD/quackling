#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from typing import Iterable, List

from docling_core.types import Document as DLDocument
from langchain_core.documents import Document as LCDocument
from pydantic import BaseModel

from quackling.core.chunkers.base import BaseChunker
from quackling.core.chunkers.hierarchical_chunker import HierarchicalChunker


class ChunkDocMetadata(BaseModel):
    dl_doc_id: str
    path: str


class HierarchicalJSONSplitter:

    def __init__(
        self,
        chunker: BaseChunker | None = None,
    ) -> None:
        self.chunker: BaseChunker = chunker or HierarchicalChunker()

    def split_documents(self, documents: Iterable[LCDocument]) -> List[LCDocument]:

        all_chunk_docs: list[LCDocument] = []
        for doc in documents:
            lc_doc: LCDocument = LCDocument.parse_obj(doc)
            dl_doc: DLDocument = DLDocument.model_validate_json(lc_doc.page_content)
            chunk_iter = self.chunker.chunk(dl_doc=dl_doc)
            chunk_docs = [
                LCDocument(
                    page_content=chunk.text,
                    metadata=ChunkDocMetadata(
                        dl_doc_id=dl_doc.file_info.document_hash,
                        path=chunk.path,
                    ).model_dump(),
                )
                for chunk in chunk_iter
            ]
            all_chunk_docs.extend(chunk_docs)

        return all_chunk_docs
