import threading
from contextlib import AsyncContextDecorator

from classic.components import component
from classic.sql_storage.utils import ThreadSafeCounter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


@component(init=False)
class TransactionContextAsync(AsyncContextDecorator):

    def __init__(self, **kwargs):
        kwargs.pop('class_', None)
        kwargs.pop('expire_on_commit', None)

        self.create_session = sessionmaker(
            class_=AsyncSession, expire_on_commit=False, **kwargs
        )
        self._storage = threading.local()
        self._calls = ThreadSafeCounter()

    def _get_session_if_exists(self):
        return getattr(self._storage, 'session', None)

    @property
    def current_session(self) -> AsyncSession:
        session = self._get_session_if_exists()
        if session is None:
            session = self.create_session()
            self._storage.session = session
        return session

    async def __aenter__(self):
        self._calls.increment()
        return self

    async def __aexit__(self, *exc):
        self._calls.decrement()

        if self._calls.is_last:
            session = self._get_session_if_exists()
            if session is None:
                return None

            if exc[0] is None:
                await session.commit()
            else:
                await session.rollback()

            await session.close()
        return False
