# **File Sharing System**  

A secure and efficient system for user management, file registration, and file search. This project demonstrates key backend functionalities, including user authentication, file metadata management, and search operations.

---

## **Features**  
- **User Registration**: Register users with secure password hashing using bcrypt and validate against database constraints.  
- **User Login**: Authenticate users with hashed password verification, ensuring only valid users access the system.  
- **File Registration**: Store file details (name, size, type, IP address, and port) in the database for sharing purposes.  
- **File Search**: Query files by name or type with support for partial matches and filters.  
- **Thread-Safe Operations**: Manage concurrent database access using threading locks to prevent race conditions.  
- **RESTful API**: Built using Flask to support structured client-server communication.  

---

## **Tech Stack**  
- **Backend**: Flask (Python), Flask-RESTful, Flask-CORS  
- **Database**: SQLite  
- **Password Hashing**: bcrypt  
- **Concurrent Access**: Python threading  
- **Logging**: Python logging module  

---

## **Setup and Usage**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
