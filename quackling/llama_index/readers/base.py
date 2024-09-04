#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from enum import Enum

from docling_core.types import Document as DLDocument
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document as LIDocument
from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    class ExcludedKeys:
        _COMMON = [
            "dl_doc_hash",
        ]
        LLM = _COMMON
        EMBED = _COMMON

    dl_doc_hash: str
    # source: str


class BaseDoclingReader(BasePydanticReader):
    class ParseType(str, Enum):
        MARKDOWN = "markdown"
        JSON = "json"

    parse_type: ParseType = ParseType.MARKDOWN

    def _create_li_doc_from_dl_doc(self, dl_doc: DLDocument) -> LIDocument:
        if self.parse_type == self.ParseType.MARKDOWN:
            text = dl_doc.export_to_markdown()
        elif self.parse_type == self.ParseType.JSON:
            text = dl_doc.model_dump_json()
        else:
            raise RuntimeError(f"Unexpected parse type encountered: {self.parse_type}")

        li_doc = LIDocument(
            doc_id=dl_doc.file_info.document_hash,
            text=text,
            excluded_embed_metadata_keys=DocumentMetadata.ExcludedKeys.EMBED,
            excluded_llm_metadata_keys=DocumentMetadata.ExcludedKeys.LLM,
        )
        li_doc.metadata = DocumentMetadata(
            dl_doc_hash=dl_doc.file_info.document_hash,
        ).model_dump()
        return li_doc
