from src.models.entities import Author
from src.utils import InvalidParameterException


class AuthorDAO:

    def __init__(self, db_manager):
        self._db = db_manager

    def get_by_id(self, author_id: int) -> Author | None:
        sql = "select name, nationality from authors where id = ?"
        row = self._db.fetch_one(sql, (author_id,))
        if not row:
            return None

        return Author(author_id, *row)

    def get_by_name(self, name: str) -> Author | None:
        sql = "select id, nationality from authors where name = ?"
        row = self._db.fetch_one(sql, (name,))
        if not row:
            return None

        return Author(row[0], name, row[1])

    def get_authors(self, offset: int, limit: int | None) -> list:
        sql = """
            select id, name, nationality
            from authors 
            order by id 
            offset ? rows
        """

        if limit is not None:
            sql += " fetch next ? rows only"
            rows = self._db.fetch_all(sql, (offset, limit))
        else:
            rows = self._db.fetch_all(sql, (offset,))

        authors = []
        for row in rows:
            author = Author(*row)
            authors.append(author)

        return authors


    def create(self, author: Author) -> bool:
        sql = """
            insert into authors (name, nationality)
            output inserted.id
            values (?, ?);
        """

        params = (
            author.name,
            author.nationality
        )

        out = self._db.execute_get_output(sql, params)
        if out:
            _id = out[0]
            author.id = _id
            return True
        return False

    def update(self, author: Author) -> bool:
        sql = """
            update authors
            set name = ?, 
                nationality = ?
            where id = ?
        """
        params = (
            author.name,
            author.nationality,
            author.id
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, author_id: int) -> bool:
        sql = "delete from authors where id = ?"

        rows_affected = self._db.execute(sql, (author_id,))
        return rows_affected > 0