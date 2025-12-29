from src.daos.title_dao import TitleDAO
from src.daos.copy_dao import CopyDAO
from src.models.entities import Title, Copy, CopyStatus
from src.utils import InvalidParameterException


class CopyService:

    def __init__(self, db_manager):
        self._copy_dao = CopyDAO(db_manager)
        self._title_dao = TitleDAO(db_manager)

    def add_new_copy(self, title_id: int, code: str, location: str | None, status: CopyStatus ) -> Copy | None:

        location = location.strip() if location else None

        title = self._title_dao.get_by_id(title_id)
        if not title:
            raise InvalidParameterException("Title not found")

        copy = Copy(0, title, code, location, status)
        if self._copy_dao.create(copy):
            return copy
        return None

    def update_copy(self,copy_id: int, title_id: int, code: str, location: str | None, status: CopyStatus) -> bool:

        location = location.strip() if location else None

        title = self._title_dao.get_by_id(title_id)
        if not title:
            raise InvalidParameterException("Title not found")

        copy = Copy(copy_id, title, code, location, status)
        return self._copy_dao.update(copy)

    def remove_copy(self, copy_id: int) -> bool:
        return self._copy_dao.delete(copy_id)

    def get_copies(self, offset: int, limit: int) -> list:
        return self._copy_dao.get_copies(offset, limit)