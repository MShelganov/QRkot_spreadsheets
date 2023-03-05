from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_before_update,
                                check_charity_project_name_duplilcate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreateSchema, CharityProjectDBSchema,
                         CharityProjectUpdateSchema)
from app.services import constants as const
from app.services.funds_allocation import allocate_donation_funds

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDBSchema],
    response_model_exclude_none=True,
    summary=const.GET_ALL_CHARITY_PROJECTS
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Доступно для всех посетителей.
    Возвращает список всех проектов.
    """
    return await charity_project_crud.get_all(session=session)


@router.post(
    '/',
    response_model=CharityProjectDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=const.CREATE_CHARITY_PROJECTS
)
async def create_charity_project(
    charity_project: CharityProjectCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Создает благотворительный проект.
     - **name** — название проекта;
     - **description** — описание проекта;
     - **full_amount** — сумма сбора.
    """
    await check_charity_project_name_duplilcate(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )
    await allocate_donation_funds(session=session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    dependencies=[Depends(current_superuser)],
    summary=const.DELETE_CHARITY_PROJECTS
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Удаляет благотворительный проект. Нельзя удалить проект, в который
    уже были проинвестированы средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_before_delete(
        charity_project_id=project_id, session=session
    )
    deleted_charity_project = await charity_project_crud.remove(
        db_obj=charity_project, session=session
    )
    return deleted_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDBSchema,
    dependencies=[Depends(current_superuser)],
    summary=const.UPDATE_CHARITY_PROJECT
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Редактирует благотворительный проект.
    Закрытый проект нельзя редактировать, также нельзя установить требуемую
    сумму меньше уже вложенной.
    """
    charity_project_db = await check_charity_project_before_update(
        charity_project_id=project_id,
        session=session,
        charity_project_in=charity_project_in
    )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project_db, obj_in=charity_project_in, session=session
    )
    return charity_project
