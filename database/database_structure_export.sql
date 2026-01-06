USE [my_library]
GO
/****** Object:  Table [dbo].[customers]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[customers](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[code] [varchar](20) NOT NULL,
	[first_name] [varchar](100) NOT NULL,
	[last_name] [varchar](100) NOT NULL,
	[email] [varchar](100) NOT NULL,
	[is_active] [bit] NULL,
	[registration_date] [datetime] NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [unc] UNIQUE NONCLUSTERED
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[authors]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[authors](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](100) NOT NULL,
	[nationality] [varchar](50) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[titles]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[titles](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[author_id] [int] NULL,
	[title] [varchar](200) NOT NULL,
	[isbn] [varchar](20) NULL,
	[page_count] [int] NULL,
	[price] [decimal](10, 2) NOT NULL,
	[description] [varchar](200) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[copies]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[copies](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[title_id] [int] NULL,
	[code] [varchar](20) NOT NULL,
	[location] [varchar](50) NULL,
	[status] [varchar](20) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[loans]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[loans](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[customer_id] [int] NULL,
	[copy_id] [int] NULL,
	[loan_date] [datetime] NULL,
	[return_date] [datetime] NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[v_loans]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create view [dbo].[v_loans] as
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
GO
/****** Object:  View [dbo].[v_stats]    Script Date: 06.01.2026 17:56:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create   view [dbo].[v_stats] as
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

GO
ALTER TABLE [dbo].[customers] ADD  DEFAULT ((1)) FOR [is_active]
GO
ALTER TABLE [dbo].[customers] ADD  DEFAULT (getdate()) FOR [registration_date]
GO
ALTER TABLE [dbo].[loans] ADD  DEFAULT (getdate()) FOR [loan_date]
GO
ALTER TABLE [dbo].[copies]  WITH CHECK ADD FOREIGN KEY([title_id])
REFERENCES [dbo].[titles] ([id])
GO
ALTER TABLE [dbo].[loans]  WITH CHECK ADD FOREIGN KEY([copy_id])
REFERENCES [dbo].[copies] ([id])
GO
ALTER TABLE [dbo].[loans]  WITH CHECK ADD FOREIGN KEY([customer_id])
REFERENCES [dbo].[customers] ([id])
GO
ALTER TABLE [dbo].[titles]  WITH CHECK ADD FOREIGN KEY([author_id])
REFERENCES [dbo].[authors] ([id])
GO
ALTER TABLE [dbo].[copies]  WITH CHECK ADD CHECK  (([status]='discarded' OR [status]='lost' OR [status]='on_loan' OR [status]='available'))
GO
