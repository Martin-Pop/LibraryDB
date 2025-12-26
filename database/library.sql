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

-- titles
create table titles (
    id int primary key identity(1,1),
    title varchar(200) not null,
    isbn varchar(20),
    page_count int,
    price decimal(10,2) not null
);

-- authors
create table authors (
    id int primary key identity(1,1),
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    nationality varchar(50)
);

-- title_authors
create table title_authors (
    title_id int references titles(id),
    author_id int references authors(id),
    primary key (title_id, author_id)
);

-- copies
create table copies (
    id int primary key identity(1,1),
    title_id int references titles(id),
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