# ai_chat.py
import asyncio
import g4f

async def get_ai_response(message):
    try:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
            provider=None  # Use default provider
        )
        return response
    except Exception as e:
        return f"Ошибка: {str(e)}"