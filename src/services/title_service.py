from src.daos.copy_dao import CopyDAO
from src.daos.title_dao import TitleDAO
from src.daos.author_dao import AuthorDAO
from src.models.entities import Title, Author
from src.main.utils import InvalidParameterException, ObjectAlreadyExistsException


class TitleService:

    def __init__(self, db_manager):
        self._db = db_manager
        self._title_dao = TitleDAO(db_manager)
        self._author_dao = AuthorDAO(db_manager)
        self._copy_dao = CopyDAO(db_manager)

    def _validate(self, title: str, isbn: str | None, page_count: int | None, price: float):
        errors = []
        if len(title) < 1:
            errors.append("Title must be specified")

        if len(title) > 200:
            errors.append("Title is too long .")

        if isbn:
            clean_isbn = isbn.replace("-", "").replace(" ", "")
            if not clean_isbn.isdigit():
                errors.append("ISBN must contain only numbers.")

            elif len(clean_isbn) < 10 or len(clean_isbn) > 13:
                errors.append("ISBN must be between 10 and 13 digits.")

        if page_count and page_count <= 0:
            errors.append("Invalid page count number.")

        if price < 0:
            errors.append("Invalid price.")

        if errors:
            raise InvalidParameterException(errors)

    def add_new_title(self, author_name: str, title: str, isbn: str | None, page_count: int | None, price: float, description: str | None) -> Title | None:

        title = title.strip() if title else ""
        isbn = isbn.strip() if isbn else None
        description = description.strip() if description else None

        self._validate(title, isbn, page_count, price)

        author = self._author_dao.get_by_name(author_name)
        if not author:
            author = Author(0, author_name, None)
            success = self._author_dao.create(author)
            if not success:
                raise InvalidParameterException("Author was not found and his creation failed.")

        book = Title(0, author, title, isbn, page_count, price, description)
        exists = self._title_dao.exists(book)
        if exists:
            raise ObjectAlreadyExistsException("Title from this author already exists.")

        if self._title_dao.create(book):
            return book
        return None

    def update_title(self, title_id: int, author_name: str, title: str, isbn: str | None, page_count: int | None, price: float, description: str | None) -> bool:

        title = title.strip() if title else ""
        isbn = isbn.strip() if isbn else None
        description = description.strip() if description else None

        self._validate(title, isbn, page_count, price)

        author = self._author_dao.get_by_name(author_name)
        if not author:
            author = Author(0, author_name, None)
            success = self._author_dao.create(author)
            if not success:
                raise InvalidParameterException("Author was not found and his creation failed.")

        book = Title(title_id, author, title, isbn, page_count, price, description)
        exists = self._title_dao.exists(book, True)
        if exists:
            raise ObjectAlreadyExistsException("Title from this author already exists.")

        return self._title_dao.update(book)

    def remove_title(self, title_id: int) -> bool:

        title = self._title_dao.get_by_id(title_id)
        if not title:
            raise InvalidParameterException("Title was not found.")

        #try remove copies
        self._copy_dao.delete_copies_by_title_id(title_id)

        return self._title_dao.delete(title_id)

    def get_titles(self, offset: int, limit: int) -> list:
        return self._title_dao.get_titles(offset, limit)

    def get_by_id(self, title_id: int) -> Title | None:
        return self._title_dao.get_by_id(title_id)

    def bulk_csv_add(self, csv_reader, has_header: bool) -> tuple[int,int]:
        line = 0
        added = 0
        skipped = 0
        try:
            self._db.begin_transaction()
            if has_header:
                next(csv_reader, None)

            line = 1
            for row in csv_reader:
                title = row[0].strip()
                author_name = row[1].strip()
                isbn = row[2].strip()
                page_count = row[3].strip()
                price = row[4].strip()
                description = row[5].strip()

                page_count = int(page_count) if page_count else None
                price = float(price)

                try:
                    self.add_new_title(author_name, title, isbn, page_count, price, description)
                    added += 1
                except ObjectAlreadyExistsException:
                    skipped += 1

                line += 1

            self._db.commit()
            return added, skipped
        except IndexError:
            raise Exception(f"Not enough columns in csv (line {line})")
        except Exception as e:
            raise Exception(f"(line {line}): {e}")
        finally:
            self._db.rollback()