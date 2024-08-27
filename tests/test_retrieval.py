import json
from tempfile import TemporaryDirectory

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.milvus import MilvusVectorStore

from quackling.llama_index.node_parsers.hier_node_parser import HierarchicalNodeParser
from quackling.llama_index.readers.docling_reader import DoclingReader


def test_retrieval():
    FILE_PATH = "https://arxiv.org/pdf/2206.01062"  # DocLayNet paper
    QUERY = "How many pages were human annotated?"
    TOP_K = 3
    HF_EMBED_MODEL_ID = "BAAI/bge-small-en-v1.5"
    ID_GEN_SEED = 42
    MILVUS_DB_FNAME = "milvus_demo.db"
    MILVUS_COLL_NAME = "quackling_test_coll"

    reader = DoclingReader(parse_type=DoclingReader.ParseType.JSON)
    node_parser = HierarchicalNodeParser(id_gen_seed=ID_GEN_SEED)
    embed_model = HuggingFaceEmbedding(model_name=HF_EMBED_MODEL_ID)

    with TemporaryDirectory() as tmp_dir:
        vector_store = MilvusVectorStore(
            uri=f"{tmp_dir}/{MILVUS_DB_FNAME}",
            collection_name=MILVUS_COLL_NAME,
            dim=len(embed_model.get_text_embedding("hi")),
            overwrite=True,
        )
        docs = reader.load_data(file_path=[FILE_PATH])
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents=docs,
            storage_context=storage_context,
            transformations=[node_parser],
            embed_model=embed_model,
        )
        retriever = index.as_retriever(
            similarity_top_k=TOP_K,
            vector_store_query_mode=VectorStoreQueryMode.DEFAULT,
        )
        retr_res = retriever.retrieve(QUERY)
        act_data = dict(root=[n.text for n in retr_res])
        with open("tests/data/2_out_retrieval_results.json") as f:
            exp_data = json.load(fp=f)
        assert exp_data == act_data
