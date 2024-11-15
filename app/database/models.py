from sqlalchemy import ForeignKey, String, Integer, BigInteger, Text, DateTime, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
from config import DB_URL

# Создаем асинхронный движок базы данных
engine = create_async_engine(url=DB_URL, echo=True)

# Создаем фабрику для сессий
async_session = async_sessionmaker(engine, class_=AsyncAttrs)


# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Модель пациента
class Patient(Base):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    attending_physician: Mapped[str] = mapped_column(String(100), nullable=True)
    diagnosis: Mapped[str] = mapped_column(String(200), nullable=True)

    # Связь с записями о здоровье
    health_data = relationship("HealthData", back_populates="patient")

    # Связь с графиками лекарств
    medication_schedule = relationship("MedicationSchedule", back_populates="patient")

    # Записи о консультациях с врачом
    consultations = relationship("Consultation", back_populates="patient")


# Модель врача
class Doctor(Base):
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)

    # Связь с записями консультаций
    consultations = relationship("Consultation", back_populates="doctor")


# Модель лекарства
class Medication(Base):
    __tablename__ = 'medications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    dosage: Mapped[str] = mapped_column(String(50), nullable=True)

    schedules = relationship("MedicationSchedule", back_populates="medication")


# Модель графика приема лекарства
class MedicationSchedule(Base):
    __tablename__ = 'medication_schedules'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), nullable=False)
    medication_id: Mapped[int] = mapped_column(ForeignKey('medications.id'), nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # Связь с пациентом и лекарством
    patient = relationship("Patient", back_populates="medication_schedule")
    medication = relationship("Medication", back_populates="schedules")


# Модель данных о здоровье
class HealthData(Base):
    __tablename__ = 'health_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    measurement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[float] = mapped_column(Integer, nullable=False)  # или Float, в зависимости от данных
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь с пациентом
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="health_data")


# Модель консультации
class Consultation(Base):
    __tablename__ = 'consultations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)

    # Связь с пациентом и врачом
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    physician_id: Mapped[int] = mapped_column(ForeignKey('doctors.id'))

    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")


# Функция для создания таблиц в базе данных
async def async_main():
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
