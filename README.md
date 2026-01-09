
# Library System

**Author:** Martin Pop  
**Date:** Dec 25 2025 - now
**Project Type:** School Database project - **D1**
  
## Overview  
  
The objective of this project is to create a system for a small to medium-sized library.  
The system allows librarians to manage the catalog of books, authors, physical copies, customers, and loan transactions.  
  
The system implements the following use cases:  
  
- **Catalog Management**:  
  - Add, edit, and delete authors.  
  - Add, edit, and delete book titles (linked to authors, supports bulk add from csv - import).  
  - Manage physical copies of books (inventory control).  
- **Customer Management**:  
  - Register new library members (supports bulk register from csv - import).  
  - Update customer details and status (active/inactive).  
- **Loan Operations**:  
  - Issue loans to registered customers (checking copy availability).  
  - Return books (updating copy status and return date).  
- **Statistics**:  
  - View a dashboard displaying total assets, active loans, available inventory, and financial value.  
  
## Dependencies  
  
### Software Requirements  
- Python: Version 3.10 or higher.  
- Database Engine: Microsoft SQL Server (2019 or newer recommended).  
- Driver: ODBC Driver 17 for SQL Server.  
  
### Third-Party Python Libraries  
- Flask: Core web framework.  
- pyodbc: Interface for connecting to Microsoft SQL Server.
- pyinstaller: Compiles project into standalone executable.
  
## Database Model  
The backend utilizes a relational database model.  
**Tables:**  
	- **authors**: Stores author details `(id, name, nationality)`.  
	- **titles**: Stores book metadata `(id, title, isbn, price, page_count, description, author_id)`.  
	- **copies**: Physical inventory tracking `(id, code, status, location, title_id)`.  
	- **customers**: User registry `(id, code, first_name, last_name, email, is_active, registration_date)`.  
	- **loans**: Transaction history `(id, customer_id, copy_id, loan_date, return_date)`.  

## 3. How it Works (Internal Logic Flow)

The application relies on a strictly layered architecture to separate concerns. This ensures that the code handling HTTP requests is distinct from the code handling business logic and database access. The data flow follows a hierarchical path: **Controller (Blueprint) → Service → DAO → Database**.

### 1. The Controller Layer (Flask Blueprints)

The entry point for any user action is the **Controller**. The application uses Flask **Blueprints** to organize routes into logical modules (e.g., `stats_bp`, `loans_bp`).

-   **Role:** Handles the HTTP Request/Response cycle.
-   **Responsibility:**
    -   Receives the URL request (e.g., `GET /stats`).
    -   Parses input data (forms, query parameters).
    -   **Calls the Service Layer** to perform the required action.
    -   Receives the result from the Service and renders the appropriate HTML template (View) to the user.    

### 2. The Service Layer

The **Service** acts as the "brain" of the application. It contains logic and rules.
-   **Role:** Processes data.
-   **Responsibility:**
    -   Validates complex logic (e.g., "Is this book currently available?", "Is the customer active?").
    -   Orchestrates data retrieval.
    -   **Calls the DAO Layer** 
    -   Returns clean, processed data back to the Controller.
        
### 3. The DAO Layer (Data Access Object)

The **DAO** is the only layer that interacts directly with the database. It isolates the SQL code from the rest of the application.

-   **Role:** Database communication.
-   **Responsibility:**
    -   Manages the database connection (obtaining a cursor).
    -   Executes SQL queries (`SELECT`, `INSERT`, `UPDATE`).
    -   Maps raw database rows (tuples) into Python dictionaries or objects.
    -   Returns data to the Service.

## Installation steps
1. Download Project.
   - Download latest release.
   - If you want to compile it yourself:
     - Download / clone this repo
     - Install dependencies `pip install -r requirements.txt`
     - Compile with: `pyinstaller --noconfirm --onedir --console --name "LibraryDB" --paths "." --add-data "public;public" src/main/app.py`
     - Copy config folder and paste in next to your executable
2. Create database on your Microsoft SQL Server. Read: `database/DATABASE_INSTALLATION.md`
3. Configure configuration files for webserver and database connection. Read: `config/CONFIGURATION.md`
4. Open library dashboard in your browser.

## License
MIT License