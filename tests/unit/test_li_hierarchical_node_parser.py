#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

import json

from llama_index.core.schema import Document as LIDocument

from quackling.llama_index.node_parsers import HierarchicalJSONNodeParser


def test_node_parse():
    with open("tests/unit/data/1_inp_li_doc.json") as f:
        data_json = f.read()
    li_doc = LIDocument.from_json(data_json)
    node_parser = HierarchicalJSONNodeParser(id_gen_seed=42)
    nodes = node_parser._parse_nodes(nodes=[li_doc])
    act_data = dict(root=[n.dict() for n in nodes])
    with open("tests/unit/data/1_out_nodes.json") as f:
        exp_data = json.load(fp=f)
    assert exp_data == act_data
