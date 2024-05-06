from sqlmodel import create_engine, SQLModel

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SQLModel.metadata.create_all(engine)
