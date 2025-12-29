from src.models.entities import Title, Copy, Author, CopyStatus


class CopyDAO:
    def __init__(self, db_manager):
        self._db = db_manager

    def get_by_id(self, copy_id: int) -> Copy | None:
        sql = """
            select 
                c.id, c.code, c.location, c.status,
                t.id, t.title, t.isbn, t.page_count, t.price, t.description,
                a.id, a.first_name, a.last_name, a.nationality
            from copies c
            join titles t on c.title_id = t.id
            join authors a on t.author_id = a.id
            where c.id = ?
        """

        row = self._db.fetch_one(sql, (copy_id,))

        if not row:
            return None

        author = Author(*row[10:])
        title = Title(row[4], author, *row[5:10])

        return Copy(row[0], title, row[1], row[2], CopyStatus(row[3]))

    def get_copies(self, offset: int, limit: int) -> list:
        sql = """
                select 
                    c.id, c.code, c.location, c.status,
                    t.id, t.title, t.isbn, t.page_count, t.price, t.description,
                    a.id, a.first_name, a.last_name, a.nationality
                from copies c
                join titles t on c.title_id = t.id
                join authors a on t.author_id = a.id
                order by c.id
                offset ? rows fetch next ? rows only
            """

        # copy - 0-3, title - 4-9, author - 10-13

        rows = self._db.fetch_all(sql, (offset, limit))

        copies = []
        authors_map = {}
        titles_map = {}

        for row in rows:

            author_id = row[10]
            if author_id in authors_map:
                author = authors_map[author_id]
            else:
                author = Author(*row[10:])
                authors_map[author_id] = author

            title_id = row[4]
            if title_id in titles_map:
                title = titles_map[title_id]
            else:
                title = Title(title_id, author, *row[5:10])
                titles_map[title_id] = title

            copies.append(Copy(row[0], title, row[1], row[2], CopyStatus(row[3])))
        return copies


    def create(self, copy: Copy) -> bool:
        sql = """
            insert into copies (title_id, code, location, status)
            output inserted.id
            values (?, ?, ?, ?);
        """

        params = (
            copy.title.id,
            copy.code,
            copy.location,
            copy.status.value,
        )

        out = self._db.execute_get_output(sql, params)
        if out:
            _id = out[0]
            copy.id = _id
            return True
        return False

    def update(self, copy: Copy) -> bool:
        sql = """
            update copies
            set title_id = ?,
            code = ?,
            location = ?,
            status = ?
            where id = ?
        """

        params = (
            copy.title.id,
            copy.code,
            copy.location,
            copy.status.value,
            copy.id,
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, copy_id: int) -> bool:
        sql = "delete from copies where id = ?"
        rows_affected = self._db.execute(sql, (copy_id,))
        return rows_affected > 0