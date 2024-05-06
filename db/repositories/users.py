from uuid import UUID

from sqlmodel import Session, select

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from db.database import engine
from db.tables.users import User


class UsersRepository:

    def list(self) -> list[UserRead]:
        with Session(engine) as session:
            statement = select(User)
            users_db = session.execute(statement).scalars().all()
            list_users: [UserRead] = []

            for user in users_db:
                list_users.append(UserRead(**user.__dict__))

            return list_users

    def get_one(self, id: UUID) -> UserRead:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            user_db = session.execute(statement).scalar_one()
            return UserRead(**user_db.__dict__)

    def create(self, user: UserCreate) -> UserRead:
        with Session(engine) as session:
            user_db = User(**user.dict())
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return UserRead(**user_db.__dict__)

    def update(self, id: UUID, user: UserUpdate) -> UserRead:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            user_db = session.execute(statement).scalar_one()
            for field, value in user.dict(exclude_unset=True).items():
                setattr(user_db, field, value)

            session.commit()
            session.refresh(user_db)
            return UserRead(**user_db.__dict__)

    def delete(self, id: UUID) -> None:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            user_db = session.execute(statement).scalar_one()
            session.delete(user_db)
            session.commit()

            return None
