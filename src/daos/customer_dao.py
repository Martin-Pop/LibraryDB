from src.models.entities import Customer

class CustomerDAO:
    def __init__(self, db_manager):
        self._db = db_manager

    def get_customers(self, offset: int, limit: int) -> list:
        """
        Retrieves list of customers.
        :param offset: Number of rows to skip.
        :param limit: Number of rows to return.
        """

        # order by required?
        sql = """
            select id, code, first_name, last_name, email, is_active, registration_date 
            from customers 
            order by id 
            offset ? rows 
            fetch next ? rows only
        """

        rows = self._db.fetch_all(sql, (offset, limit))

        customers = []
        for row in rows:
            customer = Customer(*row)
            customers.append(customer)

        return customers

    def get_by_id(self, customer_id: int) -> Customer | None:
        sql = "select id, code, first_name, last_name, email, is_active, registration_date from customers where id = ?"
        row = self._db.fetch_one(sql, (customer_id,))
        if row:
            return Customer(*row)
        return None

    def get_by_code(self, customer_code: str) -> Customer | None:
        sql = "select id, code, first_name, last_name, email, is_active, registration_date from customers where code = ?"
        row = self._db.fetch_one(sql, (customer_code,))
        if row:
            return Customer(*row)
        return None

    def create(self, customer: Customer) -> bool:
        sql = """
            insert into customers (code, first_name, last_name, email, is_active, registration_date)
            output inserted.id
            values (?, ?, ?, ?, ?, ?);
        """
        params = (
            customer.code,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.is_active,
            customer.registered_on
        )

        out = self._db.execute_get_output(sql, params)
        if out:
            _id = out[0]
            customer.id = _id
            return True
        return False

    def update(self, customer: Customer) -> bool:
        sql = """
            update customers 
            set code = ?, 
                first_name = ?, 
                last_name = ?, 
                email = ?, 
                is_active = ?, 
                registration_date = ?
            where id = ?
        """
        params = (
            customer.code,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.is_active,
            customer.registered_on,
            customer.id
        )

        rows_affected = self._db.execute(sql, params)
        return rows_affected > 0

    def delete(self, customer_id: int) -> bool:
        sql = "delete from customers where id = ?"

        rows_affected = self._db.execute(sql, (customer_id,))
        return rows_affected > 0

    def set_is_active(self, customer_id: int, is_active_value: bool) -> bool:
        sql = "update customers set is_active = ? where id = ?"

        rows_affected = self._db.execute(sql, (is_active_value, customer_id))
        return rows_affected > 0

    def does_code_exist(self, code: str) -> bool:
        sql = "select 1 from customers where code = ?"
        result = self._db.fetch_one(sql, (code,))
        return result is not None