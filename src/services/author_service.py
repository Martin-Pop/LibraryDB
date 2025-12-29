from src.daos.author_dao import AuthorDAO
from src.models.entities import Author
from src.utils import InvalidParameterException

class AuthorService:

    def __init__(self, db_manager):
        self._dao = AuthorDAO(db_manager)

    def _validate(self, first_name: str):
        """
        Validates authors parameters
        :param first_name: first name must be at least 1 character long
        :raises: InvalidParameterException if invalid parameters
        """

        if len(first_name) < 1:
            raise InvalidParameterException("Invalid author parameters: First name must be at least 1 character")

    def add_new_author(self, first_name: str, last_name: str, nationality: str | None) -> Author | None:
        """
        Adds new author
        :param first_name: authors first name
        :param last_name: authors last name
        :param nationality: authors nationality (can be None)
        :return: author object
        """
        first_name = first_name.strip() if first_name else ""
        last_name = last_name.strip() if last_name else ""
        nationality = nationality.strip() if nationality else None

        self._validate(first_name)

        author = Author(0, first_name, last_name, nationality)
        if self._dao.create(author):
            return author
        return None

    def update_author(self, _id: int, first_name: str, last_name: str, nationality: str | None) -> bool:
        """
        Updates author
        :param _id: authors db id
        :param first_name: authors first name
        :param last_name: authors last name
        :param nationality: authors nationality (can be None)
        :return: True if update was success else False
        """
        first_name = first_name.strip() if first_name else ""
        last_name = last_name.strip() if last_name else ""
        nationality = nationality.strip() if nationality else None

        self._validate(first_name)

        author = Author(_id, first_name, last_name, nationality)
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