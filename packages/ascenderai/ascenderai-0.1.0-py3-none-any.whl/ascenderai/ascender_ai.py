import json
from aiohttp import ClientSession
from typing import AsyncIterator, Literal, Optional
from rich import print as rprint
from rich.panel import Panel
from numpy import array

import os
from ascenderai.handler import AscenderExceptionManager

from ascenderai.types import CompletionChoice, CompletionResponse, CompletionUsage, EmbeddingResponse, EmbeddingUsage


class AscenderAI:

    def __init__(self, model: str = "mistral-7b-instruct", *, max_tokens: int = 200,
                 streaming: bool = False, verbose: bool = False) -> None:
        self.completions = AscenderAIChat(
            model=model,
            max_tokens=max_tokens,
            streaming=streaming,
            verbose=verbose
        )
        self.embeddings = AscenderAIEmbeddings(
            model=model,
            verbose=verbose
        )
    @property
    def base_url(self):
        return self.completions.base_url
    
    @base_url.setter
    def base_url(self, value: str):
        self.completions.base_url = value
        self.embeddings.base_url = value

    def ping(self):
        """
        This method made for testing connection with AI Cluster and health of AI Cluster.
        """
        # TODO: Implement the ping-pong method
        return "PONG!"
    
    def __str__(self) -> str:
        return self.completions.model
    
    def __repr__(self) -> str:
        return f"AscenderAI(model={self.completions.model!r}, max_tokens={self.completions.max_tokens}, streaming={self.completions.streaming}, verbose={self.completions.verbose})"


class AscenderAIChat:
    base_url: str = os.getenv("ASCENDER_AI_BASE_URL", "https://ai.ascender.space")
    def __init__(self, model: str = "mistral-7b-instruct", *,
                 max_tokens: int = 30, streaming: bool = False,
                 verbose: bool = False) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.streaming = streaming
        self.verbose = verbose
        self._exception_manager = AscenderExceptionManager(model)
    
    async def create(self, prompt: str, *, temperature: float = 0.9, 
                             stop_seqs: Optional[list[str]] = None, seed: Optional[int] = None) -> CompletionResponse | AsyncIterator[CompletionResponse]:
        """
        ## Create Completion

        `AscenderAIChat.create()` or `AscenderAI.completions.create()` is used to create completions for a given prompt.
        It creates a completion for the given prompt using the specified LLM model.

        Args:
            prompt (str): Prompt for which the completion will be created.
            temperature (float, optional): Temperature of inference during sampling, from 0 to 1. Less temperature - more creative. Defaults to 0.9.
            stop_seqs (Optional[list[str]], optional): Tokens where inference response generation should be stopped. Defaults to None.
            seed (Optional[int], optional): Seed of inference. Defaults to None.
        """
        # Verbose displaying of the prompt
        if self.verbose:
            panel = Panel(f"[bold green]{prompt.replace('[', '\[').replace("]", "\]")}[/bold green]", title="Get completion request")
            rprint(panel)
        
        if self.streaming:
            return self.stream(prompt, temperature=temperature, stop=stop_seqs, seed=seed)
        else:
            async with ClientSession(base_url=self.base_url) as client:
                async with client.post("/completions/completions", json={
                    "prompt": prompt,
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "temperature": temperature,
                    "stop_seqs": stop_seqs,
                    "seed": seed,
                }) as resp:
                    # For HTTP error handling
                    self._exception_manager.listen_for_errors("completions.create", resp)

                    # NOTE: If http error will be raised, then exception manager will stop execution of code from this line
                    response = await resp.json()
                    choices = response["choices"]
                    usage = response["usage"]

                    if self.verbose:
                        response_panel = Panel(f"[bold yellow]{response['choices'][0]['text']}[/bold yellow]", title="AI Response")
                        rprint(response_panel)
                    
                    del response["choices"]
                    del response["usage"]

                    response = CompletionResponse(
                        **response, choices=[CompletionChoice(**choice) for choice in choices],
                        usage=CompletionUsage(**usage)
                    )
                    return response
    
    async def stream(self, prompt: str, *, temperature: float = 0.9,
                                       stop: Optional[list[str]] = None, seed: Optional[int] = None):
        """
        ## Stream Completions

        `AscenderAIChat.stream()` or `AscenderAI.completions.stream()` is similar to `AscenderAIChat.stream()` or `AscenderAI.completions.stream()`.
        When previous one waits until completion would be generated completely and then returns, this one streams by returning iterator with token chunks.
        """
        
        async with ClientSession(base_url=self.base_url) as client:
            async with client.post("/completions/completions/stream", json={
                "prompt": prompt,
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": temperature,
                "stop_seqs": stop,
                "seed": seed,
            }) as resp:
                # For HTTP error handling
                self._exception_manager.listen_for_errors("completions.stream", resp)

                # NOTE: If http error will be raised, then exception manager will stop execution of code from this line
                async for line in resp.content.iter_any():
                    try:
                        readed_line = line.decode()

                        readed_line.split("} {")
                        json_decoded = json.loads(readed_line)
                        
                        choices = json_decoded["choices"]
                        usage = json_decoded["usage"]
                        
                        del json_decoded["choices"]
                        del json_decoded["usage"]
                        
                        response = CompletionResponse(
                            **json_decoded, choices=[CompletionChoice(**choice) for choice in choices],
                            usage=CompletionUsage(**usage)
                        )
                        yield response

                    except:
                        pass
                
    

