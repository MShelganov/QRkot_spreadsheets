from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id, session: AsyncSession):
        db_obj = await session.scalar(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj

    async def get_all(self, session: AsyncSession):
        db_objs = await session.scalars(select(self.model))
        return db_objs.all()

    async def create(
        self, obj_in, session: AsyncSession, user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            for field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: int, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def read_not_closed(self, session: AsyncSession):
        charity_projects = await session.scalars(
            select(self.model).where(self.model.fully_invested.is_(False))
                              .order_by(asc('create_date'))
        )
        return charity_projects
