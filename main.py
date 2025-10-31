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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

# Твои данные
BOT_TOKEN = os.getenv('BOT_TOKEN')
MASHA_ID = 390005162
MILANA_ID = 436264598
DATA_FILE = 'data.json'

# ТВОИ ПУПЫ — вставлены!
PUP_IMAGES = {
    'happy': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_happy.webp',
    'sad': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_sad.webp',
    'surprise': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/pup_surprise.webp',
    'love': 'https://raw.githubusercontent.com/kondaevama/pup-bot-milanochka/refs/heads/main/up_love.webp'
}

# Разнообразие
PRAISE = ["Умница, Миланочка! ☀️", "Ты просто волшебница, Миланочка! ✨", "Моя любимая садовница! 🌸"]
WATER_REMS = ["шепчет: «Мне бы глоточек водички...» 💧", "тихо намекает: «А не пора ли попить?» 💦", "нежно просит: «Чуточку воды, пожалуйста?» 🌱"]
FUN_FACTS = ["Герань очищает воздух и помогает спать спокойно. 💕", "Герани отпугивают комаров! 🦸‍♀️", "Герани — путешественницы из Африки, но полюбили твой домик! 🌍"]
LEVELS = [(0, "Росточек 🌱"), (10, "Госпожа Лейка 💧"), (30, "Лепесточек 🌸"), (60, "Хранительница цветения 🌿"), (100, "Цветочная фея 🌷")]

class Form(States
