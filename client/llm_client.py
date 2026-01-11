from openai import AsyncOpenAI
from client.response import TextDelta, TokenUsage, StreamEvent, EventType

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
            event = await self._non_stream_response(client, kwargs)
            yield event

    async def _stream_response(self):
        pass

    async def _non_stream_response(self, client: AsyncOpenAI, kwargs: dict[str, any])->StreamEvent:
        response = await client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        message = choice.message

        text_delta = None
        if message.content:
            text_delta=TextDelta(content=message.content)

        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                cached_tokens=response.prompt_token_details.cached_tokens,
            )
        else:
            usage= None

        return StreamEvent(
            type= EventType.MESSAGE_COMPLETE,
            text_delta=text_delta,
            finish_reason = choice.finish_reason,
            usage=usage
        )