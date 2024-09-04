<p align="center">
  <a href="https://github.com/DS4SD/quackling">
    <img loading="lazy" alt="Quackling" src="https://raw.githubusercontent.com/DS4SD/quackling/main/resources/logo.jpeg" width="150" />
  </a>
</p>

# Quackling

[![PyPI version](https://img.shields.io/pypi/v/quackling)](https://pypi.org/project/quackling/)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License MIT](https://img.shields.io/github/license/DS4SD/quackling)](https://opensource.org/licenses/MIT)

Quackling enables document-native generative AI applications, such as RAG, based on [Docling](https://github.com/DS4SD/docling).

## Features

- 🧠 Enables rich gen AI applications by providing capabilities on native document level — not just plain text / Markdown!
- ⚡️ Leverages Docling's conversion quality and speed.
- ⚙️ Integrates with standard LLM application frameworks, such as LlamaIndex, for building powerful applications like RAG.

<p align="center">
  <a href="https://raw.githubusercontent.com/DS4SD/quackling/main/resources/doc_native_rag.png">
    <img loading="lazy" alt="Doc-native RAG" src="https://raw.githubusercontent.com/DS4SD/quackling/main/resources/doc_native_rag.png" width="350" />
  </a>
</p>


## Installation

To use Quackling, simply install `quackling` from your package manager, e.g. pip:

```sh
pip install quackling
```

## Usage

Quackling offers core capabilities (`quackling.core`), as well as framework integration components
e.g. for LlamaIndex (`quackling.llama_index`). Below you find examples of both.

### Basic RAG

Below you find a basic RAG pipeline using LlamaIndex.

> [!NOTE]
> To use as is, first `pip install llama-index-embeddings-huggingface llama-index-llms-huggingface-api`
> additionally to `quackling` to install the models.
> Otherwise, you can set `EMBED_MODEL` & `LLM` as desired, e.g. using
> [local models](https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local).

```python
import os

from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from quackling.llama_index.node_parsers import HierarchicalJSONNodeParser
from quackling.llama_index.readers import DoclingPDFReader

DOCS = ["https://arxiv.org/pdf/2206.01062"]
QUESTION = "How many pages were human annotated?"
EMBED_MODEL = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
LLM = HuggingFaceInferenceAPI(
    token=os.getenv("HF_TOKEN"),
    model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
)

index = VectorStoreIndex.from_documents(
    documents=DoclingPDFReader(parse_type=DoclingPDFReader.ParseType.JSON).load_data(DOCS),
    embed_model=EMBED_MODEL,
    transformations=[HierarchicalJSONNodeParser()],
)
query_engine = index.as_query_engine(llm=LLM)
result = query_engine.query(QUESTION)
print(result.response)
# > 80K pages were human annotated
```

### Chunking

You can also use Quackling as a standalone with any pipeline.
For instance, to split the document to chunks based on document structure and returning pointers
to Docling document's nodes:

```python
from docling.document_converter import DocumentConverter
from quackling.core.chunkers import HierarchicalChunker

doc = DocumentConverter().convert_single("https://arxiv.org/pdf/2408.09869").output
chunks = list(HierarchicalChunker().chunk(doc))
# > [
# >     ChunkWithMetadata(
# >         path='$.main-text[4]',
# >         text='Docling Technical Report\n[...]',
# >         page=1,
# >         bbox=[117.56, 439.85, 494.07, 482.42]
# >     ),
# >     [...]
# > ]
```

## More examples
Check out the [examples](examples) — showcasing different variants of RAG incl. vector ingestion & retrieval:
- [[LlamaIndex] Milvus basic RAG (dense embeddings)](examples/basic_pipeline.ipynb)
- [[LlamaIndex] Milvus hybrid RAG (dense & sparse embeddings combined e.g. via RRF) & reranker model usage](examples/hybrid_pipeline.ipynb)
- [[LlamaIndex] Milvus RAG also fetching native document metadata for search results](examples/native_nodes.ipynb)
- [[LlamaIndex] Local node transformations (e.g. embeddings)](examples/node_transformations.ipynb)
- ...

## Contributing

Please read [Contributing to Quackling](./CONTRIBUTING.md) for details.

## References

If you use Quackling in your projects, please consider citing the following:

```bib
@techreport{Docling,
  author = "Deep Search Team",
  month = 8,
  title = "Docling Technical Report",
  url = "https://arxiv.org/abs/2408.09869",
  eprint = "2408.09869",
  doi = "10.48550/arXiv.2408.09869",
  version = "1.0.0",
  year = 2024
}
```

## License

The Quackling codebase is under MIT license.
For individual component usage, please refer to the component licenses found in the original packages.
