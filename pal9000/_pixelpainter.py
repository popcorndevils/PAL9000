import concurrent.futures
import asyncio
from openai import OpenAI


class PixelPainter:
    '''
    Interface between OpenAI's DALL-E 3 API and PAL9000.
    '''
    def __init__(self, api_key):
        self.key = api_key
        self.client = OpenAI(api_key = self.key)

    def sync_generate(self, prompt: str):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response

    async def async_generate(self, prompt: str):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            response = await loop.run_in_executor(pool, self.sync_generate, prompt)
            return response

    async def generate_multiple(self, prompt: str, n: int):
        tasks = [self.async_generate(prompt) for _ in range(n)]
        responses = await asyncio.gather(*tasks)
        _output = responses[0]
        for r in responses[1:]:
            _output.data.append(r.data[0])

        return _output
