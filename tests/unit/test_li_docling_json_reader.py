#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from quackling.llama_index.readers import DoclingJSONReader


def test_lazy_load_data():
    reader = DoclingJSONReader(parse_type=DoclingJSONReader.ParseType.JSON)

    file_path = "tests/unit/data/0_inp_dl_doc.json"
    li_docs = list(reader.lazy_load_data(file_path))
    assert len(li_docs) == 1
