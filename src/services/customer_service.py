from src.daos.customer_dao import CustomerDAO
from src.models.entities import Customer
from src.utils import InvalidParameterException

from datetime import datetime
import string
import random


class CustomerService:

    def __init__(self, db_manager):
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


    def register_customer(self, first_name: str, last_name: str, email: str) -> Customer | None:
        """
        Registers a new customer.
        :param first_name: customers first name
        :param last_name: customers last name
        :param email: customer email
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

        customer = Customer(0, new_code, first_name, last_name, email, True, datetime.now())

        if self._dao.create(customer):
            return customer
        return None

    def update_customer(self, _id: int, first_name: str, last_name: str, email: str) -> bool:

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

    def get_by_id(self, _id: int) -> Customer:
        return self._dao.get_by_id(_id)