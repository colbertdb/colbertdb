"""https://github.com/bclavie/RAGatouille/blob/main/ragatouille/models/torch_kmeans.py"""

import torch
from fast_pytorch_kmeans import KMeans


def _train_kmeans(self, sample, shared_lists):  # noqa: ARG001

    if self.use_gpu:
        torch.cuda.empty_cache()
    centroids = compute_pytorch_kmeans(
        sample,
        self.config.dim,
        self.num_partitions,
        self.config.kmeans_niters,
        self.use_gpu,
    )
    centroids = torch.nn.functional.normalize(centroids, dim=-1)
    if self.use_gpu:
        centroids = centroids.half()
    else:
        centroids = centroids.float()
    return centroids


def compute_pytorch_kmeans(
    sample,
    dim,  # noqa compatibility
    num_partitions,
    kmeans_niters,
    use_gpu,
    batch_size=16000,
    verbose=1,
    seed=123,
    max_points_per_centroid=256,
    min_points_per_centroid=10,
):
    device = torch.device("cuda" if use_gpu else "cpu")
    sample = sample.to(device)
    total_size = sample.shape[0]

    torch.manual_seed(seed)

    # Subsample the training set if too large
    if total_size > num_partitions * max_points_per_centroid:
        print("too many!")
        print("partitions:", num_partitions)
        print(total_size)
        perm = torch.randperm(total_size, device=device)[
            : num_partitions * max_points_per_centroid
        ]
        sample = sample[perm]
        total_size = sample.shape[0]
        print("reduced size:")
        print(total_size)
    elif total_size < num_partitions * min_points_per_centroid:
        if verbose:
            print(
                f"Warning: number of training points ({total_size}) is less than "
                f"the minimum recommended ({num_partitions * min_points_per_centroid})"
            )

    sample = sample.float()
    minibatch = None
    if num_partitions > 15000:
        minibatch = batch_size
    if num_partitions > 30000:
        minibatch = int(batch_size / 2)

    kmeans = KMeans(
        n_clusters=num_partitions,
        mode="euclidean",
        verbose=1,
        max_iter=kmeans_niters,
        minibatch=minibatch,
    )
    kmeans.fit(sample)
    return kmeans.centroids
