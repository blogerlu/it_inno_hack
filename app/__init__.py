import mapply

mapply.init(
    n_workers=-1,
    chunk_size=100,
    max_chunks_per_worker=8,
    progressbar=False,
)

from .processor import Processor

__all__ = ["Processor"]
