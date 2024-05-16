""" A module for the Collection class, which represents a collection of indexed and searchable documents."""

from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, TypeVar, Union
from uuid import uuid4

from colbertdb.core.utils.documentutils import (
    llama_index_sentence_splitter,
    CorpusProcessor,
)
from colbertdb.core.models.colbertplaid import ColbertPLAID
from colbertdb.core.models.pydantic_models import Document


class Collection:
    """
    A class to represent a collection of indexed and searchable documents.
    """

    index_name: Union[str, None] = None
    store_name: Union[str, None] = None
    model_name: Union[str, None] = None
    model: Union[ColbertPLAID, None] = None
    corpus_processor: Optional[CorpusProcessor] = None

    @classmethod
    def create(
        cls,
        collection: List[Document],
        name: str,
        store_name: Optional[str] = "default",
        checkpoint: Union[str, Path] = ".checkpoints/colbertv2.0",
    ) -> "Collection":
        """Load a ColBERT model from a pre-trained checkpoint.

        Parameters:
            pretrained_model_name_or_path (str): Local path or huggingface model name.
            n_gpu (int): Number of GPUs to use. By default, value is -1, which means use all available GPUs or none if no GPU is available.
            verbose (int): The level of ColBERT verbosity requested. By default, 1, which will filter out most internal logs.
            index_root (Optional[str]): The root directory where indexes will be stored. If None, will use the default directory, '.ragatouille/'.

        Returns:
            cls (Collection): The current instance of Collection, with the model initialised.
        """
        instance = cls()
        instance.model = ColbertPLAID(
            index_name=name,
            store_name=store_name,
            load_from_index=False,
            checkpoint=checkpoint,
        )
        instance.index(collection, index_name=name)
        return instance

    @classmethod
    def load(cls, name: str, store_name: str = "default") -> "Collection":
        """Load an Index and the associated ColBERT encoder from an existing document index."""
        print(f"Loading index {name} from store {store_name}...")
        instance = cls()
        instance.model = ColbertPLAID(
            index_name=name, store_name=store_name, load_from_index=True
        )
        return instance

    def _process_metadata(
        self,
        document_metadatas: Optional[list[dict[Any, Any]]],
        collection_len: int,
        document_ids: Optional[list[str]] = None,
    ) -> tuple[list[str], Optional[dict[Any, Any]]]:
        print("Processing metadata...")
        if document_ids is None:
            print("Generating document IDs...")
            document_ids = [str(uuid4()) for i in range(collection_len)]
        else:
            if len(document_ids) != collection_len:
                raise ValueError("document_ids must be the same length as collection")
            if len(document_ids) != len(set(document_ids)):
                raise ValueError("document_ids must be unique")
            if any(not id.strip() for id in document_ids):
                raise ValueError("document_ids must not contain empty strings")
            if not all(isinstance(id, type(document_ids[0])) for id in document_ids):
                raise ValueError("All document_ids must be of the same type")

        if document_metadatas is not None:
            if len(document_metadatas) != collection_len:
                raise ValueError(
                    "document_metadatas must be the same length as collection"
                )
            docid_metadata_map = {
                x: y for x, y in zip(document_ids, document_metadatas)
            }
        else:
            docid_metadata_map = None

        return document_ids, docid_metadata_map

    def _process_corpus(
        self,
        collection: List[Document],
        document_splitter_fn: Optional[Callable[[str], List[str]]],
        max_document_length: int,
    ) -> Tuple[List[str], Dict[int, str], Dict[str, Dict[Any, Any]]]:
        """
        Processes a collection of documents by assigning unique IDs, splitting documents if necessary,
        applying preprocessing, and organizing metadata.
        """
        document_metadatas = [
            x.metadata if x.metadata is not None else {} for x in collection
        ]

        document_corpus = [x.content for x in collection]

        document_ids, docid_metadata_map = self._process_metadata(
            document_metadatas=document_metadatas,
            collection_len=len(collection),
        )

        if document_splitter_fn is not None:
            print("Splitting documents...")
            self.corpus_processor = CorpusProcessor(
                document_splitter_fn=document_splitter_fn,
            )
            collection_with_ids = self.corpus_processor.process_corpus(
                document_corpus,
                document_ids,
                chunk_size=max_document_length,
            )
        else:
            collection_with_ids = [
                {"document_id": x, "content": y}
                for x, y in zip(document_ids, collection)
            ]

        pid_docid_map = {
            index: item["document_id"] for index, item in enumerate(collection_with_ids)
        }

        collection = [x["content"] for x in collection_with_ids]
        return collection, pid_docid_map, docid_metadata_map

    def index(
        self,
        collection: list[Document],
        index_name: str = None,
        overwrite_index: Union[bool, str] = True,
        max_document_length: int = 256,
        split_documents: bool = True,
        document_splitter_fn: Optional[Callable] = llama_index_sentence_splitter,
        bsize: int = 32,
    ):
        """Build an index from a list of documents.

        Parameters:
            collection (list[str]): The collection of documents to index.
            document_ids (Optional[list[str]]): An optional list of document ids. Ids will be generated at index time if not supplied.
            index_name (str): The name of the index that will be built.
            overwrite_index (Union[bool, str]): Whether to overwrite an existing index with the same name.
            max_document_length (int): The maximum length of a document. Documents longer than this will be split into chunks.
            split_documents (bool): Whether to split documents into chunks.
            document_splitter_fn (Optional[Callable]): A function to split documents into chunks. If None and by default, will use the llama_index_sentence_splitter.
            preprocessing_fn (Optional[Union[Callable, list[Callable]]]): A function or list of functions to preprocess documents. If None and by default, will not preprocess documents.
            bsize (int): The batch size to use for encoding the passages.

        Returns:
            index (str): The path to the index that was built.
        """
        if not split_documents:
            document_splitter_fn = None
        collection, pid_docid_map, docid_metadata_map = self._process_corpus(
            collection,
            document_splitter_fn,
            max_document_length,
        )
        return self.model.index(
            collection,
            pid_docid_map=pid_docid_map,
            docid_metadata_map=docid_metadata_map,
            index_name=index_name,
            max_document_length=max_document_length,
            overwrite=overwrite_index,
            bsize=bsize,
        )

    def add_to_index(
        self,
        collection: list[Document],
        split_documents: bool = True,
        document_splitter_fn: Optional[Callable] = llama_index_sentence_splitter,
        bsize: int = 32,
    ):
        """Add documents to an existing index.

        Parameters:
            collection (list[str]): The documents to add to the index.
            new_document_metadatas (Optional[list[dict]]): An optional list of metadata dicts
            bsize (int): The batch size to use for encoding the passages.
        """
        if not split_documents:
            document_splitter_fn = None

        (
            new_collection,
            new_pid_docid_map,
            new_docid_metadata_map,
        ) = self._process_corpus(
            collection,
            document_splitter_fn,
            self.model.config.doc_maxlen,
        )

        self.model.add_to_index(
            new_collection,
            new_pid_docid_map,
            new_docid_metadata_map=new_docid_metadata_map,
            bsize=bsize,
        )

    def delete_from_index(
        self,
        document_ids: Union[TypeVar("T"), List[TypeVar("T")]],
        index_name: Optional[str] = None,
    ):
        """Delete documents from an index by their IDs.

        Parameters:
            document_ids (Union[TypeVar("T"), List[TypeVar("T")]]): The IDs of the documents to delete.
            index_name (Optional[str]): The name of the index to delete documents from. If None and by default, will delete documents from the already initialised one.
        """
        self.model.delete_from_index(
            document_ids,
            index_name=index_name,
        )

    def delete(self):
        """Delete the index and the associated ColBERT encoder."""
        self.model.delete()

    def search(
        self,
        query: Union[str, list[str]],
        index_name: Optional["str"] = None,
        k: int = 10,
        force_fast: bool = False,
        zero_index_ranks: bool = False,
        doc_ids: Optional[list[str]] = None,
        **kwargs,
    ):
        """Query an index.

        Parameters:
            query (Union[str, list[str]]): The query or list of queries to search for.
            index_name (Optional[str]): Provide the name of an index to query. If None and by default, will query an already initialised one.
            k (int): The number of results to return for each query.
            force_fast (bool): Whether to force the use of a faster but less accurate search method.
            zero_index_ranks (bool): Whether to zero the index ranks of the results. By default, result rank 1 is the highest ranked result

        Returns:
            results (Union[list[dict], list[list[dict]]]): A list of dict containing individual results for each query. If a list of queries is provided, returns a list of lists of dicts. Each result is a dict with keys `content`, `score`, `rank`, and 'document_id'. If metadata was indexed for the document, it will be returned under the "document_metadata" key.

        Individual results are always in the format:
        ```python3
        {"content": "text of the relevant passage", "score": 0.123456, "rank": 1, "document_id": "x"}
        ```
        or
        ```python3
        {"content": "text of the relevant passage", "score": 0.123456, "rank": 1, "document_id": "x", "document_metadata": {"metadata_key": "metadata_value", ...}}
        ```

        """
        k = k if k else 10
        return self.model.search(
            query=query,
            index_name=index_name,
            k=k,
            force_fast=force_fast,
            zero_index_ranks=zero_index_ranks,
            doc_ids=doc_ids,
            **kwargs,
        )

    def rerank(
        self,
        query: Union[str, list[str]],
        documents: list[str],
        k: int = 10,
        zero_index_ranks: bool = False,
        bsize: Union[Literal["auto"], int] = "auto",
    ):
        """Encode documents and rerank them in-memory. Performance degrades rapidly with more documents.

        Parameters:
            query (Union[str, list[str]]): The query or list of queries to search for.
            documents (list[str]): The documents to rerank.
            k (int): The number of results to return for each query.
            zero_index_ranks (bool): Whether to zero the index ranks of the results. By default, result rank 1 is the highest ranked result
            bsize (int): The batch size to use for re-ranking.

        Returns:
            results (Union[list[dict], list[list[dict]]]): A list of dict containing individual results for each query. If a list of queries is provided, returns a list of lists of dicts. Each result is a dict with keys `content`, `score` and `rank`.

        Individual results are always in the format:
        ```python3
        {"content": "text of the relevant passage", "score": 0.123456, "rank": 1}
        ```
        """

        return self.model.rank(
            query=query,
            documents=documents,
            k=k,
            zero_index_ranks=zero_index_ranks,
            bsize=bsize,
        )

    def encode(
        self,
        documents: list[str],
        bsize: Union[Literal["auto"], int] = "auto",
        document_metadatas: Optional[list[dict]] = None,
        verbose: bool = True,
        max_document_length: Union[Literal["auto"], int] = "auto",
    ):
        """Encode documents in memory to be searched through with no Index. Performance degrades rapidly with more documents.

        Parameters:
            documents (list[str]): The documents to encode.
            bsize (int): The batch size to use for encoding.
            document_metadatas (Optional[list[dict]]): An optional list of metadata dicts. Each entry must correspond to a document.
        """
        if verbose:
            print(f"Encoding {len(documents)} documents...")
        self.model.encode(
            documents=documents,
            bsize=bsize,
            document_metadatas=document_metadatas,
            verbose=verbose,
            max_tokens=max_document_length,
        )
        if verbose:
            print("Documents encoded!")

    def search_encoded_docs(
        self,
        query: Union[str, list[str]],
        k: int = 10,
        bsize: int = 32,
    ) -> list[dict[str, Any]]:
        """Search through documents encoded in-memory.

        Parameters:
            query (Union[str, list[str]]): The query or list of queries to search for.
            k (int): The number of results to return for each query.
            batch_size (int): The batch size to use for searching.

        Returns:
            results (list[dict[str, Any]]): A list of dict containing individual results for each query. If a list of queries is provided, returns a list of lists of dicts.
        """
        return self.model.search_encoded_docs(
            queries=query,
            k=k,
            bsize=bsize,
        )

    def clear_encoded_docs(self, force: bool = False):
        """Clear documents encoded in-memory.

        Parameters:
            force (bool): Whether to force the clearing of encoded documents without enforcing a 10s wait time.
        """
        self.model.clear_encoded_docs(force=force)
