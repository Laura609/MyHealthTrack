from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from app.notifications import send_medication_reminder
from app.database import session
from app.database.models import MedicationSchedule
from aiogram import Bot


# Инициализация планировщика
scheduler = AsyncIOScheduler()


def start_scheduler(bot: Bot):
    scheduler.start()

    # Запускаем задачу каждые 5 минут
    scheduler.add_job(check_medication_schedule, IntervalTrigger(minutes=5, jitter=60), args=[bot])


async def check_medication_schedule(bot: Bot):
    session = Session()
    now = datetime.now()

    # Получаем все расписания, которые наступают в будущем или близки к текущему времени
    schedules = session.query(MedicationSchedule).filter(MedicationSchedule.time > now).all()

    for schedule in schedules:
        # Отправляем напоминание пациенту
        await send_medication_reminder(schedule.patient_id, schedule.medication.name, schedule.medication.dosage,
                                       schedule.time, bot)

    session.close()
