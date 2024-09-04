#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

import json
from typing import Iterable

from docling_core.types import Document as DLDocument
from llama_index.core.schema import Document as LIDocument

from quackling.llama_index.readers.base import BaseDoclingReader


class DoclingJSONReader(BaseDoclingReader):
    def lazy_load_data(self, file_path: str | list[str]) -> Iterable[LIDocument]:

        file_paths = file_path if isinstance(file_path, list) else [file_path]

        for source in file_paths:
            with open(source, encoding="utf-8") as file_obj:
                data = json.load(file_obj)
            dl_doc: DLDocument = DLDocument.model_validate(data)
            li_doc: LIDocument = self._create_li_doc_from_dl_doc(dl_doc=dl_doc)
            yield li_doc
