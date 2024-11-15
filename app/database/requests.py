from app.database.models import async_session, Patient
from sqlalchemy import select


async def set_user(tg_id, name=None, attending_physician=None, diagnosis=None):
    async with async_session() as session:
        # Ищем пациента с таким tg_id в базе данных
        user = await session.scalar(select(Patient).where(Patient.tg_id == tg_id))

        # Если пациента нет в базе данных, создаём нового
        if not user:
            # Если имя не передано, генерируем значение по умолчанию
            name = name if name else "Без имени"

            # Создаём нового пациента с переданными данными
            new_patient = Patient(
                tg_id=tg_id,
                name=name,  # Используем переданное или значение по умолчанию
                attending_physician=attending_physician if attending_physician else "Не назначен",
                diagnosis=diagnosis if diagnosis else "Не указан"
            )
            session.add(new_patient)
            await session.commit()
            print(f"Пациент с tg_id {tg_id} и именем '{name}' добавлен в базу данных.")
        else:
            print(f"Пациент с tg_id {tg_id} уже существует в базе данных.")
