import boto3

from . import config
from .models import GatewayResponse, PromptRequest
from .router import select_model


class Gateway:
    def __init__(self, client=None, small=None, large=None):
        self.client = client or boto3.client(
            "bedrock-runtime", region_name=config.AWS_REGION
        )
        self.small = small or config.SMALL_MODEL_ID
        self.large = large or config.LARGE_MODEL_ID
        if not self.small or not self.large:
            raise ValueError("Set SMALL_MODEL_ID and LARGE_MODEL_ID")

    def _kwargs(self, req: PromptRequest) -> dict:
        return {
            "modelId": select_model(req.prompt, self.small, self.large),
            "messages": [{"role": "user", "content": [{"text": req.prompt}]}],
            "inferenceConfig": {
                "maxTokens": req.max_tokens,
                "temperature": req.temperature,
            },
        }

    def invoke(self, req: PromptRequest) -> GatewayResponse:
        kw = self._kwargs(req)
        r = self.client.converse(**kw)
        return GatewayResponse(
            text=r["output"]["message"]["content"][0]["text"],
            model_id=kw["modelId"],
            input_tokens=r["usage"]["inputTokens"],
            output_tokens=r["usage"]["outputTokens"],
            latency_ms=r["metrics"]["latencyMs"],
        )

    def stream(self, req: PromptRequest):
        r = self.client.converse_stream(**self._kwargs(req))
        for event in r["stream"]:
            delta = event.get("contentBlockDelta")
            if delta:
                yield delta["delta"].get("text", "")
