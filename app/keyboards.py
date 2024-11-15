from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для страницы пациента
patient = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть данные о здоровье", callback_data="view_health_data")],
    [InlineKeyboardButton(text="Получить рекомендации", callback_data="view_recommendations")]
])

# Клавиатура для страницы врача
doctor = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть данные пациента", callback_data="view_patient_data")],
    [InlineKeyboardButton(text="Добавить рекомендацию", callback_data="add_recommendation")],
    [InlineKeyboardButton(text="Построить график лекарств", callback_data="build_medication_schedule")]
])
