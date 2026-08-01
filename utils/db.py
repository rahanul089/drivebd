"""
DriveBD - Database layer (SQLAlchemy models + session helper)
Uses SQLite by default (drivebd.db) - swap DATABASE_URL env var for Postgres/Supabase.
"""
import os
import datetime as dt
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, DateTime, Date,
    ForeignKey, Text
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "drivebd.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False, default="driver")  # driver | owner | admin
    nid = Column(String(30))
    phone = Column(String(20))
    license_no = Column(String(30))
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    vehicles = relationship("Vehicle", back_populates="owner", cascade="all,delete")
    payments = relationship("Payment", back_populates="user", cascade="all,delete")
    documents = relationship("Document", back_populates="user", cascade="all,delete")
    notifications = relationship("Notification", back_populates="user", cascade="all,delete")
    appeals = relationship("Appeal", back_populates="user", cascade="all,delete")


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    reg_number = Column(String(30), unique=True, nullable=False)
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    vehicle_type = Column(String(30))
    engine_no = Column(String(40))
    chassis_no = Column(String(40))
    status = Column(String(20), default="active")  # active | suspended | scrapped
    registered_on = Column(Date, default=dt.date.today)

    owner = relationship("User", back_populates="vehicles")
    violations = relationship("Violation", back_populates="vehicle", cascade="all,delete")
    documents = relationship("Document", back_populates="vehicle", cascade="all,delete")
    service_history = relationship("ServiceHistory", back_populates="vehicle", cascade="all,delete")


class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    violation_type = Column(String(80))
    date = Column(Date, default=dt.date.today)
    location = Column(String(120))
    latitude = Column(Float)
    longitude = Column(Float)
    fine_amount = Column(Float, default=0)
    status = Column(String(20), default="unpaid")  # unpaid | paid | appealed | waived
    officer_name = Column(String(80))
    notes = Column(Text)

    vehicle = relationship("Vehicle", back_populates="violations")
    payments = relationship("Payment", back_populates="violation", cascade="all,delete")
    appeals = relationship("Appeal", back_populates="violation", cascade="all,delete")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    violation_id = Column(Integer, ForeignKey("violations.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    method = Column(String(30))  # bKash | Nagad | Card | Bank
    date = Column(Date, default=dt.date.today)
    status = Column(String(20), default="completed")
    reference_no = Column(String(40))

    violation = relationship("Violation", back_populates="payments")
    user = relationship("User", back_populates="payments")


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    doc_type = Column(String(50))  # NID | License | Registration | Fitness | Tax Token | Insurance
    file_path = Column(String(255))
    expiry_date = Column(Date, nullable=True)
    status = Column(String(20), default="valid")  # valid | expiring | expired
    uploaded_on = Column(Date, default=dt.date.today)

    user = relationship("User", back_populates="documents")
    vehicle = relationship("Vehicle", back_populates="documents")


class ServiceHistory(Base):
    __tablename__ = "service_history"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    service_date = Column(Date, default=dt.date.today)
    service_type = Column(String(80))
    cost = Column(Float)
    workshop = Column(String(100))
    mileage_km = Column(Integer)
    notes = Column(Text)

    vehicle = relationship("Vehicle", back_populates="service_history")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(255))
    category = Column(String(30), default="info")  # info | warning | alert
    date = Column(DateTime, default=dt.datetime.utcnow)
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")


class Appeal(Base):
    __tablename__ = "appeals"
    id = Column(Integer, primary_key=True)
    violation_id = Column(Integer, ForeignKey("violations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(Text)
    status = Column(String(20), default="pending")  # pending | approved | rejected
    date = Column(Date, default=dt.date.today)
    admin_comment = Column(Text)

    violation = relationship("Violation", back_populates="appeals")
    user = relationship("User", back_populates="appeals")


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(255))
    timestamp = Column(DateTime, default=dt.datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String(50), primary_key=True)
    value = Column(String(255))


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()
