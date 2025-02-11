from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Library(Base):
    __tablename__ = "library"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    city = Column(String(100))
    postal_code = Column(String(10))
    phone = Column(String(20))
    email = Column(String(100))
    # Beziehung: eine Bibliothek hat viele Bücher und Events
    books = relationship("Book", back_populates="library")
    events = relationship("Event", back_populates="library")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(50), nullable=False)  # 'student' oder 'employee'
    first_name = Column(String(100))
    last_name = Column(String(100))
    # Beziehungen
    reservations = relationship("Reservation", back_populates="user")
    event_registrations = relationship("EventRegistration", back_populates="user")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    library_id = Column(Integer, ForeignKey("library.id"), nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    publish_year = Column(Integer)
    total_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    library = relationship("Library", back_populates="books")
    reservations = relationship("Reservation", back_populates="book")


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reservation_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="pending")
    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    library_id = Column(Integer, ForeignKey("library.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    max_participants = Column(Integer)
    registered_participants = Column(Integer, default=0)
    library = relationship("Library", back_populates="events")
    registrations = relationship(
        "EventRegistration", back_populates="event", cascade="all, delete"
    )


class EventRegistration(Base):
    __tablename__ = "event_registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_user"),)
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="event_registrations")
