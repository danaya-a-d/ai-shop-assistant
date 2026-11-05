import asyncio
import os
from llm import ask_llm
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv


# загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")


# создаем диспетчер
dp = Dispatcher()


# обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! 👋 Я AI-ассистент интернет-магазина.\n"
        "Напиши свой вопрос, и я постараюсь помочь!"
    )


# обработчик обычных текстовых сообщений
@dp.message(F.text)
async def message_handler(message: Message):
    try:
        answer = await ask_llm(message.text)
        await message.answer(answer)

    except Exception:
        await message.answer(
            "Извините, сейчас не удалось обработать запрос. "
            "Попробуйте немного позже."
        )



# запуск бота
async def main():
    async with Bot(token=BOT_TOKEN) as bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
