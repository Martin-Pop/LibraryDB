from datetime import datetime
from src.daos.loan_dao import LoanDAO
from src.daos.customer_dao import CustomerDAO
from src.daos.copy_dao import CopyDAO
from src.models.entities import Loan
from src.utils import InvalidParameterException


class LoanService:

    def __init__(self, db_manager):
        self._loan_dao = LoanDAO(db_manager)
        self._customer_dao = CustomerDAO(db_manager)
        self._copy_dao = CopyDAO(db_manager)

    def create_loan(self, customer_id: int, copy_id: int, loan_date: datetime = None) -> Loan | None:

        customer = self._customer_dao.get_by_id(customer_id)
        if not customer:
            raise InvalidParameterException(f"Customer with id {customer_id} not found")

        copy = self._copy_dao.get_by_id(copy_id)
        if not copy:
            raise InvalidParameterException(f"Copy with id {copy_id} not found")

        if loan_date is None:
            loan_date = datetime.now()

        loan = Loan(0, customer, copy, loan_date, None)

        if self._loan_dao.create(loan):
            return loan
        return None

    def update_loan(self, loan_id: int, customer_id: int, copy_id: int, loan_date: datetime,
                    return_date: datetime | None) -> bool:

        customer = self._customer_dao.get_by_id(customer_id)
        if not customer:
            raise InvalidParameterException("Customer not found")

        copy = self._copy_dao.get_by_id(copy_id)
        if not copy:
            raise InvalidParameterException("Copy not found")

        loan = Loan(loan_id, customer, copy, loan_date, return_date)
        return self._loan_dao.update(loan)

    def close_loan(self, loan_id: int) -> bool:
        pass

    def remove_loan(self, loan_id: int) -> bool:
        return self._loan_dao.delete(loan_id)

    def get_loans(self, offset: int, limit: int) -> list:
        return self._loan_dao.get_loans(offset, limit)