from typing import Any, Sequence

from approck_sqlalchemy_utils.model import Base
from multimethod import multimethod as overload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Delete, Select, Update

from approck_services.base import BaseService


class BaseSQLAlchemyService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()

        self.session = session

    async def _create(self, instance: Base) -> Base:
        instance = await self._save(instance)
        await self.session.refresh(instance)

        return instance

    async def _find(
        self,
        statement: Select,
        params: Any = None,
        bind_arguments: Any = None,
    ) -> Sequence[Base]:
        return (
            (await self.session.scalars(statement=statement, params=params, bind_arguments=bind_arguments))
            .unique()
            .all()
        )

    async def _find_one(
        self,
        statement: Select,
        params: Any = None,
        bind_arguments: Any = None,
    ) -> Base | None:
        return await self.session.scalar(statement=statement, params=params, bind_arguments=bind_arguments)

    async def _find_one_or_fail(
        self,
        statement: Select,
        params: Any = None,
        bind_arguments: Any = None,
    ) -> Base:
        instance = await self._find_one(statement=statement, params=params, bind_arguments=bind_arguments)

        if instance is None:
            raise NoResultFound(f"{statement.froms} not found")

        return instance

    async def _update(
        self,
        statement: Update,
        params: Any = None,
        bind_arguments: Any = None,
    ) -> None:
        await self.session.execute(statement=statement, params=params, bind_arguments=bind_arguments)
        await self.session.commit()

    async def _delete(
        self,
        statement: Delete,
        params: Any = None,
        bind_arguments: Any = None,
    ) -> None:
        await self.session.execute(
            statement=statement,
            params=params,
            bind_arguments=bind_arguments,
        )
        await self.session.commit()

    @overload
    async def _remove(self, instance: Base) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    @overload
    async def _remove(self, instances: Sequence[Base]) -> None:
        for instance in instances:
            await self.session.delete(instance)

        await self.session.commit()

    @overload
    async def _pre_save(self, instance: Base, **kwargs) -> Base:
        return await self.session.merge(instance, **kwargs)

    @overload
    async def _pre_save(self, instances: Sequence[Base]) -> Sequence[Base]:
        self.session.add_all(instances)
        await self.session.flush(instances)
        return instances

    @overload
    async def _save(self, instance: Base, **kwargs) -> Base:
        instance = await self._pre_save(instance, **kwargs)
        await self.session.commit()
        return instance

    @overload
    async def _save(self, instances: Sequence[Base]) -> Sequence[Base]:
        instances = await self._pre_save(instances)
        await self.session.commit()
        return instances
