from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import (AllDonationsDBSchema, DonationCreateSchema,
                         DonationDBSchema)
from app.services import constants as const
from app.services.funds_allocation import allocate_donation_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationsDBSchema],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=const.GET_ALL_DONATIONS
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_all(session=session)


@router.post(
    '/',
    response_model=DonationDBSchema,
    response_model_exclude_none=True,
    summary=const.CREATE_DONATION
)
async def create_donation(
    donation_in: DonationCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Досутпно для авторизированного пользователя.
    Создать пожертвование.
      - **comment** — комментарий;
      - **full_amount** — сумма пожертвования.
    """
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await allocate_donation_funds(session=session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDBSchema],
    summary=const.GET_MY_DONATIONS
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Доступно для авторизированного пользователя.
    Возвращает список пожертвований пользователя, выполняющего запрос.
    """
    return await donation_crud.get_user_donations(user=user, session=session)
