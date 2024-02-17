from langchain_core.callbacks import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from ascenderai.ascender_ai import AscenderAIChat
from langchain_core.outputs import GenerationChunk, LLMResult, Generation
from langchain_core.language_models.llms import LLM

from typing import Any, AsyncIterator, List, Mapping, Optional
from langchain_core.pydantic_v1 import Field

class AscenderAIL(LLM):
    model_name: str = "mistral-7b-instruct"
    prefix_messages: list[str] = Field(default=[], description="Messages to prefix to the prompt")
    """Series of messages to input before the given message"""
    streaming: bool = Field(default=False, description="Whether to stream the response or not")
    """Whether to stream the response or not"""
    max_tokens: int = Field(default=100, description="Maximum number of tokens to generate")
    """Maximum number of tokens to generate"""

    @property
    def _llm_type(self):
        return "ascender-ai"
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "prefix_messages": self.prefix_messages,
            "streaming": self.streaming,
            "max_tokens": self.max_tokens
        }

    async def _astream(self, prompt: str, stop: List[str] | None = None, run_manager: AsyncCallbackManagerForLLMRun | None = None, **kwargs: Any) -> AsyncIterator[GenerationChunk]:
        _client = AscenderAIChat(self.model_name, max_tokens=self.max_tokens, streaming=True, verbose=self.verbose)
        
        response = await _client.create(prompt, stop_seqs=stop, **kwargs)
        async for chunk in response:
            yield GenerationChunk(text=chunk.choices[0].text, generation_info=chunk.model_dump())
            if run_manager:
                await run_manager.on_llm_new_token(chunk.choices[0].text, chunk=chunk.model_dump())

    async def _agenerate(self, prompts: List[str], stop: List[str] | None = None, run_manager: AsyncCallbackManagerForLLMRun | None = None, **kwargs: Any) -> LLMResult:
        _client = AscenderAIChat(self.model_name, max_tokens=self.max_tokens, verbose=self.verbose)
        completions = []
        for prompt in prompts:
            print(self.predict_messages)
            if len(self.prefix_messages):
                prompt = "\n".join(self.prefix_messages) + "\n" + prompt
            completion = await _client.create(prompt, stop_seqs=stop, **kwargs)
            completions.append(list(map(lambda c: Generation(text=c.text, generation_info=c.model_dump()), completion.choices)))
                
        return LLMResult(generations=completions, llm_output={"model_name": self.model_name})

    async def _acall(self, prompt: str, stop: List[str] | None = None, run_manager: AsyncCallbackManagerForLLMRun | None = None, **kwargs: Any) -> str:
        return await self._agenerate([prompt], stop=stop, run_manager=run_manager, **kwargs)
    
    def _call(self, prompt: str, stop: List[str] | None = None, run_manager: CallbackManagerForLLMRun | None = None, **kwargs: Any) -> str:
        raise NotImplementedError("This LLM does not support synchronous calls")