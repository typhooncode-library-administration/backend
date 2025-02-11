from pydantic import BaseModel
from typing import Optional, List
import datetime


class BookBase(BaseModel):
    title: str
    author: Optional[str]
    publisher: Optional[str]
    publish_year: Optional[int]
    total_quantity: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    available_quantity: int

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    user_id: int
    book_id: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    reservation_date: datetime.datetime
    status: str

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime.datetime
    end_time: datetime.datetime
    max_participants: int


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    registered_participants: int

    class Config:
        orm_mode = True


class EventRegistrationBase(BaseModel):
    event_id: int
    user_id: int


class EventRegistrationCreate(EventRegistrationBase):
    pass


class EventRegistration(EventRegistrationBase):
    id: int
    registration_date: datetime.datetime

    class Config:
        orm_mode = True