class AscenderAIEmbeddings:

    base_url: str = os.getenv("ASCENDER_AI_BASE_URL", "https://ai.ascender.space")
    def __init__(self, model: str = "text-embedder-minilm-l6v2", *,
                 verbose: bool = False) -> None:
        self.model = model
        self.verbose = verbose
        self._exception_manager = AscenderExceptionManager(model)
    
    async def create(self, prompt: str | list[str], 
                     encoding_format: Literal["base64", "float"] = "float",
                     output_type: Optional[Literal["sentence_embedding", "token_embeddings"]] = "sentence_embedding") -> EmbeddingResponse:
        """
        ## Create Embedding

        `AscenderAIEmbeddings.create()` or `AscenderAI.embeddings.create()` is used to create embeddings for a given sentence or list of sentences.
        It creates vectoral representration of the sentence(s) using the specified sentence embedding model.

        Can be used for:
        - Search (where results are ranked by relevance to a query string)
        - Clustering (where text strings are grouped by similarity)
        - Recommendations (where items with related text strings are recommended)
        - Anomaly detection (where outliers with little relatedness are identified)
        - Diversity measurement (where similarity distributions are analyzed)
        - Classification (where text strings are classified by their most similar label)


        Args:
            prompt (str | list[str]): Sentence or list of sentences that will be used for embedding creation.
            encoding_format (Literal[&quot;base64&quot;, &quot;float&quot;], optional): Format of embedding encoding, float - will return in numpay array matrix in other ways it will return bytes representation. Defaults to "float".
            output_type (Optional[Literal[&quot;sentence_embedding&quot;, &quot;token_embeddings&quot;]], optional): The type of embeddings to return: "sentence_embedding" to get sentence embeddings, "token_embeddings" to get wordpiece token embeddings, and None, to get all output values. Defaults to "sentence_embedding".

        Returns:
            EmbeddingResponse: _description_
        """
        if self.verbose:
            panel = Panel(title="|- Embeddings creation request -|", renderable="")
            
            if isinstance(prompt, str):
                panel.renderable += prompt.replace('[', '\[').replace(']', '\]')
            
            else:
                panel.renderable += "\n".join([f"{i+1}. {p.replace('[', '\[').replace(']', '\]')}" for i, p in enumerate(prompt)])
            
            rprint(panel)
        
        async with ClientSession(base_url=self.base_url, headers={"Content-Type": "application/json"}) as client:
            async with client.post("/embeddings", json={
                "sentences": prompt,
                "model": self.model,
                "encoding_format": encoding_format,
                "output_type": output_type,
            }) as resp:
                # For HTTP error handling
                self._exception_manager.listen_for_errors("embeddings.create", resp)

                # NOTE: If http error will be raised, then exception manager will stop execution of code from this line
                response = await resp.json()
                embeddings_data = response["data"]
                usage = response["usage"]

                if encoding_format == "float":
                    embeddings_data = array(embeddings_data)
                else:
                    embeddings_data = embeddings_data.encode()
                
                del response["data"]
                del response["usage"]

                response = EmbeddingResponse(**response, data=embeddings_data, usage=EmbeddingUsage(
                    **usage
                ))
                return response