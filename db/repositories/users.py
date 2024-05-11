from uuid import UUID

from sqlmodel import Session, select

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from db.tables.users import User


class UsersRepository:

    def list(self, db: Session) -> list[UserRead]:
        statement = select(User)
        users_db = db.execute(statement).scalars().all()
        list_users: [UserRead] = []

        for user in users_db:
            list_users.append(UserRead(**user.__dict__))

        return list_users

    def get_one(self, db: Session, id: UUID) -> UserRead:
        statement = select(User).where(User.id == id)
        user_db = db.execute(statement).scalar_one()

        return UserRead(**user_db.__dict__)

    def create(self, db: Session, user: UserCreate) -> UserRead:
        user_db = User(**user.model_dump())
        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        return UserRead(**user_db.__dict__)

    def update(self, db: Session, id: UUID, user: UserUpdate) -> UserRead:
        statement = select(User).where(User.id == id)
        user_db = db.execute(statement).scalar_one()
        for field, value in user.model_dump(exclude_unset=True).items():
            setattr(user_db, field, value)

        db.commit()
        db.refresh(user_db)

        return UserRead(**user_db.__dict__)

    def delete(self, db: Session, id: UUID) -> None:
        statement = select(User).where(User.id == id)
        user_db = db.execute(statement).scalar_one()
        db.delete(user_db)
        db.commit()

        return None
