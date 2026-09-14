# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import numpy as np
import rasterio
from torch.utils.data import Sampler


class RandomGeoSampler(Sampler):
    def __init__(self, image_fns, length, patch_size, tile_size=None, weights=None):
        self.tile_sample_weights = []
        self.tile_heights = []
        self.tile_widths = []
        self.length = length
        self.patch_size = patch_size

        if tile_size is None:
            for image_fn in image_fns:
                with rasterio.open(image_fn[0]) as f:
                    image_height, image_width = f.shape
                self.tile_sample_weights.append(image_height * image_width)
                self.tile_heights.append(image_height)
                self.tile_widths.append(image_width)
        else:
            for image_fn in image_fns:
                self.tile_sample_weights.append(tile_size[0] * tile_size[1])
                self.tile_heights.append(tile_size[0])
                self.tile_widths.append(tile_size[1])

        if weights is not None:
            assert len(weights) == len(image_fns)
            self.tile_sample_weights = weights

        self.tile_sample_weights = np.array(self.tile_sample_weights)
        self.tile_sample_weights = (
            self.tile_sample_weights / self.tile_sample_weights.sum()
        )
        self.num_tiles = len(self.tile_sample_weights)

    def __iter__(self):
        # Draw all random indices/offsets for the epoch in a handful of vectorized
        # numpy calls instead of 3 separate per-sample RNG calls (np.random.choice
        # + 2x np.random.randint), each of which pays O(num_tiles) setup overhead
        # (e.g. rebuilding the cumulative weight array) on every call. Batching
        # this drastically reduces per-sample CPU/energy overhead, especially for
        # large ``length`` values (train_batches_per_epoch * batch_size).
        n = len(self)
        tile_heights = np.asarray(self.tile_heights)
        tile_widths = np.asarray(self.tile_widths)

        indices = np.random.choice(self.num_tiles, size=n, p=self.tile_sample_weights)
        max_y_sizes = np.maximum(tile_heights[indices] - self.patch_size, 1)
        max_x_sizes = np.maximum(tile_widths[indices] - self.patch_size, 1)
        ys = (np.random.random(n) * max_y_sizes).astype(np.int64)
        xs = (np.random.random(n) * max_x_sizes).astype(np.int64)

        for i, y, x in zip(indices.tolist(), ys.tolist(), xs.tolist()):
            yield (i, y, x, self.patch_size)

    def __len__(self):
        return self.length


class GridGeoSampler(Sampler):
    def __init__(
        self,
        image_fns,
        image_fn_indices,
        patch_size=256,
        stride=256,
    ):
        self.image_fn_indices = image_fn_indices
        self.patch_size = patch_size

        # tuples of the form (i, y, x, patch_size) that index into a CustomTileDataset
        self.indices = []
        for i in self.image_fn_indices:
            with rasterio.open(image_fns[i][0]) as f:
                height, width = f.height, f.width

            if patch_size > height and patch_size > width:
                self.indices.append((i, 0, 0, self.patch_size))
            else:
                for y in list(range(0, height - patch_size, stride)) + [
                    height - patch_size
                ]:
                    for x in list(range(0, width - patch_size, stride)) + [
                        width - patch_size
                    ]:
                        self.indices.append((i, y, x, self.patch_size))
        self.num_chips = len(self.indices)

    def __iter__(self):
        for index in self.indices:
            yield index

    def __len__(self):
        return self.num_chips
