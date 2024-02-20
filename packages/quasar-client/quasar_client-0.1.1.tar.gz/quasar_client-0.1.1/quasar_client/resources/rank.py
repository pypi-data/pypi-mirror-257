"""Ranker Resource Module."""

from typing import List, Tuple

from ..dataclasses.rank import RankerMeta
from .base import Resource


class RankerResource(Resource):
    """Ranker Resource Class."""

    def rank(
        self,
        pairs: List[Tuple[str, str]],
    ) -> List[RankerMeta]:
        """Rank pairs of text."""
        output = self._post(
            data={
                "input_data": {"pairs": pairs},
                "task": "ranking",
            },
        )
        output.raise_for_status()
        return [
            RankerMeta(
                pair=(pair["query"], pair["candidate"]),
                score=pair["score"],
            )
            for pair in output.json()["output"]
        ]
