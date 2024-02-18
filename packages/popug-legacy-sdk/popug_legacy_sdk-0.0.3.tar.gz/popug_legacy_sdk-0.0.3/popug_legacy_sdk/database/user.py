from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from popug_legacy_sdk.database import Base
from popug_legacy_sdk.database.base import BaseRepo
from popug_legacy_sdk.schemas import Pagination


class ModelRepos(BaseRepo):
    def __init__(self, session: AsyncSession, model: Type[Base] | None = None):
        super().__init__(session, model)

    async def get_by_field(self, data: int | str, field: str):
        query = self._query.where(getattr(self._model, field) == data)
        return await self(query).get_one()

    async def set_filter(self, data: int | str, field: str):
        query = self._query.where(getattr(self._model, field) == data)
        return self(query)

    async def add(self, data: dict[str, Any]):
        new_data = self._model(**data)
        self._session.add(new_data)
        return await self(new_data).apply(flush=True)

    async def get_all_data(self, pagination: Pagination = None):
        query = self._query
        if pagination is not None:
            query = await self.use_pagination(
                pagination.page_size, pagination.page
            )
        return await self(query).get_all()
