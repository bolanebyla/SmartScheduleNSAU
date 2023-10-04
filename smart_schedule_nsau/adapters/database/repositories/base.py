import attr
from sqlalchemy.ext.asyncio import AsyncSession


@attr.dataclass(frozen=True)
class BaseRepositoryAsync:
    session: AsyncSession
