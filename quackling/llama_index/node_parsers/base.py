#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from pydantic import BaseModel


class NodeMetadata(BaseModel):
    class ExcludedKeys:
        _COMMON = [
            "path",
        ]
        LLM = _COMMON
        EMBED = _COMMON

    path: str
    # dl_doc_id: str  # unnecessary due to source relationship
