from datetime import datetime
from src.daos.loan_dao import LoanDAO
from src.daos.customer_dao import CustomerDAO
from src.daos.copy_dao import CopyDAO
from src.models.entities import Loan, CopyStatus
from src.utils import InvalidParameterException


class LoanService:

    def __init__(self, db_manager):
        self._db = db_manager #for transactions
        self._loan_dao = LoanDAO(db_manager)
        self._customer_dao = CustomerDAO(db_manager)
        self._copy_dao = CopyDAO(db_manager)

    def create_loan(self, customer_code: str, copy_code: str, loan_date: datetime = None) -> Loan | None:

        customer = self._customer_dao.get_by_code(customer_code)
        if not customer:
            raise InvalidParameterException(f"Customer with code: {customer_code} not found")

        copy = self._copy_dao.get_by_code(copy_code)
        if not copy:
            raise InvalidParameterException(f"Copy with id {copy_code} not found")

        if copy.status != CopyStatus.AVAILABLE:
            raise InvalidParameterException(f"Copy is currently {copy.status.value}, cannot be loaned.")

        if loan_date is None:
            loan_date = datetime.now()

        # transaction
        try:
            self._db.begin_transaction()

            loan = Loan(0, customer, copy, loan_date, None)
            success_loan = self._loan_dao.create(loan)

            if not success_loan:
                raise Exception("Failed to create loan record")

            copy.status = CopyStatus.ON_LOAN
            success_copy = self._copy_dao.update(copy)

            if not success_copy:
                raise Exception("Failed to update copy status")

            self._db.commit()
            return loan

        except Exception as e:
            self._db.rollback()
            raise e

    def close_loan(self, customer_code: str, copy_code: str, status: CopyStatus) -> bool:

        loan = self._loan_dao.get_loan_by_codes(customer_code, copy_code)

        if not loan:
            raise InvalidParameterException(f"Loan {customer_code} x {copy_code} was not found")

        if loan.return_date is not None:
            raise InvalidParameterException("This loan is already closed.")

        try:
            self._db.begin_transaction()

            loan.return_date = datetime.now()
            if not self._loan_dao.update(loan):
                raise Exception("Failed to update loan return date")

            copy = loan.copy
            copy.status = status

            if not self._copy_dao.update(copy):
                raise Exception(f"Failed to update copy status to {status.value}")

            self._db.commit()
            return True

        except Exception as e:
            self._db.rollback()
            raise e

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

    def remove_loan(self, loan_id: int) -> bool:
        return self._loan_dao.delete(loan_id)

    def get_loans(self, offset: int, limit: int) -> list:
        return self._loan_dao.get_loans(offset, limit)