#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

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
