from approck_sqlalchemy_utils.mocks import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from approck_services.sqlalchemy import BaseSQLAlchemyService


class BaseFastAPISQLAlchemyService(BaseSQLAlchemyService):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session)
