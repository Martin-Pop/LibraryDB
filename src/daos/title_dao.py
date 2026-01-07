from src.models.entities import Title, Author


class TitleDAO:
    def __init__(self, db):
        self._db = db

    def get_by_id(self, title_id: int) -> Title | None:
        sql = """
            select authors.id, authors.name, authors.nationality,
            titles.title, titles.isbn, titles.page_count, titles.price, titles.description
            from titles join authors on titles.author_id = authors.id
            where titles.id = ?
        """
        row = self._db.fetch_one(sql, (title_id,))
        if not row:
            return None

        author = Author(*row[:3])
        return Title(title_id, author,*row[3:])

    def get_by_title_author_name(self, title: str, author_name: str) -> Title | None:
        sql = """
            select authors.id, authors.name, authors.nationality,
            titles.id, titles.isbn, titles.page_count, titles.price, titles.description
            from titles join authors on titles.author_id = authors.id
            where titles.title = ? and authors.name = ?
        """
        row = self._db.fetch_one(sql, (title, author_name))
        if not row:
            return None

        author = Author(*row[:3])
        return Title(row[3], author, title, *row[4:])

    def get_titles(self, offset: int, limit: int) -> list:

        sql = """
            select titles.id, authors.id, authors.name, authors.nationality, 
            titles.title, titles.isbn, titles.page_count, titles.price, titles.description
            from titles join authors on titles.author_id = authors.id
            order by titles.id 
            offset ? rows 
            fetch next ? rows only
        """

        rows = self._db.fetch_all(sql, (offset, limit))

        titles = []
        for row in rows:
            author = Author(row[1], row[2], row[3])
            title = Title(row[0], author, row[4], row[5], row[6], row[7], row[8])
            titles.append(title)

        return titles

    def create(self, title: Title) -> bool:
        sql = """
            insert into titles (author_id, title, isbn, description, page_count, price)
            output inserted.id
            values (?, ?, ?, ?, ?, ?);
        """

        params = (
            title.author.id,
            title.title,
            title.isbn,
            title.description,
            title.page_count,
            title.price
        )

        out = self._db.execute_get_output(sql, params)
        if out:
            _id = out[0]
            title.id = _id
            return True
        return False

    def update(self, title: Title) -> bool:
        sql = """
            update titles
            set author_id = ?,
            title = ?,
            isbn = ?,
            description = ?,
            page_count = ?,
            price = ?
            where id = ?
        """
        params = (
            title.author.id,
            title.title,
            title.isbn,
            title.description,
            title.page_count,
            title.price,
            title.id
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, title_id: int) -> bool:
        sql = "delete from titles where id = ?"
        rows_affected = self._db.execute(sql, (title_id,))
        return rows_affected > 0

    def exists(self, title: Title, is_update=False) -> bool:
        if is_update:
            sql = "select 1 from titles where title = ? and author_id = ? and id != ?"
            row = self._db.fetch_one(sql, (title.title, title.author.id, title.id))
        else:
            sql = "select 1 from titles where title = ? and author_id = ?"
            row = self._db.fetch_one(sql, (title.title, title.author.id))
        if not row:
            return False
        return True