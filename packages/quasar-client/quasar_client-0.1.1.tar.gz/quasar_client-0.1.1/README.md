# Quasar Python Client

[![PyPI version](https://img.shields.io/pypi/v/quasar-client.svg)](https://pypi.org/project/quasar-client/)

## Installation

```sh
pip install quasar-client
```

## Usage

```python
from quasar_client import Quasar

quasar_base = "URL for Quasar-compatible server"
quasar = Quasar(quasar_base=quasar_base)

# Use OpenAI-compatible interfaces...
chat_completion = quasar.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello quasar",
        }
    ],
    model="gpt-3.5-turbo",
)

# Use Quasar-specific interfaces like NER...
entities = quasar.tagger.tag(
    task="ner", 
    text="Yurts Technologies is based in SF."
)
```

Quasar provides a convenient interface for common RAG APIs. In addition to the OpenAI APIs, the client supports:

- Entities
- Embedding
- Ranking
