from typing import Dict
from urllib.parse import urljoin

import requests


class Resource:
    """Resource Base Class."""

    def __init__(self, quasar_base):
        self._quasar_base = quasar_base
        self._prediction_endpoint = urljoin(self._quasar_base, "/predictions/")

    def _post(self, data: Dict):
        """Post data to the resource."""
        if "model_version" not in data:
            data["model_version"] = 1
        return requests.post(
            self._prediction_endpoint,
            json=data,
        )
