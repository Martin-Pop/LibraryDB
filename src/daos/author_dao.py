from src.models.entities import Author

class AuthorDAO:

    def __init__(self, db_manager):
        self._db = db_manager

    def get_by_id(self, author_id: int) -> Author:
        sql = "select first_name, last_name, nationality from authors where id = ?"
        return self._db.fetchone(sql, (author_id,))

    def get_authors(self, offset: int, limit: int) -> list:
        sql = """
            select id, first_name, last_name, nationality
            from authors 
            order by id 
            offset ? rows 
            fetch next ? rows only
        """

        rows = self._db.fetch_all(sql, (offset, limit))

        authors = []
        for row in rows:
            author = Author(*row)
            authors.append(author)

        return authors


    def create(self, author: Author) -> bool:
        sql = """
            insert into authors (first_name, last_name, nationality)
            output inserted.id
            values (?, ?, ?);
        """

        params = (
            author.first_name,
            author.last_name,
            author.nationality,
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
            set first_name = ?, 
                last_name = ?, 
                nationality = ?
            where id = ?
        """
        params = (
            author.first_name,
            author.last_name,
            author.nationality,
            author.id,
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, author_id: int) -> bool:
        sql = "delete from authors where id = ?"

        rows_affected = self._db.execute(sql, (author_id,))
        return rows_affected > 0