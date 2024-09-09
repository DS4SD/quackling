#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from enum import Enum

from docling.document_converter import DocumentConverter
from docling_core.types import Document as DLDocument
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    dl_doc_hash: str
    # source: str


class BaseDoclingLoader(BaseLoader):
    class ParseType(str, Enum):
        MARKDOWN = "markdown"
        JSON = "json"

    def __init__(self, file_path: str | list[str], parse_type: ParseType) -> None:
        self._file_paths = file_path if isinstance(file_path, list) else [file_path]
        self._parse_type = parse_type
        self._converter = DocumentConverter()

    def _create_lc_doc_from_dl_doc(self, dl_doc: DLDocument) -> LCDocument:
        if self._parse_type == self.ParseType.MARKDOWN:
            text = dl_doc.export_to_markdown()
        elif self._parse_type == self.ParseType.JSON:
            text = dl_doc.model_dump_json()
        else:
            raise RuntimeError(f"Unexpected parse type encountered: {self._parse_type}")
        lc_doc = LCDocument(
            page_content=text,
            metadata=DocumentMetadata(
                dl_doc_hash=dl_doc.file_info.document_hash,
            ).model_dump(),
        )
        return lc_doc
