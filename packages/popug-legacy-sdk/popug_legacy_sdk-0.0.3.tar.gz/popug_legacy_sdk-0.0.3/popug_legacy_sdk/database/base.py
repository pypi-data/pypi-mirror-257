from typing import Type

from schemas.errors import NoContextError
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from popug_legacy_sdk.database import Base


class BaseRepo:
    def __init__(self, session: AsyncSession, model: Type[Base] | None = None):
        self._session = session
        self._model = model
        self._query = self._init_query()

    def _init_query(self):
        if self._model is not None:
            return select(self._model)

    def __call__(self, query: select):
        self._query = query
        return self

    async def apply(self, flush: bool = False):
        result = self.get()
        if flush:
            await self._session.flush()
        await self._session.commit()

        return result

    def get(self):
        if self._query is None:
            raise NoContextError
        return self._query

    async def use_pagination(self, page_size: int = 25, page: int = 1):
        query = self.get()
        return query.limit(page_size).offset((page - 1) * page_size)

    async def get_one(self):
        query = self.get()
        result = await self._session.execute(query)
        return result.scalar()

    async def get_all(self):
        query = self.get()
        result = await self._session.execute(query)
        return result.scalars(), await self.count()

    async def count(self):
        result = await self._session.execute(
            select(func.count()).select_from(self._model)
        )
        return result.scalar() or 0

    async def delete(self, data: Type[Base] | None = None):
        if data:
            await self._session.delete(data)
            await self._session.commit()
