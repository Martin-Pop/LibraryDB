from src.daos.customer_dao import CustomerDAO
from src.models.entities import Customer
from src.utils import InvalidParameterException

from datetime import datetime
import string
import random


class CustomerService:

    def __init__(self, db_manager):
        self._db = db_manager
        self._dao = CustomerDAO(db_manager)

    def _generate_customer_code(self):
        """
        Generates a random customer code.
        :return: new customer code
        """
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(8))
        return random_part

    def _validate(self, first_name: str, last_name: str, email: str):
        """
        Validates customers parameters
        :param first_name: first name - must be at least 2 characters long
        :param last_name: last name - must be at least 2 characters long
        :param email: email address - must contain @ and .
        :raises InvalidParameterException: invalid parameters
        """
        if not first_name or len(first_name) < 2:
            raise InvalidParameterException("Name must be at least 2 characters long")

        if not last_name or len(last_name) < 2:
            raise InvalidParameterException("Last name must be at least 2 characters long")

        if not email or "@" not in email or "." not in email:
            raise InvalidParameterException("Invalid email address.")


    def register_customer(self, first_name: str, last_name: str, email: str, is_active: bool) -> Customer | None:
        """
        Registers a new customer.
        :param first_name: customers first name
        :param last_name: customers last name
        :param email: customer email
        :param is_active: if customer account is activated
        :return: customer object
        """

        first_name = first_name.strip() if first_name else ""
        last_name = last_name.strip() if last_name else ""
        email = email.strip() if email else ""

        self._validate(first_name, last_name, email)

        while True:
            new_code = self._generate_customer_code()

            if not self._dao.does_code_exist(new_code):
                break

        customer = Customer(0, new_code, first_name, last_name, email, is_active, datetime.now())

        if self._dao.create(customer):
            return customer
        return None

    def update_customer(self, _id: int, first_name: str, last_name: str, email: str, is_active: bool) -> bool:

        customer = self._dao.get_by_id(_id)
        if not customer:
            return False

        first_name = first_name.strip() if first_name else ""
        last_name = last_name.strip() if last_name else ""
        email = email.strip() if email else ""

        self._validate(first_name, last_name, email)

        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.is_active = is_active

        return self._dao.update(customer)

    def remove_customer(self, customer_id: int) -> bool:
        return self._dao.delete(customer_id)

    def get_customers(self, offset, limit):
        """
        Gets a list of customers
        :param offset: Number of rows to skip.
        :param limit: Number of rows to return.
        :return: list of customers
        """
        return self._dao.get_customers(offset, limit)

    def get_by_id(self, _id: int) -> Customer | None:
        return self._dao.get_by_id(_id)

    def get_by_code(self, code: str) -> Customer | None:
        return self._dao.get_by_code(code)

    def bulk_csv_add(self, csv_reader, has_header: bool) -> int:
        line = 0
        try:
            self._db.begin_transaction()
            if has_header:
                next(csv_reader, None)

            line = 1
            for row in csv_reader:
                first_name = row[0].strip()
                last_name = row[1].strip()
                email = row[2].strip()
                is_active = True if row[3].strip().lower() in ('true', '1', 'yes', 't') else False

                self.register_customer(first_name, last_name, email, is_active)
                line += 1

            self._db.commit()
            return line -1
        except IndexError:
            raise Exception(f"Not enough columns in csv (line {line})")
        except Exception as e:
            raise Exception(f"(line {line}): {e}")
        finally:
            self._db.rollback()