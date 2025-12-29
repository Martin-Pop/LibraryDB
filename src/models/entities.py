from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class CopyStatus(Enum):
    AVAILABLE = 'available',
    ON_LOAN = 'on_loan',
    LOST = 'lost',
    DISCARDED = 'discarded'

@dataclass
class Author:
    id: int
    first_name: str
    last_name: str
    nationality: str | None

@dataclass
class Title:
    id: int
    author: Author
    title: str
    isbn: str | None
    page_count: int | None
    price: float
    description: str | None

@dataclass
class Copy:
    id: int
    title: Title
    code: str
    location: str
    status: CopyStatus

@dataclass
class Customer:
    id: int
    code: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    registered_on: datetime

@dataclass
class Loan:
    id: int
    customer: Customer
    copy: Copy
    loan_date: datetime
    return_date: datetime | None