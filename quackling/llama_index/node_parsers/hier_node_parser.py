#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

from datetime import datetime
from random import Random
from typing import Any, Iterable, Sequence
from uuid import UUID

from docling_core.types import Document as DLDocument
from llama_index.core import Document as LIDocument
from llama_index.core.node_parser.interface import NodeParser
from llama_index.core.schema import (
    BaseNode,
    NodeRelationship,
    RelatedNodeType,
    TextNode,
)
from llama_index.core.utils import get_tqdm_iterable
from pydantic import Field

from quackling.core.chunkers.hierarchical_chunker import HierarchicalChunker
from quackling.llama_index.node_parsers.base import NodeMetadata


class HierarchicalNodeParser(NodeParser):

    # override default to False to avoid inheriting source doc's metadata
    include_metadata: bool = Field(
        default=False, description="Whether or not to consider metadata when splitting."
    )

    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        id_gen_seed: int | None = None,
        **kwargs: Any,
    ) -> list[BaseNode]:
        # based on llama_index.core.node_parser.interface.TextSplitter
        nodes_with_progress: Iterable[BaseNode] = get_tqdm_iterable(
            items=nodes, show_progress=show_progress, desc="Parsing nodes"
        )
        all_nodes: list[BaseNode] = []
        chunker = HierarchicalChunker()
        excl_meta_embed = NodeMetadata.ExcludedKeys.EMBED
        excl_meta_llm = NodeMetadata.ExcludedKeys.LLM

        seed = id_gen_seed if id_gen_seed is not None else datetime.now().timestamp()
        rd = Random()
        rd.seed(seed)

        for input_node in nodes_with_progress:
            li_doc = LIDocument.parse_obj(input_node)
            dl_doc: DLDocument = DLDocument.model_validate_json(li_doc.get_content())
            chunk_iter = chunker.chunk(dl_doc=dl_doc)
            for chunk in chunk_iter:
                rels: dict[NodeRelationship, RelatedNodeType] = {
                    NodeRelationship.SOURCE: li_doc.as_related_node_info(),
                }
                # based on llama_index.core.node_parser.node_utils.build_nodes_from_splits  # noqa
                node = TextNode(
                    id_=str(UUID(int=rd.getrandbits(128), version=4)),
                    text=chunk.text,
                    excluded_embed_metadata_keys=excl_meta_embed,
                    excluded_llm_metadata_keys=excl_meta_llm,
                    relationships=rels,
                )
                node.metadata = NodeMetadata(
                    path=chunk.path,
                ).model_dump()
                all_nodes.append(node)
        return all_nodes
