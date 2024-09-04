#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from typing import Iterable

from docling.document_converter import DocumentConverter
from llama_index.core.schema import Document as LIDocument
from typing_extensions import deprecated

from quackling.llama_index.readers.base import BaseDoclingReader


@deprecated("Use `quackling.llama_index.readers.DoclingPDFReader` instead.")
class DoclingReader(BaseDoclingReader):
    def lazy_load_data(self, file_path: str | list[str]) -> Iterable[LIDocument]:

        file_paths = file_path if isinstance(file_path, list) else [file_path]

        converter = DocumentConverter()
        for source in file_paths:
            dl_doc = converter.convert_single(source).output
            li_doc = self._create_li_doc_from_dl_doc(dl_doc=dl_doc)
            yield li_doc
