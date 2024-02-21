import numpy as np
from typing import Any
from ReplayTables.sampling.IndexSampler import IndexSampler
from ReplayTables.interface import IDX, IDXs, LaggedTimestep, Batch

class UniformSampler(IndexSampler):
    def __init__(
        self,
        rng: np.random.Generator,
        max_size: int,
    ) -> None:
        super().__init__(rng, max_size)

    def replace(self, idx: IDX, transition: LaggedTimestep, /, **kwargs: Any) -> None:
        ...

    def update(self, idxs: IDXs, batch: Batch, /, **kwargs: Any) -> None:
        ...

    def isr_weights(self, idxs: IDXs):
        return np.ones(len(idxs))

    def sample(self, n: int) -> IDXs:
        idxs: Any = self._rng.integers(0, self._mapper.size, size=n)
        return idxs
