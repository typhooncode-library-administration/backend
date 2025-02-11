import datetime
from sqlalchemy.orm import Session
from models import models
from schemas import schemas


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        library_id=1,  # Nur eine Bibliothek
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        publish_year=book.publish_year,
        total_quantity=book.total_quantity,
        available_quantity=book.total_quantity,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # Prüfen, ob das Buch verfügbar ist:
    db_book = (
        db.query(models.Book).filter(models.Book.id == reservation.book_id).first()
    )
    if not db_book:
        return None
    if db_book.available_quantity < 1:
        return None
    db_reservation = models.Reservation(
        user_id=reservation.user_id, book_id=reservation.book_id
    )
    db_book.available_quantity -= 1
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_reservation(db: Session, reservation_id: int):
    res = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .first()
    )
    if res:
        # Falls bereits genehmigt, Buch wieder freigeben:
        if res.status == "approved":
            db_book = (
                db.query(models.Book).filter(models.Book.id == res.book_id).first()
            )
            if db_book:
                db_book.available_quantity += 1
        db.delete(res)
        db.commit()
        return True
    return False


def get_events(db: Session):
    # Hier wird eine Liste aller Event-Objekte aus der Datenbank zurückgegeben
    return db.query(models.Event).all()


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        library_id=1,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        max_participants=event.max_participants,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        return True
    return False


def register_for_event(db: Session, reg: schemas.EventRegistrationCreate):
    event = db.query(models.Event).filter(models.Event.id == reg.event_id).first()
    if not event:
        return None
    if event.registered_participants >= event.max_participants:
        return None
    db_reg = models.EventRegistration(event_id=reg.event_id, user_id=reg.user_id)
    event.registered_participants += 1
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg


def unregister_from_event(db: Session, event_id: int, user_id: int):
    reg = (
        db.query(models.EventRegistration)
        .filter(
            models.EventRegistration.event_id == event_id,
            models.EventRegistration.user_id == user_id,
        )
        .first()
    )
    if reg:
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if event and event.registered_participants > 0:
            event.registered_participants -= 1
        db.delete(reg)
        db.commit()
        return True
    return False
