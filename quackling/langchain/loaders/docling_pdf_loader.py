#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from typing import Iterator

from langchain_core.documents import Document as LCDocument

from quackling.langchain.loaders.base import BaseDoclingLoader


class DoclingPDFLoader(BaseDoclingLoader):

    def lazy_load(self) -> Iterator[LCDocument]:
        for source in self._file_paths:
            dl_doc = self._converter.convert_single(source).output
            lc_doc = self._create_lc_doc_from_dl_doc(dl_doc=dl_doc)
            yield lc_doc
