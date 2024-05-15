"""
https://github.com/bclavie/RAGatouille/blob/main/ragatouille/models/index.py
"""

from pathlib import Path
from typing import Any, List, Optional, TypeVar, Union


from colbert import Indexer, IndexUpdater, Searcher
from colbert.indexing.collection_indexer import CollectionIndexer
from colbert.infra import ColBERTConfig

from colbertdb.lib import torch_kmeans


class PLAIDModelIndex:
    """
    A class to represent a PLAIDModelIndex.
    """

    _DEFAULT_INDEX_BSIZE = 32
    index_type = "PLAID"
    pytorch_kmeans = staticmethod(
        torch_kmeans._train_kmeans
    )  # pylint: disable=protected-access

    def __init__(self, config: ColBERTConfig) -> None:
        self.config = config
        self.searcher: Optional[Searcher] = None

    @staticmethod
    def construct(
        config: ColBERTConfig,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_name: Optional["str"] = None,
        overwrite: Union[bool, str] = "reuse",
        verbose: bool = True,
        **kwargs,
    ) -> "PLAIDModelIndex":
        """
        Constructs a PLAIDModelIndex object.

        Args:
            config (ColBERTConfig): The configuration for the ColBERT model.
            checkpoint (Union[str, Path]): The path to the checkpoint file.
            collection (List[str]): The list of documents in the collection.
            index_name (Optional[str], optional): The name of the index. Defaults to None.
            overwrite (Union[bool, str], optional): Whether to overwrite an existing index or reuse it. Defaults to "reuse".
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            PLAIDModelIndex: The constructed PLAIDModelIndex object.
        """
        []
        return PLAIDModelIndex(config).build(
            checkpoint, collection, index_name, overwrite, verbose, **kwargs
        )

    @staticmethod
    def load_from_file(
        index_path: Union[str, Path],
        index_name: Optional[str],
        index_config: dict[str, Any],
        config: ColBERTConfig,
        verbose: bool = True,
    ) -> "PLAIDModelIndex":
        """
        Load a PLAIDModelIndex from a file.

        Args:
            index_path (Union[str, Path]): The path to the index file.
            index_name (Optional[str]): The name of the index.
            index_config (dict[str, Any]): The configuration for the index.
            config (ColBERTConfig): The ColBERT configuration.
            verbose (bool, optional): Whether to print verbose output. Defaults to True.

        Returns:
            PLAIDModelIndex: The loaded PLAIDModelIndex object.
        """
        _, _, _, _ = index_path, index_name, index_config, verbose
        return PLAIDModelIndex(config)

    def build(
        self,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_name: Optional[str] = None,
        overwrite: Union[bool, str] = "reuse",
        verbose: bool = True,
        **kwargs,
    ) -> "PLAIDModelIndex":
        """
        Builds the index for the given collection using the specified checkpoint.

        Args:
            checkpoint (Union[str, Path]): The path to the checkpoint file or the checkpoint file itself.
            collection (List[str]): The collection of documents to build the index from.
            index_name (Optional[str]): The name of the index. If not provided, a default name will be used.
            overwrite (Union[bool, str]): Specifies whether to overwrite an existing index with the same name.
                If set to "reuse", the existing index will be reused. If set to True, the existing index will be overwritten.
            verbose (bool): Specifies whether to print verbose output during the indexing process.
            **kwargs: Additional keyword arguments.

        Returns:
            PLAIDModelIndex: The built index.

        Raises:
            AssertionError: If `bsize` is not an integer.

        """
        bsize = kwargs.get("bsize", PLAIDModelIndex._DEFAULT_INDEX_BSIZE)
        assert isinstance(bsize, int)

        nbits = 2
        if len(collection) < 5000:
            nbits = 8
        elif len(collection) < 10000:
            nbits = 4

        self.config = ColBERTConfig.from_existing(
            self.config, ColBERTConfig(nbits=nbits, index_bsize=bsize)
        )

        # Instruct colbert-ai to disable forking if nranks == 1
        self.config.avoid_fork_if_possible = True

        if len(collection) > 100000:
            self.config.kmeans_niters = 4
        elif len(collection) > 50000:
            self.config.kmeans_niters = 10
        else:
            self.config.kmeans_niters = 20

        CollectionIndexer._train_kmeans = (
            self.pytorch_kmeans
        )  # pylint: disable=protected-access

        indexer = Indexer(
            checkpoint=checkpoint,
            config=self.config,
            verbose=verbose,
        )
        indexer.configure(avoid_fork_if_possible=True)
        indexer.index(name=index_name, collection=collection, overwrite=overwrite)

        return self

    def _load_searcher(
        self,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_name: Optional[str],
        force_fast: bool = False,
    ):
        print(
            f"Loading searcher for index {index_name} for the first time...",
            "This may take a few seconds",
        )
        self.searcher = Searcher(
            checkpoint=checkpoint,
            config=None,
            collection=collection,
            index_root=self.config.root,
            index=index_name,
        )

        if not force_fast:
            self.searcher.configure(ndocs=1024)
            self.searcher.configure(ncells=16)
            if len(self.searcher.collection) < 10000:
                self.searcher.configure(ncells=8)
                self.searcher.configure(centroid_score_threshold=0.4)
            elif len(self.searcher.collection) < 100000:
                self.searcher.configure(ncells=4)
                self.searcher.configure(centroid_score_threshold=0.45)
            # Otherwise, use defaults for k
        else:
            # Use fast settingss
            self.searcher.configure(ncells=1)
            self.searcher.configure(centroid_score_threshold=0.5)
            self.searcher.configure(ndocs=256)

        print("Searcher loaded!")

    def _search(self, query: str, k: int, pids: Optional[List[int]] = None):
        assert self.searcher is not None
        return self.searcher.search(query, k=k, pids=pids)

    def _batch_search(self, query: list[str], k: int):
        assert self.searcher is not None
        queries = {i: x for i, x in enumerate(query)}
        results = self.searcher.search_all(queries, k=k)
        results = [
            [list(zip(*value))[i] for i in range(3)]
            for value in results.todict().values()
        ]
        return results

    def _upgrade_searcher_maxlen(self, maxlen: int, base_model_max_tokens: int):
        assert self.searcher is not None
        # Keep maxlen stable at 32 for short queries for easier visualisation
        maxlen = min(max(maxlen, 32), base_model_max_tokens)
        self.searcher.config.query_maxlen = maxlen
        self.searcher.checkpoint.query_tokenizer.query_maxlen = maxlen

    def search(
        self,
        config: ColBERTConfig,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_name: Optional[str],
        base_model_max_tokens: int,
        query: Union[str, list[str]],
        k: int = 10,
        pids: Optional[List[int]] = None,
        force_reload: bool = False,
        **kwargs,
    ) -> list[tuple[list, list, list]]:
        """
        Perform a search on the index.

        Args:
            config (ColBERTConfig): The configuration for ColBERT.
            checkpoint (Union[str, Path]): The path to the checkpoint.
            collection (List[str]): The collection of documents.
            index_name (Optional[str]): The name of the index.
            base_model_max_tokens (int): The maximum number of tokens in the base model.
            query (Union[str, list[str]]): The query or list of queries to search for.
            k (int, optional): The number of documents to retrieve. Defaults to 10.
            pids (Optional[List[int]], optional): The list of document IDs to retrieve. Defaults to None.
            force_reload (bool, optional): Whether to force reload the index. Defaults to False.
            **kwargs: Additional keyword arguments.

        Returns:
            list[tuple[list, list, list]]: A list of search results, where each result is a tuple containing three lists:
                - The document IDs of the retrieved documents.
                - The scores of the retrieved documents.
                - The offsets of the retrieved documents.
        """
        self.config = config

        force_fast = kwargs.get("force_fast", False)
        assert isinstance(force_fast, bool)

        if self.searcher is None or force_reload:
            self._load_searcher(
                checkpoint,
                collection,
                index_name,
                force_fast,
            )
        assert self.searcher is not None

        base_ncells = self.searcher.config.ncells
        base_ndocs = self.searcher.config.ndocs

        if k > len(self.searcher.collection):
            print(
                "WARNING: k value is larger than the number of documents in the index!",
                f"Lowering k to {len(self.searcher.collection)}...",
            )
            k = len(self.searcher.collection)

        # For smaller collections, we need a higher ncells value to ensure we return enough results
        if k > (32 * self.searcher.config.ncells):
            self.searcher.configure(ncells=min((k // 32 + 2), base_ncells))

        self.searcher.configure(ndocs=max(k * 4, base_ndocs))

        if isinstance(query, str):
            query_length = int(len(query.split(" ")) * 1.35)
            self._upgrade_searcher_maxlen(query_length, base_model_max_tokens)
            results = [self._search(query, k, pids)]
        else:
            longest_query_length = max([int(len(x.split(" ")) * 1.35) for x in query])
            self._upgrade_searcher_maxlen(longest_query_length, base_model_max_tokens)
            results = self._batch_search(query, k)

        # Restore original ncells&ndocs if it had to be changed for large k values
        self.searcher.configure(ncells=base_ncells)
        self.searcher.configure(ndocs=base_ndocs)

        return results  # type: ignore

    @staticmethod
    def _should_rebuild(current_len: int, new_doc_len: int) -> bool:
        """
        Heuristic to determine if it is more efficient to rebuild the index instead of updating it.
        """
        return current_len + new_doc_len < 5000 or new_doc_len > current_len * 0.05

    def add(
        self,
        config: ColBERTConfig,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_root: str,
        index_name: str,
        new_collection: List[str],
        verbose: bool = True,
        **kwargs,
    ) -> None:
        """
        Adds new documents to the index.

        Args:
            config (ColBERTConfig): The configuration for the ColBERT model.
            checkpoint (Union[str, Path]): The path to the checkpoint file.
            collection (List[str]): The existing collection of documents.
            index_root (str): The root directory for the index.
            index_name (str): The name of the index.
            new_collection (List[str]): The new collection of documents to be added.
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        self.config = config

        bsize = kwargs.get("bsize", PLAIDModelIndex._DEFAULT_INDEX_BSIZE)
        assert isinstance(bsize, int)

        searcher = Searcher(
            checkpoint=checkpoint,
            config=None,
            collection=collection,
            index=index_name,
            index_root=index_root,
            verbose=verbose,
        )

        if PLAIDModelIndex._should_rebuild(
            len(searcher.collection), len(new_collection)
        ):
            self.build(
                checkpoint=checkpoint,
                collection=collection + new_collection,
                index_name=index_name,
                overwrite="force_silent_overwrite",
                verbose=verbose,
                **kwargs,
            )
        else:
            if self.config.index_bsize != bsize:  # Update bsize if it's different
                self.config.index_bsize = bsize

            updater = IndexUpdater(
                config=self.config, searcher=searcher, checkpoint=checkpoint
            )
            updater.add(new_collection)
            updater.persist_to_disk()

    def delete(
        self,
        config: ColBERTConfig,
        checkpoint: Union[str, Path],
        collection: List[str],
        index_name: str,
        pids_to_remove: Union[TypeVar("T"), List[TypeVar("T")]],
        verbose: bool = True,
    ) -> None:
        """
        Delete documents from the index.

        Args:
            config (ColBERTConfig): The configuration for ColBERT.
            checkpoint (Union[str, Path]): The path to the checkpoint.
            collection (List[str]): The collection of documents.
            index_name (str): The name of the index.
            pids_to_remove (Union[TypeVar("T"), List[TypeVar("T")]]): The document IDs to remove from the index.
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
        """
        self.config = config

        # Initialize the searcher and updater
        searcher = Searcher(
            checkpoint=checkpoint,
            config=None,
            collection=collection,
            index=index_name,
            verbose=verbose,
        )
        updater = IndexUpdater(config=config, searcher=searcher, checkpoint=checkpoint)

        updater.remove(pids_to_remove)
        updater.persist_to_disk()

    def _export_config(self) -> dict[str, Any]:
        return {}

    def export_metadata(self) -> dict[str, Any]:
        """
        Export the metadata for the index."""
        config = self._export_config()
        config["index_type"] = self.index_type
        return config
