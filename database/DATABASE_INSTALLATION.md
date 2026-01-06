
# Database Installation
Step by step guide on how to set up database.

## 1. Log into Microsoft SQL Server Management studio
Log in to  your Microsoft SQL Server Management studio with login as server admin.
Example: 
- SERVER TYPE: Database engine  
- SERVER NAME: PC1234
- AUTHENTICATION: SQL Server authentication  
- LOGIN: sa  
- PASSWORD: password

## 2. Create new Database and Login
Create new database using gui or create new query and paste in commands.
- **Paste in method:**
	- Create a new query and paste in the commands from `database/databasae_setup.sql`
	- If you wish to change database name change every line that has `[my_library]` to `[your_own_name]`
	- Select everything and click execute
**GUI method**
	1. Right Click Databases and select 'New Database'
	2. Fill in 'Database name' and click ok
	3. Right Click on Logins (Security/Logins) and select 'New Login'
	4. Fill in 'Login name', select 'SQL Server authentication', fill in passwords and disable enforce password policy
	5. Click on 'User Mapping', select your database name and add 'db_datareader' and 'db_datawriter', click OK

## 3. Create database structure
Create database structure by pasting in commands.
1. Create new query and paste in commands from `database/database_structure_export.sql` 
2. If you renamed your database (step 2) change every line that has `[my_library]` to `[your_own_name]`
3. Select everything and click execute.

**NOTE:** if you get an error try using the `database/library.sql` commands and create tables and view one by one - do not forget using the `USE [your_db_name]` command
