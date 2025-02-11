import os
from sqlalchemy import create_engine


def read_secret(secret_name: str, default: str = "") -> str:
    """
    Liest den Inhalt einer Secret-Datei aus dem Verzeichnis /run/secrets/.
    Falls die Datei nicht existiert, wird der Default-Wert zurückgegeben.
    """
    secret_path = os.path.join("/run/secrets", secret_name)
    try:
        with open(secret_path, "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        return default


# Auslesen und Speichern der Benutzer- und Passwort-Secrets:
DB_USER = read_secret("postgres-admin-username", "default_user")
DB_PASSWORD = read_secret("postgres-admin-password", "default_password")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@postgres:5432/Bibliotheksverwaltung"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
