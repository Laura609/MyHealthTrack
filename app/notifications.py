from aiogram import Bot
from datetime import datetime


async def send_medication_reminder(patient_id, medication_name, dosage, time, bot: Bot):
    message = f"Напоминание: Принять {medication_name} ({dosage}) в {time.strftime('%H:%M')}"
    await bot.send_message(patient_id, message, parse_mode="Markdown")  # Используйте строку "Markdown"
