from unittest.mock import MagicMock

from gateway.client import Gateway
from gateway.models import PromptRequest


def test_invoke_maps_response():
    fake = MagicMock()
    fake.converse.return_value = {
        "output": {"message": {"content": [{"text": "hi"}]}},
        "usage": {"inputTokens": 3, "outputTokens": 1},
        "metrics": {"latencyMs": 42},
    }
    out = Gateway(client=fake, small="s", large="l").invoke(
        PromptRequest(prompt="hello")
    )
    assert out.text == "hi" and out.model_id == "s" and out.latency_ms == 42
