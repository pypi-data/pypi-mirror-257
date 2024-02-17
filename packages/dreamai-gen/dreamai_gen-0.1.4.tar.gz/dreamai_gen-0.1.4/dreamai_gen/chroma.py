from typing import Callable

import chromadb
from chromadb import Collection as ChromaCollection
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.documents import Document as LCDocument
from termcolor import colored

EMBEDDING_MODEL = "multi-qa-mpnet-base-cos-v1"


def chroma_collection(
    name: str,
    persistent_dir: str = "chroma_dir",
    delete_existing: bool = False,
    embedding_model: str = EMBEDDING_MODEL,
    device: str = "cuda",
) -> ChromaCollection:
    chroma_client = chromadb.PersistentClient(path=persistent_dir)
    if delete_existing:
        try:
            chroma_client.delete_collection(name)
        except Exception as e:
            print(colored(f"Error deleting collection named {name}: {e}", "red"))
            pass
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=embedding_model, device=device
    )
    collection = chroma_client.get_or_create_collection(
        name, embedding_function=embedding_function
    )
    return collection


def id_from_lc_doc(doc: LCDocument, doc_idx=None, **kwargs) -> str | None:
    """Get a unique id from an LCDocument."""

    try:
        file_name = doc.metadata["filename"]
        page_number = doc.metadata["page_number"]
        doc_id = f"{file_name}_{page_number}"
        if doc_idx is not None:
            doc_id += f"_{doc_idx}"
        return doc_id
    except Exception as e:
        print(colored(f"Error getting id from LCDocument: {e}", "red"))
        return None


def lc_docs_to_chroma_docs(
    docs: list[LCDocument], id_fn: Callable = id_from_lc_doc
) -> tuple[list[str], list[str], list[dict]]:
    """Convert a list of LCDocuments to Chroma docs with ids and metadata."""

    chroma_ids = []
    chroma_docs = []
    chroma_metadatas = []
    for i, doc in enumerate(docs):
        chroma_docs.append(doc.page_content)
        chroma_metadatas.append(
            {
                k: v
                for k, v in doc.metadata.items()
                if type(v) in [str, int, float, bool]
            }
        )
        chroma_ids.append(id_fn(doc=doc, doc_idx=i) or f"id_{i}")
    return chroma_ids, chroma_docs, chroma_metadatas
