from openai import AsyncOpenAI

class LLMClient:
    def __init__(self)-> None:
        self._client : AsyncOpenAI| None = None

    def get_client(self)->AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key='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',
                base_url='https://openrouter.ai/api/v1'
            )
            return self._client

    async def close(self)->None:
        if self._client:
            await self._client.close()
            self._client=None

    async def chat_completions(self, messages: list[dict[str, any]], stream: bool=True):
        client = self.get_client()
        kwargs = {
            "model":"arcee-ai/trinity-mini:free",
            "messages":messages,
            "stream":stream
        }
        if stream:  
            await self._stream_response()
        else:
            await self._non_stream_response(client, kwargs)

    async def _stream_response(self):
        pass

    async def _non_stream_response(self, client: AsyncOpenAI, kwargs: dict[str, any]):
        response = await client.chat.completions.create(**kwargs)
        print(response)