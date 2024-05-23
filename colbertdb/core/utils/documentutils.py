"""
https://github.com/bclavie/RAGatouille/blob/main/ragatouille/data/corpus_processor.py
https://github.com/bclavie/RAGatouille/blob/main/ragatouille/data/preprocessors.py
"""

from typing import Optional, Callable, List
from uuid import uuid4

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document


def llama_index_sentence_splitter(
    documents: list[str], document_ids: list[str], chunk_size=256
):
    """
    Splits the given documents into chunks of sentences for indexing.

    Args:
        documents (list[str]): A list of documents to be split into chunks.
        document_ids (list[str]): A list of document IDs corresponding to the documents.
        chunk_size (int, optional): The maximum number of characters in each chunk. Defaults to 256.

    Returns:
        list[dict]: A list of dictionaries representing the chunks, where each dictionary contains the document ID and the content of the chunk.
    """
    chunk_overlap = min(chunk_size / 4, chunk_size / 2, 64)
    chunks = []
    node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = [[Document(text=doc)] for doc in documents]
    for doc_id, doc in zip(document_ids, docs):
        chunks += [
            {"document_id": doc_id, "content": node.text} for node in node_parser(doc)
        ]
    return chunks


class CorpusProcessor:
    """
    Class to process a corpus of documents using a document splitter.
    """

    def __init__(
        self,
        document_splitter_fn: Optional[Callable] = SentenceSplitter,
    ):
        self.document_splitter_fn = document_splitter_fn

    def process_corpus(
        self,
        documents: list[str],
        document_ids: Optional[list[str]] = None,
        **splitter_kwargs,
    ) -> List[dict]:
        """
        Process a corpus of documents using the document splitter function.
        """
        document_ids = (
            [str(uuid4()) for _ in range(len(documents))]
            if document_ids is None
            else document_ids
        )
        if self.document_splitter_fn is not None:
            documents = self.document_splitter_fn(
                documents, document_ids, **splitter_kwargs
            )
        return documents
