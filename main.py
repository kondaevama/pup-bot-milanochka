import asyncio
import json
import logging
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

# Твои данные
BOT_TOKEN = os.getenv('BOT_TOKEN')
MASHA_ID = 390005162
MILANA_ID = 436264598
DATA_FILE = 'data.json'

# ТВОИ ПУПЫ — ВСТАВЛЕНЫ!
PUP_IMAGES = {
    'happy': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_happy.webp',
    'sad': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_sad.webp',
    'surprise': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_surprise.webp',
    'love': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/up_love.webp'
}

# Разнообразие фраз
PRAISE = ["Умница, Миланочка! ☀️", "Ты просто волшебница, Миланочка! ✨", "Моя любимая садовница! 🌸"]
WATER_REMS = ["шепчет: «Мне бы глоточек водички...» 💧", "тихо намекает: «А не пора ли попить?» 💦", "нежно просит: «Чуточку воды, пожалуйста?» 🌱"]
FUN_FACTS = ["Герань очищает воздух и помогает спать спокойно. 💕", "Герани отпугивают комаров! 🦸‍♀️", "Герани — путешественницы из Африки, но полюбили твой домик! 🌍"]
LEVELS = [(0, "Росточек 🌱"), (10, "Госпожа Лейка 💧"), (30, "Лепесточек 🌸"), (60, "Хранительница цветения 🌿"), (100, "Цветочная фея 🌷")]

class Form(StatesGroup):
    waiting_photo1 = State()
    waiting_name1 = State()
    waiting_photo2 = State()
    waiting_name2 = State()
    lesson_light = State()
    lesson_water = State()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"plants": {}, "milanochka": {"level": LEVELS[0][1], "xp_total": 0, "petals": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8
