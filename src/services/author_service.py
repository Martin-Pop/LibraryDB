from src.daos.author_dao import AuthorDAO
from src.models.entities import Author
from src.utils import InvalidParameterException

class AuthorService:

    def __init__(self, db_manager):
        self._dao = AuthorDAO(db_manager)

    def _validate(self, name: str):
        """
        Validates authors parameters
        :param name: name must be at least 1 character long
        :raises: InvalidParameterException if invalid parameters
        """

        if len(name) < 1:
            raise InvalidParameterException("Invalid author parameters: Name must be at least 1 character")

    def add_new_author(self, name: str, nationality: str | None) -> Author | None:
        """
        Adds new author
        :param name: authors name
        :param nationality: authors nationality (can be None)
        :return: author object
        """
        name = name.strip() if name else ""
        nationality = nationality.strip() if nationality else None

        self._validate(name)

        author = Author(0, name, nationality)
        if self._dao.create(author):
            return author
        return None

    def update_author(self, _id: int, name: str, nationality: str | None) -> bool:
        """
        Updates author
        :param _id: authors db id
        :param name: authors name
        :param nationality: authors nationality (can be None)
        :return: True if update was success else False
        """
        name = name.strip() if name else ""
        nationality = nationality.strip() if nationality else None

        self._validate(name)

        author = Author(_id, name, nationality)
        return self._dao.update(author)

    def remove_author(self, _id: int) -> bool:
        """
        Deletes author
        :param _id: authors db id
        :return: True if delete was success else False
        """
        return self._dao.delete(_id)

    def get_authors(self, offset: int, limit: int) -> list:
        return self._dao.get_authors(offset, limit)

    def get_by_id(self, author_id: int) -> Author:
        return self._dao.get_by_id(author_id)