#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from enum import Enum
from typing import Iterable

from docling.document_converter import DocumentConverter
from docling_core.types import Document as DLDocument
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document as LIDocument

from quackling.llama_index.readers.base import DocumentMetadata


class DoclingReader(BasePydanticReader):
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

    def lazy_load_data(self, file_path: str | list[str]) -> Iterable[LIDocument]:

        file_paths = file_path if isinstance(file_path, list) else [file_path]

        converter = DocumentConverter()
        for source in file_paths:
            dl_doc = converter.convert_single(source)
            li_doc = self._create_li_doc_from_dl_doc(dl_doc=dl_doc)
            yield li_doc
