from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


class Reference:
    """
    A class to store the previous response from the Groq API
    """

    def __init__(self) -> None:
        self.reference = ""


reference = Reference()

# Fast Groq model
model_name = "openai/gpt-oss-20b"

# Store separate conversation history for each user
conversation_history = {}

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):

    await message.reply(
        "Hi\nI am Tele Bot!\nCreated by SRUJAN G M. How can I assist you?"
    )


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):

    user_id = message.from_user.id

    # Clear only this user's conversation
    conversation_history[user_id] = []

    await message.reply(
        "I've cleared the past conversation and context."
    )


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):

    help_command = """
Hi There, I'm a Telegram bot created by SRUJAN G M!

Please follow these commands:

/start - to start the conversation
/clear - to clear the past conversation and context
/help - to get this help menu

I hope this helps. :)
"""

    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message):

    print(f"USER: {message.text}")

    user_id = message.from_user.id

    # Create separate history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Add user's message
    conversation_history[user_id].append({
        "role": "user",
        "content": message.text
    })

    messages = [
        {
            "role": "system",
            "content": """
Answer the user's question briefly and directly.

Rules:
- Give only the answer requested.
- For definition questions, give only 1-2 sentences.
- Do not give extra information unless asked.
- For full form questions, give only the full form.
- For programming questions, give only the required code unless explanation is requested.
- If the user refers to something from the previous message, use the conversation history to understand it.
"""
        }
    ]

    # Add only this user's conversation history
    messages.extend(conversation_history[user_id])

    # Send request to Groq
    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    # Get response
    reference.reference = response.choices[0].message.content

    # Store bot response for this user
    conversation_history[user_id].append({
        "role": "assistant",
        "content": reference.reference
    })

    print(f"Groq: {reference.reference}")

    # Telegram message limit
    MAX_LENGTH = 4096

    # Send long responses in multiple messages
    for i in range(0, len(reference.reference), MAX_LENGTH):

        await bot.send_message(
            chat_id=message.chat.id,
            text=reference.reference[i:i + MAX_LENGTH]
        )


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)