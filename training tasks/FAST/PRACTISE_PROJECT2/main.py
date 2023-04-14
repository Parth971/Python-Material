from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException

from models import User, Gender, Role, UserUpdate

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("480135fd-eb91-452e-b8c9-b1e94b329f36"),
        first_name='Parth',
        last_name='Desai',
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    ),
    User(
        id=UUID("c87a6257-2772-4fc0-9ba5-31fe3f753a77"),
        first_name='XYZ',
        last_name='ABC',
        gender=Gender.female,
        roles=[Role.admin, Role.student]
    )
]


@app.get('/')
async def root():
    return {'msg': 'Hello'}


@app.get('/api/v1/users')
async def user_list_view():
    return db


@app.post('/api/v1/users')
async def user_create_view(user: User):
    db.append(user)
    return {'id': user.id}


@app.delete('/api/v1/users/{user_id}')
async def user_delete_view(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return

    raise HTTPException(
        status_code=404,
        detail=f'User with id: {user_id} does not exists.'
    )


@app.put('/api/v1/users/{user_id}')
async def user_delete_view(user_id: UUID, updated_user: UserUpdate):
    for user in db:
        if user.id == user_id:
            if updated_user.first_name is not None:
                user.first_name = updated_user.first_name
            if updated_user.last_name is not None:
                user.last_name = updated_user.last_name
            if updated_user.middle_name is not None:
                user.middle_name = updated_user.middle_name
            if updated_user.roles is not None:
                user.roles = updated_user.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f'User with id: {user_id} does not exists.'
    )
