from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdateSchema
from app.services import constants as const


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверяет, существует ли проект в базе."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=const.ERR_NOT_FOUND % charity_project_id
        )
    return charity_project


async def check_charity_project_name_duplilcate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """Проверяет название проекта на уникальность."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.ERR_NAME_EXIST
        )


async def check_charity_project_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """
    Проверяет, существут ли проект в базе и были ли в него
    инвестированы средства.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.ERR_HAS_INVEST
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверят, соответствует ли проект условиям для редактирования:
        - проект должен существовать в базе;
        - проект не должен быть закрыт;
        - нельзя установить требуемую сумму меньше уже вложенной;
        - новое название проекта должно быть уникальным.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.ERR_PROJECT_CLOSED
        )
    full_amount_update_value = charity_project_in.full_amount
    if (full_amount_update_value and
       charity_project.invested_amount > full_amount_update_value):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=const.ERR_FULL_AMOUNT
        )
    name_update_value = charity_project_in.name
    await check_charity_project_name_duplilcate(
        charity_project_name=name_update_value, session=session
    )
    return charity_project
