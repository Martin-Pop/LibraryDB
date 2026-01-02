create database my_library;
use my_library;


-- customer
create table customers (
    id int primary key identity(1,1),
	code varchar(20) unique not null,
	first_name varchar(100) not null,
    last_name varchar(100) not null,
    email varchar(100) not null,
    is_active bit default 1,
    registration_date datetime default getdate()
);

-- authors
create table authors (
    id int primary key identity(1,1),
    name varchar(100) not null unique,
    nationality varchar(50)
);

-- titles
create table titles (
    id int primary key identity(1,1),
	author_id int foreign key references authors(id),
    title varchar(200) not null,
    isbn varchar(20),
    page_count int,
    price decimal(10,2) not null,
    description varchar(200)
);

-- copies
create table copies (
    id int primary key identity(1,1),
    title_id int references titles(id),
	code varchar(20) unique not null,
    location varchar(50),
    status varchar(20) check (status in ('available', 'on_loan', 'lost', 'discarded')) 
);

-- loans
create table loans (
    id int primary key identity(1,1),
    customer_id int references customers(id),
    copy_id int references copies(id),
    loan_date datetime default getdate(), 
    return_date datetime null 
);