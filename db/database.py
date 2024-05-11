from fastapi import HTTPException, status
from sqlmodel import create_engine, Session, SQLModel

from db.tables.users import User

# sqlite_file_name = "./database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)


def get_session():
    session_engine: Session = Session(engine)
    try:
        with session_engine as session:
            yield session
    except Exception as e:
        print(f"Database connection error: {e.args[0]}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
        )
    finally:
        session_engine.close()
