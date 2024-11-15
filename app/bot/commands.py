from aiogram import types
from aiogram.dispatcher import Dispatcher
from app.database import Session
from app.database.models import Medication, MedicationSchedule
from datetime import datetime


async def add_medication_schedule(message: types.Message):
    args = message.text.split(' ')

    # Пример команды: /add_medication_schedule patient_id medication_id dosage time
    patient_id = int(args[1])
    medication_id = int(args[2])
    dosage = args[3]
    time = datetime.strptime(args[4], "%Y-%m-%d %H:%M")

    # Добавление записи в базу данных
    session = Session()
    medication_schedule = MedicationSchedule(patient_id=patient_id, medication_id=medication_id, time=time)
    session.add(medication_schedule)
    session.commit()
    session.close()

    await message.answer(f"График приема лекарства для пациента {patient_id} успешно добавлен.")
