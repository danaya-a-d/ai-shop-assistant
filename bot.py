import asyncio
import os
from llm import ask_llm
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import logging


# загружаем переменные окружения
load_dotenv()

logger = logging.getLogger(__name__)

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


# обработчик текстовых сообщений
@dp.message(F.text)
async def message_handler(message: Message):
    try:
        answer = await ask_llm(message.text)
        await message.answer(answer)

    except Exception:
        logger.exception("Failed to process message")

        await message.answer(
            "Извините, сейчас не удалось обработать запрос. "
            "Попробуйте немного позже."
        )




# запуск бота

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    logger.info("Starting AI Shop Assistant")

    async with Bot(token=BOT_TOKEN) as bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
