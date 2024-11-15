from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app import keyboards as kb  # Импортируем клавиатуры

doctor = Router()


# Команда /doctor - доступ к странице для врача
@doctor.message(Command('doctor'))
async def doctor_page(message: Message):
    doctor_id = message.from_user.id
    await message.answer(
        "Добро пожаловать в бот, Доктор! Вы можете управлять состоянием здоровья ваших пациентов.\n"
        "Что вы хотите сделать?",
        reply_markup=kb.doctor()  # Используем клавиатуру для врача
    )


# Просмотр данных пациента
@doctor.callback_query(F.data == 'view_patient_data')
async def view_patient_data(callback_query: CallbackQuery):
    await callback_query.answer("Введите TG ID пациента, чьи данные вы хотите просмотреть:")
    # Получение и отображение данных пациента из базы данных
    # patient_data = await get_patient_data(tg_id)
    await callback_query.message.answer("Здесь будут отображаться данные пациента...")


# Добавление рекомендации для пациента
@doctor.callback_query(F.data == 'add_recommendation')
async def add_recommendation_page(callback_query: CallbackQuery):
    await callback_query.answer("Введите TG ID пациента и рекомендации для него:")
    # Получение и сохранение рекомендаций
    await callback_query.message.answer("Рекомендации были отправлены пациенту!")


# Построение графика приема лекарств
@doctor.callback_query(F.data == 'build_medication_schedule')
async def build_medication_schedule_page(callback_query: CallbackQuery):
    await callback_query.answer("Введите TG ID пациента и график приема лекарства:")
    # Получение и сохранение графика приема лекарства
    await callback_query.message.answer("График был создан и отправлен пациенту!")
