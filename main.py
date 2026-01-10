from client.llm_client import LLMClient
import asyncio
async def main():
    client = LLMClient()
    messages = [{
        "role":"user",
        "content":"Hi, Whats up"
    }]
    await client.chat_completions(messages, False)

asyncio.run(main())
