import asyncio
from typing import List, Optional
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel

from ascenderai.ascender_ai import AscenderAI

class AscenderAIEmbeddingsL(BaseModel, Embeddings):
    model_name: str = "text-embedder-minilm-l6v2"
    output_type: str = "sentence_embedding"
    verbose: bool = False

    base_url: Optional[str] = None

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        client = AscenderAI(self.model_name, verbose=self.verbose)

        if self.base_url:
            client.base_url = self.base_url
        # NOTE: This is a blocking call.
        _response = asyncio.run(client.embeddings.create(texts, output_type=self.output_type))

        return _response.data.tolist()[0]
    
    def embed_query(self, text: str) -> List[float]:
        client = AscenderAI(self.model_name, verbose=self.verbose)
        
        if self.base_url:
            client.base_url = self.base_url
        # NOTE: This is a blocking call.
        _response = asyncio.run(client.embeddings.create(text, output_type=self.output_type))

        return _response.data.tolist()[0]
    
    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        client = AscenderAI(self.model_name, verbose=self.verbose)
        if self.base_url:
            client.base_url = self.base_url
        # Response in formated instance
        _response = await client.embeddings.create(texts, output_type=self.output_type)

        return _response.data.tolist()

    async def aembed_query(self, text: str) -> List[float]:
        client = AscenderAI(self.model_name, verbose=self.verbose)

        if self.base_url:
            client.base_url = self.base_url
        # Response in formated instance
        _response = await client.embeddings.create(text, output_type=self.output_type)

        return _response.data.tolist()