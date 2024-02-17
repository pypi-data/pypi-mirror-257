# AscenderAI SDK
⚡ Commuting with AscenderAI cluster in python with 1 lib ⚡

## Installation
```bash
# For windows
pip install ascenderai-sdk
# For linux or mac os
pip3 install ascenderai-sdk
```

## Usage
```python
import asyncio
from ascenderai import AscenderAI

client = AscenderAI()

async def main():
    response = await client.completions.create(
        prompt="Explain me about LLMs",
        max_tokens=5
    )
    print(response.choices[0].text)

asyncio.run(main())
```

## Documentation
- [Ascender Team](https://ascender.space/)
- [API Documentation](https://ascenderai.github.io/ascender-cluster-python-sdk/)
- [AscenderAI API](https://ai.ascender.space/docs/api/)