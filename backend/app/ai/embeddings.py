"""Text embeddings for duplicate detection and lesson retrieval (pgvector).

The MVP uses a local feature-hashing embedder: deterministic, free and good at catching near-identical
questions. It sits behind `get_embedder()` so a semantic model (e.g. Voyage, or a multilingual sentence model)
can replace it later; switching requires re-embedding stored rows and possibly a new EMBEDDING_DIM migration.
"""

import hashlib
import math
import re
from functools import lru_cache

from app.config import get_settings

_TOKEN = re.compile(r"\w+", re.UNICODE)


class HashingEmbedder:
    def __init__(self, dim: int):
        self.dim = dim

    def _features(self, text: str):
        words = _TOKEN.findall(text.lower())
        yield from words
        yield from (f"{a}_{b}" for a, b in zip(words, words[1:]))

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for f in self._features(text):
            h = hashlib.md5(f.encode()).digest()
            idx = int.from_bytes(h[:4], "little") % self.dim
            vec[idx] += 1.0 if h[4] & 1 else -1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


@lru_cache
def get_embedder() -> HashingEmbedder:
    return HashingEmbedder(get_settings().embedding_dim)


def embed(text: str) -> list[float]:
    return get_embedder().embed(text)


def cosine(a: list[float] | None, b: list[float] | None) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)
