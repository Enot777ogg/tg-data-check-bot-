import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ChatAction
from aiogram.filters import Command
from dotenv import load_dotenv
from phonecheck import check_phone
from fiocheck import search_fio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я помогу проверить данные:\n\n"
        "📱 /checkphone <номер> — валидность и спам\n"
        "🧑 /checkfio <ФИО> — поиск в базе утечек\n\n"
        "Пример:\n"
        "/checkphone +79991234567\n"
        "/checkfio Иванов Иван Иванович"
    )

@dp.message(Command("checkphone"))
async def cmd_checkphone(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("❗ Пример использования:\n/checkphone +79991234567")
        return

    number = args[1]
    await message.chat.do(ChatAction.TYPING)
    result = await check_phone(number)

    if not result["valid"]:
        await message.answer(f"❌ Невалидный номер: {result.get('reason')}")
    else:
        spam = "🔴 Найден в спам-базе" if result["spammer"] else "🟢 Не найден в спаме"
        await message.answer(
            f"☎️ Номер: {result['formatted']}\n"
            f"🌍 Страна: {result['country']}\n"
            f"✅ Валидный\n"
            f"{spam}"
        )

@dp.message(Command("checkfio"))
async def cmd_checkfio(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("❗ Пример:\n/checkfio Иванов Иван Иванович")
        return

    fio = args[1]
    await message.chat.do(ChatAction.TYPING)
    result = search_fio(fio)

    if result is None:
        await message.answer("🟢 Совпадений не найдено.")
    elif isinstance(result, str):
        await message.answer(result)
    else:
        msg = "⚠️ Найдены совпадения:\n\n"
        for row in result:
            msg += (
                f"📅 Дата: {row['Дата']}\n"
                f"🗂 Источник: {row['Источник']}\n"
                f"📝 Комментарий: {row['Комментарий']}\n\n"
            )
        await message.answer(msg)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
