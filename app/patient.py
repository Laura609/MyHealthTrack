from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app import keyboards as kb  # Импортируем клавиатуры

patient = Router()


# Стартовая команда для пациента
@patient.message(CommandStart())
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    # Проверка, если пациент еще не зарегистрирован в БД, например:
    # await set_user(tg_id, name=message.from_user.full_name)
    await message.answer(
        "Добро пожаловать в бот! Вы можете просматривать свои данные о здоровье и получать рекомендации от врача."
        " Что вы хотите сделать?",
        reply_markup=kb.patient  # Используем клавиатуру для пациента (без скобок)
    )


# Просмотр данных о здоровье
@patient.callback_query(F.data == 'view_health_data')
async def view_health_data(callback_query: CallbackQuery):
    tg_id = callback_query.from_user.id
    # Получаем данные о здоровье пациента из БД
    # health_data = await get_patient_health_data(tg_id)
    await callback_query.answer("Здесь будут отображаться ваши данные о здоровье...")
    # Отправляем данные о здоровье


# Получение рекомендаций от врача
@patient.callback_query(F.data == 'view_recommendations')
async def view_recommendations(callback_query: CallbackQuery):
    tg_id = callback_query.from_user.id
    # Получаем рекомендации для пациента
    # recommendations = await get_recommendations(tg_id)
    await callback_query.answer("Здесь будут ваши рекомендации от врача.")
    # Отправляем рекомендации пациенту
