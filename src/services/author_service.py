from src.daos.author_dao import AuthorDAO
from src.models.entities import Author
from src.utils import InvalidParameterException

class AuthorService:

    def __init__(self, db_manager):
        self._dao = AuthorDAO(db_manager)

    def _validate(self, first_name, last_name, nationality):
        errors = []

        if not isinstance(first_name, str):
            errors.append(f"First name must be str got: {type(first_name).__name__}")

        if not isinstance(last_name, str):
            errors.append(f"Last name must be str got: {type(last_name).__name__}")

        if not isinstance(nationality, str):
            errors.append(f"Nationality must be str got: {type(nationality).__name__}")

        first_name = first_name.strip()
        last_name = last_name.strip()
        nationality = nationality.strip()

        if len(first_name) < 1:
            errors.append(f"First name must be at least 1 character")

        return errors, first_name, last_name, nationality

    def add_new_author(self, first_name, last_name, nationality):

        errors, first_name, last_name, nationality = self._validate(first_name, last_name, nationality)

        if len(errors) > 0:
            raise InvalidParameterException("Invalid author parameters" + "\n".join(errors))

        author = Author(
            id=0,
            first_name=first_name,
            last_name=last_name,
            nationality=nationality,
        )

        self._dao.create(author)
        return author

    def update_author(self, _id, first_name, last_name, nationality):

        errors, first_name, last_name, nationality = self._validate(first_name, last_name, nationality)
        if len(errors) > 0:
            raise InvalidParameterException("Invalid author parameters" + "\n".join(errors))

        author = Author(
            id=_id,
            first_name=first_name,
            last_name=last_name,
            nationality=nationality,
        )

        return self._dao.update(author)

    def delete_author(self, _id):
        return self._dao.delete(_id)