import asyncio
import json
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os

# === КОНФИГ ===
BOT_TOKEN = os.getenv('BOT_TOKEN')
MASHA_ID = 390005162
MILANA_ID = 436264598
DATA_FILE = 'data.json'

# === ПУПЫ ===
PUP_IMAGES = {
    'happy': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_happy.webp',
    'sad': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_sad.webp',
    'surprise': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_surprise.webp',
    'love': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/up_love.webp'
}

# === ФРАЗЫ ===
PRAISE = ["Умница, Миланочка! ☀️", "Ты просто волшебница, Миланочка! ✨", "Моя любимая садовница! 🌸"]
WATER_REMS = ["шепчет: «Мне бы глоточек водички...» 💧", "тихо намекает: «А не пора ли попить?» 💦", "нежно просит: «Чуточку воды, пожалуйста?» 🌱"]
FUN_FACTS = ["Герань очищает воздух и помогает спать спокойно. 💕", "Герани отпугивают комаров! 🦸‍♀️", "Герани — путешественницы из Африки, но полюбили твой домик! 🌍"]
LEVELS = [(0, "Росточек 🌱"), (10, "Госпожа Лейка 💧"), (30, "Лепесточек 🌸"), (60, "Хранительница цветения 🌿"), (100, "Цветочная фея 🌷")]

# === СОСТОЯНИЯ ===
class Form(StatesGroup):
    waiting_photo1 = State()
    waiting_name1 = State()
    waiting_photo2 = State()
    waiting_name2 = State()
    lesson_light = State()
    lesson_water = State()

# === БОТ ===
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# === ДАННЫЕ ===
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"plants": {}, "milanochka": {"level": "Росточек 🌱", "xp_total": 0, "petals": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_level(xp):
    for thresh, name in reversed(LEVELS):
        if xp >= thresh:
            return name
    return "Росточек 🌱"

# === ОТПРАВКА С ПУПОМ ===
async def send_pup(chat_id, text, image='happy', reply_markup=None):
    try:
        await bot.send_photo(chat_id, PUP_IMAGES[image], caption=text, reply_markup=reply_markup)
    except:
        await bot.send_message(chat_id, text, reply_markup=reply_markup)

# === /start ===
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    if message.from_user.id != MILANA_ID:
        return
    data = load_data()
    await send_pup(MILANA_ID, "Привет, Миланочка! Меня зовут Пуп! 🌸<br>Меня создала Машка, чтобы я помогал с цветочками 🌿<br>Пришли фото первого цветка (из гостиной)!", 'love')
    await state.set_state(Form.waiting_photo1)

# === ФОТО 1 ===
@dp.message(Form.waiting_photo1, F.photo)
async def photo1(message: types.Message, state: FSMContext):
    await send_pup(MILANA_ID, "Ого, какой красивый! А как его зовут? 🌷", 'surprise')
    await state.update_data(photo1=message.photo[-1].file_id)
    await state.set_state(Form.waiting_name1)

@dp.message(Form.waiting_name1)
async def name1(message: types.Message, state: FSMContext):
    data = load_data()
    user_data = await state.get_data()
    name = message.text.strip()
    data["plants"][name] = {"last_water": None, "photo": user_data["photo1"]}
    save_data(data)
    await send_pup(MILANA_ID, f"Теперь {name} под моей опекой! 💧<br>Пришли фото второго цветка!", 'happy')
    await state.set_state(Form.waiting_photo2)

# === ФОТО 2 ===
@dp.message(Form.waiting_photo2, F.photo)
async def photo2(message: types.Message, state: FSMContext):
    await send_pup(MILANA_ID, "Вау! А имя? 🌺", 'surprise')
    await state.update_data(photo2=message.photo[-1].file_id)
    await state.set_state(Form.waiting_name2)

@dp.message(Form.waiting_name2)
async def name2(message: types.Message, state: FSMContext):
    data = load_data()
    user_data = await state.get_data()
    name = message.text.strip()
    data["plants"][name] = {"last_water": None, "photo": user_data["photo2"]}
    save_data(data)
    await send_pup(MILANA_ID, f"Ура! {name} тоже с нами! 🌿<br>Теперь урок: где ставить цветы? ☀️", 'love')
    await state.set_state(Form.lesson_light)

# === УРОКИ ===
@dp.message(Form.lesson_light)
async def lesson_light(message: types.Message, state: FSMContext):
    data = load_data()
    data["milanochka"]["xp_total"] += 5
    data["milanochka"]["level"] = get_level(data["milanochka"]["xp_total"])
    save_data(data)
    await send_pup(MILANA_ID, random.choice(PRAISE) + "<br>Цветы любят свет, но не прямое солнце! 🌞<br>Теперь — полив! 💧", 'happy')
    await state.set_state(Form.lesson_water)

@dp.message(Form.lesson_water)
async def lesson_water(message: types.Message, state: FSMContext):
    data = load_data()
    data["milanochka"]["xp_total"] += 5
    data["milanochka"]["petals"] += 1
    save_data(data)
    await send_pup(MILANA_ID, "Поливай, когда земля сухая на 2 см! 💦<br>Ты получила +1 лепесток! 🌸", 'happy')
    if data["milanochka"]["petals"] >= 12:
        await bot.send_message(MASHA_ID, "Миланочка собрала 12 лепестков! Срочно беги — сюрприз! 🎉")
    await state.clear()

# === НАПОМИНАНИЯ О ПОЛИВЕ ===
async def water_reminders():
    while True:
        await asyncio.sleep(7200)  # каждые 2 часа
        data = load_data()
        now = datetime.now()
        for name, plant in data["plants"].items():
            if plant["last_water"] is None or (now - datetime.fromisoformat(plant["last_water"])).days >= 3:
                await send_pup(MILANA_ID, f"{name} {random.choice(WATER_REMS)}", 'sad')
                break
        if random.random() < 0.1:
            await send_pup(MILANA_ID, random.choice(FUN_FACTS), 'happy')

# === УТРЕННИЕ/ВЕЧЕРНИЕ ===
async def daily_greeting():
    while True:
        now = datetime.now()
        if 8 <= now.hour <= 10 and now.minute == 0:
            await send_pup(MILANA_ID, "Доброе утро, Миланочка! ☀️ Новый день — новые листочки!", 'happy')
        if 20 <= now.hour <= 22 and now.minute == 0:
            await send_pup(MILANA_ID, "Спокойной ночи, Миланочка! 🌙 Цветочки спят и шепчут 'спасибо' 💚", 'love')
        await asyncio.sleep(60)

# === СТАРТ ===
async def main():
    asyncio.create_task(water_reminders())
    asyncio.create_task(daily_greeting())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
