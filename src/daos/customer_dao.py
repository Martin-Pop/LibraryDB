from src.models.entities import Customer

class CustomerDAO:
    def __init__(self, db_manager):
        self._db = db_manager

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