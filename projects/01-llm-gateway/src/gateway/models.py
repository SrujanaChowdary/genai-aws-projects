from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=20000)
    max_tokens: int = Field(default=500, ge=1, le=4096)
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)


class GatewayResponse(BaseModel):
    text: str
    model_id: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
