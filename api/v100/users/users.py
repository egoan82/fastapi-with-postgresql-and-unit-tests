from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from db.database import get_session
from db.repositories.users import UsersRepository

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
async def list(
        repository: UsersRepository = Depends(UsersRepository),
        session: Session = Depends(get_session),
):
    return repository.list(db=session)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get_one(
        id: UUID,
        repository: UsersRepository = Depends(UsersRepository),
        session: Session = Depends(get_session),
):
    return repository.get_one(db=session, id=id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def create(
        user: UserCreate,
        repository: UsersRepository = Depends(UsersRepository),
        session: Session = Depends(get_session),
):
    return repository.create(db=session, user=user)


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def update(
        id: UUID,
        user: UserUpdate,
        repository: UsersRepository = Depends(UsersRepository),
        session: Session = Depends(get_session),
):
    return repository.update(db=session, id=id, user=user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
        id: UUID,
        repository: UsersRepository = Depends(UsersRepository),
        session: Session = Depends(get_session),
):
    return repository.delete(db=session, id=id)
