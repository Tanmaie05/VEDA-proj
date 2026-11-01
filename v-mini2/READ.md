# Veda Technology – Business & Service Management System

## Objective
To develop a web-based Business and Service Management System for Veda Technology that simplifies the management of services, programs, customer inquiries, and service requests through a centralized dashboard.

## Description
The Veda Technology Business & Service Management System is a Flask-based web application designed to organize business operations through a simple and user-friendly interface. It provides an authenticated dashboard where administrators can manage service details, training programs, customer inquiries, and service requests.

The application supports adding, updating, and deleting records, changing statuses, searching records, and validating user inputs. Data is stored using JSON-based persistence, allowing records to remain available between application runs.

## Technologies Used
- **Python** – Application logic
- **Flask** – Web framework and routing
- **HTML5** – Page structure
- **CSS3** – Styling and responsive layout
- **JavaScript** – Search and interactive features
- **Jinja2** – Dynamic HTML rendering
- **JSON** – Data storage
- **Werkzeug Security** – Password hashing

## Features
- Administrator login and logout
- Session-based authentication
- Protected dashboard and management routes
- Dashboard with summary information
- Service management
- Program management
- Customer inquiry management
- Service request management
- Add, update, and delete records
- Status tracking for each module
- Input validation and duplicate-name prevention for services and programs
- Search and filter functionality
- Flash notifications for application feedback
- JSON-based data persistence
- User-friendly dashboard interface

## Project Structure

```text
veda-technology/
│
├── main.py
├── data.py
├── storage.py
├── requirements.txt
└── README.md
```

*The structure above represents the expected core files; your project may contain additional templates, static files, or data files.*

## Installation and Setup

### 1. Clone or Download the Project
Download the project files and open the project folder in VS Code.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

Ensure `requirements.txt` includes the dependencies used by your project, such as Flask and Werkzeug.

```bash
pip install -r requirements.txt
```

### 5. Configure Login Credentials

The application supports environment variables for the administrator credentials.

**Windows PowerShell:**

```powershell
$env:VEDA_ADMIN_USERNAME="admin"
$env:VEDA_ADMIN_PASSWORD="ChangeThisPassword"
$env:VEDA_SECRET_KEY="replace-with-a-long-random-secret"
```

Use your configured credentials to log in. If you have not configured environment variables, the development defaults in the application may apply.

### 6. Run the Application

```bash
python main.py
```

Open the local address shown in the terminal, typically:

```text
http://127.0.0.1:5000/
```

## How to Use
1. Open the application in your browser.
2. Log in using the administrator credentials.
3. View the dashboard and its summary information.
4. Navigate to the required management section.
5. Add new records or update existing records.
6. Change record statuses when required.
7. Search for records or delete records that are no longer needed.
8. Log out after completing your work.

## Data Management
The application uses the existing `data.py` and `storage.py` modules to initialize, access, and save application data. JSON-based persistence is used instead of a database server.

## Security Notes
- Passwords are handled using Werkzeug password hashing.
- Dashboard and management routes require authentication.
- Configure a strong secret key and administrator password before use.
- The built-in development server and debug mode are intended for local development, not production deployment.
- For production use, add appropriate CSRF protection, secure cookie settings, and a production WSGI server.

## Output Snapshots
Add screenshots of the following application pages to this section:

1. Administrator Login Page
2. Main Dashboard
3. Service Management
4. Program Management
5. Customer Inquiry Management
6. Service Request Management
7. Record Update and Status Management

## Conclusion
The Veda Technology Business & Service Management System provides a centralized solution for managing essential business and customer-service activities. This project demonstrates the practical use of Flask, Python, web technologies, authentication, input validation, and JSON-based data persistence in developing a web application.

---

**Project:** Veda Technology – Business & Service Management System  
**Application Type:** Web Application  
**Backend:** Python and Flask  
**Storage:** JSON-based persistence