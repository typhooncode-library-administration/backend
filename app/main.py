import datetime
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from typing import List
from crud import crud
from dependencies import get_db


models.Base.metadata.create_all(bind=engine)

# Erstelle die FastAPI-App
app = FastAPI()

# CORSMiddleware, damit Anfragen von http://localhost:3000 zugelassen werden
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/books", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/books", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.post("/reservations", response_model=schemas.Reservation)
def add_reservation(
    reservation: schemas.ReservationCreate, db: Session = Depends(get_db)
):
    db_reservation = crud.create_reservation(db, reservation)
    if db_reservation is None:
        raise HTTPException(
            status_code=400, detail="Buch nicht verfügbar oder existiert nicht"
        )
    return db_reservation


@app.delete("/reservations/{reservation_id}", response_model=dict)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    success = crud.delete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservierung nicht gefunden")
    return {"message": "Reservierung storniert"}


@app.post("/events", response_model=schemas.Event)
def add_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)


@app.delete("/events/{event_id}", response_model=dict)
def remove_event(event_id: int, db: Session = Depends(get_db)):
    success = crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event nicht gefunden")
    return {"message": "Event abgesagt"}


@app.get("/events", response_model=List[schemas.Event])
def read_all_events(db: Session = Depends(get_db)):
    # Ruft alle Events ohne Pagination ab
    events = db.query(models.Event).all()
    return events


@app.post("/event_registrations", response_model=schemas.EventRegistration)
def register_event(reg: schemas.EventRegistrationCreate, db: Session = Depends(get_db)):
    db_reg = crud.register_for_event(db, reg)
    if db_reg is None:
        raise HTTPException(
            status_code=400,
            detail="Registrierung fehlgeschlagen (Event voll oder nicht vorhanden)",
        )
    return db_reg


@app.delete("/event_registrations", response_model=dict)
def unregister_event(
    event_id: int = Query(...), user_id: int = Query(...), db: Session = Depends(get_db)
):
    success = crud.unregister_from_event(db, event_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registrierung nicht gefunden")
    return {"message": "Vom Event abgemeldet"}
