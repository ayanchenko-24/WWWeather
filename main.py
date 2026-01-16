import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from weather_utils import get_weather, get_forecast_graph

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Кнопки
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Москва"), KeyboardButton(text="Новокузнецк")],
        [KeyboardButton(text="Новосибирск"), KeyboardButton(text="Гомель")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я бот-метеоролог. Напиши название города, и я пришлю погоду с графиком.",
        reply_markup=main_kb
    )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("Просто введи название города (например, 'Токио' или 'Лондон').")

@dp.message(F.text)
async def handle_weather(message: types.Message):
    city = message.text
    data = get_weather(city)
    
    if not data:
        await message.answer("Город не найден. Попробуй еще раз.")
        return

    text = f"Погода в {data['city']}:\n🌡 Температура: {data['temp']}°C\n☁️ Описание: {data['desc']}"
    
    # Создаем график
    graph_path = get_forecast_graph(city)
    
    if graph_path:
        photo = FSInputFile(graph_path)
        await message.answer_photo(photo, caption=text)
    else:
        await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
