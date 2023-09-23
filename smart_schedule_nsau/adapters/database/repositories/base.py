from classic.components import component
from sqlalchemy.ext.asyncio import AsyncSession


@component
class BaseRepositoryAsync:
    session: AsyncSession
