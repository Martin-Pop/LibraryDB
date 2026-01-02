from src.models.entities import Loan, Customer, Copy, Title, Author, CopyStatus


class LoanDAO:

    select = """
            select 
                l.id, l.loan_date, l.return_date,
                c.id, c.code, c.first_name, c.last_name, c.email, c.is_active, c.registration_date,
                cp.id, cp.code, cp.location, cp.status,
                t.id, t.title, t.isbn, t.page_count, t.price, t.description,
                a.id, a.name, a.nationality
            from loans l
            join customers c on l.customer_id = c.id
            join copies cp on l.copy_id = cp.id
            join titles t on cp.title_id = t.id
            join authors a on t.author_id = a.id
        """

    # Loan (0-2), Customer (3-9), Copy (10-13), Title (14-19), Author (20-22)

    def __init__(self, db_manager):
        self._db = db_manager

    def get_loan_by_codes(self, customer_code: str, copy_code: str):
        sql = self.select + "where c.code = ? and cp.code = ?"
        row = self._db.fetch_one(sql, (customer_code, copy_code))

        if not row:
            return None

        author = Author(*row[20:])
        title = Title(row[14], author, *row[15:20])
        copy = Copy(row[10], title, row[11], row[12], CopyStatus(row[13]))
        customer = Customer(*row[3:10])

        return Loan(row[0], customer, copy, row[1], row[2])


    def get_by_id(self, loan_id: int) -> Loan | None:
        sql = self.select + "where l.id = ?"
        row = self._db.fetch_one(sql, (loan_id,))

        if not row:
            return None

        author = Author(*row[20:])
        title = Title(row[14], author, *row[15:20])
        copy = Copy(row[10], title, row[11], row[12], CopyStatus(row[13]))
        customer = Customer(*row[3:10])

        return Loan(row[0], customer, copy, row[1], row[2])


    def get_loans(self, offset: int, limit: int) -> list:
        sql = self.select + "order by l.id offset ? rows fetch next ? rows only"

        # Loan (0-2), Customer (3-9), Copy (10-13), Title (14-19), Author (20-22)

        rows = self._db.fetch_all(sql, (offset, limit))

        loans = []

        authors_map = {}
        titles_map = {}
        copies_map = {}
        customers_map = {}

        for row in rows:
            # author
            author_id = row[20]
            if author_id in authors_map:
                author = authors_map[author_id]
            else:
                author = Author(*row[20:])
                authors_map[author_id] = author

            # title
            title_id = row[14]
            if title_id in titles_map:
                title = titles_map[title_id]
            else:
                title = Title(title_id, author, *row[15:20])
                titles_map[title_id] = title

            # copy
            copy_id = row[10]
            if copy_id in copies_map:
                copy = copies_map[copy_id]
            else:
                copy = Copy(copy_id, title, row[11], row[12], CopyStatus(row[13]))
                copies_map[copy_id] = copy

            # customer
            customer_id = row[3]
            if customer_id in customers_map:
                customer = customers_map[customer_id]
            else:
                customer = Customer(*row[3:10])
                customers_map[customer_id] = customer

            # loan
            loans.append(Loan(row[0], customer, copy, row[1], row[2]))

        return loans

    def create(self, loan: Loan) -> bool:
        sql = """
            insert into loans (customer_id, copy_id, loan_date, return_date)
            output inserted.id
            values (?, ?, ?, ?);
        """

        params = (
            loan.customer.id,
            loan.copy.id,
            loan.loan_date,
            loan.return_date
        )

        out = self._db.execute_get_output(sql, params)
        if out:
            _id = out[0]
            loan.id = _id
            return True
        return False

    def update(self, loan: Loan) -> bool:
        sql = """
            update loans
            set customer_id = ?,
            copy_id = ?,
            loan_date = ?,
            return_date = ?
            where id = ?
        """

        params = (
            loan.customer.id,
            loan.copy.id,
            loan.loan_date,
            loan.return_date,
            loan.id
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, loan_id: int) -> bool:
        sql = "delete from loans where id = ?"
        rows_affected = self._db.execute(sql, (loan_id,))
        return rows_affected > 0