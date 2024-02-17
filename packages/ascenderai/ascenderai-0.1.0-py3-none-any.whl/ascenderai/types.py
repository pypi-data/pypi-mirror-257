from typing import Literal, Optional
from numpy import ndarray
from pydantic import BaseModel


class CompletionChoice(BaseModel):
    text: str
    index: int = 0
    logprobs: Optional[dict]
    finish_reason: Optional[Literal["length", "stop"]] = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    model: str = "mistral-7b-instruct"
    object: str = "text_completion"
    created: int
    choices: list[CompletionChoice]
    usage: Optional[CompletionUsage] = None


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingResponse(BaseModel):
    id: str
    model: str = "text-embedder-minilm-l6v2"
    object: Literal["embeddings.sentence", "embeddings.token"]
    data: ndarray | bytes
    usage: EmbeddingUsage

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ndarray: lambda v: v.tolist()
        }