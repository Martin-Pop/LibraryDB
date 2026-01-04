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

-- loan view
go
create view v_loans as
select 
    l.id as l_id, l.loan_date, l.return_date,
    c.id as c_id, c.code as c_code, c.first_name, c.last_name, c.email, c.is_active, c.registration_date,
    cp.id as cp_id, cp.code as cp_code, cp.location, cp.status,
    t.id as t_id, t.title, t.isbn, t.page_count, t.price, t.description,
    a.id as a_id, a.name, a.nationality
from loans l
join customers c on l.customer_id = c.id
join copies cp on l.copy_id = cp.id
join titles t on cp.title_id = t.id
join authors a on t.author_id = a.id;
go


-- stats views
go
create or alter view v_stats as
select
    -- author stats
    (select count(*) from authors) as total_authors,

    -- title stats
    (select count(*) from titles) as total_titles,
    (select max(price) from titles) as max_book_price,
    (select cast(avg(price) as decimal(10,2)) from titles) as avg_book_price,
    (select sum(t.page_count) from titles t join copies c on c.title_id = t.id) as total_pages_inventory,

    -- copy stast
    (select count(*) from copies) as total_physical_copies,
    (select count(*) from copies where status = 'available') as copies_available,
    (select count(*) from copies where status = 'lost' or status = 'discarded') as copies_lost,
    
    -- finance
    (select sum(t.price) from titles t join copies c on c.title_id = t.id) as total_library_value,

    -- customer stats
    (select count(*) from customers) as total_customers,
    (select count(*) from customers where is_active = 1) as active_customers,

    -- loans stast
    (select count(*) from loans) as all_time_loans,
    (select count(*) from loans where return_date is null) as currently_borrowed,
    (select max(datediff(day, loan_date, getdate())) from loans where return_date is null) as max_days_held;
go