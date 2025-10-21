# Flask User Manager

A simple **Flask-based CRUD application** with a responsive GUI to manage users.  
You can **add, update, view, and delete users** using a modern interactive interface.

---

## Features

- **Create Users**: Add single or multiple users at once (bulk addition).  
- **Read Users**: View all registered users in a responsive table.  
- **Update Users**: Edit user name/email directly from the table.  
- **Delete Users**: Remove users with a single click.  
- **Interactive GUI**: Built with **Bootstrap 5**, fully responsive and user-friendly.  
- **SQLite Database**: Lightweight local storage for user data.  

---

## Folder Structure

flask-user-manager/
├─ app.py # Main Flask application
├─ users.db # SQLite database
├─ templates/
│ └─ index.html # GUI HTML file
└─ static/
├─ style.css # Custom CSS
└─ script.js # JS for GUI interaction

## Installation

1. **Clone the repository**


git clone https://github.com/vaibhavsawant201/flask-user-manager.git
cd flask-user-manager
Create a virtual environment (optional but recommended)


python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies


pip install Flask
Running the App
bash
Copy code
python app.py
Open your browser and navigate to:


http://127.0.0.1:5000/ui  //You should see the Flask User Manager GUI.

API Endpoints
Endpoint	Method	Description
/register_bulk	POST	Add single or multiple users
/users	GET	Get all users
/update_user/<int:id>	PUT	Update user by ID
/delete_user/<int:id>	DELETE	Delete user by ID

Screenshots
Add / Update / Delete Users Interface


<img width="1772" height="889" alt="Screenshot 2025-10-21 180526" src="https://github.com/user-attachments/assets/b9392dfd-287d-4287-bd6d-61eeb4c9100d" />


This project is open source and free to use.



