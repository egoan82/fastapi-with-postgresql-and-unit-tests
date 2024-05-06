from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.v100.schemas.users import UserRead, UserCreate, UserUpdate
from db.repositories.users import UsersRepository

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
async def users(
        repository: UsersRepository = Depends(UsersRepository),
):
    return repository.list()


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def user(
        id: UUID,
        repository: UsersRepository = Depends(UsersRepository),
):
    return repository.get_one(id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def create_user(
        user: UserCreate,
        repository: UsersRepository = Depends(UsersRepository),
):
    return repository.create(user)


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def update_user(
        id: UUID,
        user: UserUpdate,
        repository: UsersRepository = Depends(UsersRepository),
):
    return repository.update(id, user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        id: UUID,
        repository: UsersRepository = Depends(UsersRepository),
):
    return repository.delete(id)
