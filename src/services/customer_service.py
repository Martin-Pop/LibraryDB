from src.daos.customer_dao import CustomerDAO
from src.models.entities import Customer

from datetime import datetime
import string
import random


class CustomerService:

    def __init__(self, db_manager):
        self._dao = CustomerDAO(db_manager)

    def _generate_customer_code(self):
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(8))
        return f"CUSTOMER-{random_part}"

    def register_customer(self, first_name, last_name, email):
        """
        Registers a new customer.
        :param first_name: customers first name
        :param last_name: customers last name
        :param email: customer email
        :return: customer object
        """

        if not isinstance(first_name, str):
            raise TypeError(f"First name must be str got: {type(first_name).__name__}")

        if not isinstance(last_name, str):
            raise TypeError(f"Last name must be str got: {type(last_name).__name__}")

        if not isinstance(email, str):
            raise TypeError(f"Email must be str got: {type(email).__name__}")

        first_name = first_name.strip() if first_name else ""
        last_name = last_name.strip() if last_name else ""
        email = email.strip() if email else ""

        if not first_name or len(first_name) < 2:
            raise ValueError("Name must be at least 2 characters long")

        if not last_name or len(last_name) < 2:
            raise ValueError("Last name must be at least 2 characters long")

        if not email or "@" not in email or "." not in email:
            raise ValueError("Invalid email address.")

        while True:
            new_code = self._generate_customer_code()

            if not self._dao.does_code_exist(new_code):
                break

        customer = Customer(
            id=0,
            code=new_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            registered_on=datetime.now()
        )

        self._dao.create(customer)
        return customer