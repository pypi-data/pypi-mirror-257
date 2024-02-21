"""Ranker Resource Module."""

from typing import List

from ..dataclasses.embed import EmbeddingMeta
from .base import Resource


class EmbeddingResource(Resource):
    """Embedding Resource Class."""

    def embed(
        self,
        texts: List[str],
    ) -> List[EmbeddingMeta]:
        """Embed all texts."""
        output = self._post(
            data={
                "input_data": {"texts": texts},
                "task": "embedding",
            },
        )
        output.raise_for_status()
        return [
            EmbeddingMeta(
                embedding=emb["embedding"],
                text=emb["text"],
            )
            for emb in output.json()["output"]
        ]
