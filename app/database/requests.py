from app.database.models import async_session, Patient, Doctor
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def set_user(tg_id, name=None, attending_physician=None, diagnosis=None):
    async with async_session() as session:  # Открываем сессию с базой данных
        async with session.begin():  # Используем транзакцию для атомарности операции
            # Ищем пациента с таким tg_id в базе данных
            user = await session.scalar(select(Patient).where(Patient.tg_id == tg_id))

            # Если пациента нет в базе данных, создаём нового
            if not user:
                # Если имя не передано, генерируем значение по умолчанию
                name = name if name else "Без имени"
                attending_physician = attending_physician if attending_physician else "Не назначен"
                diagnosis = diagnosis if diagnosis else "Не указан"

                # Создаём нового пациента с переданными данными
                new_patient = Patient(
                    tg_id=tg_id,
                    name=name,  # Используем переданное или значение по умолчанию
                    attending_physician=attending_physician,
                    diagnosis=diagnosis
                )
                session.add(new_patient)  # Добавляем пациента в сессию
                await session.commit()  # Подтверждаем изменения
                print(f"Пациент с tg_id {tg_id} и именем '{name}' добавлен в базу данных.")
            else:
                # Если пациент найден, обновляем его данные, если они были переданы
                if name:
                    user.name = name
                if attending_physician:
                    user.attending_physician = attending_physician
                if diagnosis:
                    user.diagnosis = diagnosis

                # Сохраняем изменения, если что-то было обновлено
                await session.commit()
                print(f"Данные пациента с tg_id {tg_id} обновлены.")

            # Если назначен новый врач, создаем или обновляем связь с врачом
            if attending_physician:
                doctor = await session.scalar(select(Doctor).where(Doctor.name == attending_physician))
                if doctor:
                    user.attending_physician = doctor.name
                else:
                    # Если врача нет в базе, создаём нового
                    new_doctor = Doctor(name=attending_physician)
                    session.add(new_doctor)
                    await session.commit()
                    print(f"Врач '{attending_physician}' добавлен в базу данных.")
