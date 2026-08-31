# Student Management System

A full-stack **Student Management System** built using **Python, Django, MySQL, HTML, CSS, and JavaScript**.

The project is designed to manage students, teachers, departments, courses, subjects, attendance, and academic results through role-based dashboards and authentication.

---

## 📌 Project Overview

The Student Management System is a web-based application that helps educational institutions manage academic and administrative information in one place.

The system provides separate functionality for:

- **Administrator**
- **Teacher**
- **Student**

Each role has different permissions and access to different features.

---

## 🚀 Features

### 👨‍💼 Administrator

The Administrator can manage the complete system.

#### Student Management

- Add students
- Edit student information
- Delete students
- View student details
- Search students
- Filter students by department
- Filter students by course
- Assign students to courses
- Create login accounts for students

#### Teacher Management

- Add teachers
- Edit teacher information
- Delete teachers
- View teachers
- Search teachers
- Filter teachers by department
- Create login accounts for teachers
- Assign subjects to teachers
- View subjects taught by each teacher

#### Department Management

- Add departments
- Edit departments
- Delete departments
- View department information
- Manage department codes and names

#### Course Management

- Add courses
- Edit courses
- Delete courses
- Assign courses to departments
- Search and filter courses
- Support the same course code across different departments

Example:
CSE  → B.Tech → Bachelor Of Technology
ECE  → B.Tech → Bachelor Of Technology
AIML → B.Tech → Bachelor Of Technology





### Subject Management:

Add subjects
Edit subjects
Delete subjects
Assign subjects to courses
Organize subjects by semester
View subjects by department and course

### Attendance Management:

Record attendance
View attendance
Track attendance status
Manage student attendance records

### Results Management:

Add academic results
Update results
View student results
Manage academic performance information



👨‍🏫 Teacher Features:

Teachers have their own dashboard and can access teacher-specific information.

Teacher Dashboard

### Teachers can access:

Dashboard
Students
Attendance
Results
My Profile
My Subjects
My Profile

### Teachers can view:

Teacher ID
First Name
Last Name
Email
Phone
Department
Designation
Qualification
Joining Date
Address
My Subjects

### Teachers can view all subjects assigned to them:

Example:

Teacher: Naveen Kumar

Department:
CSE - Computer Science Engineering

Subjects:

M1 - Matrices and Calculus
PY - Python Programming


Teacher Subject Assignment

When an Admin creates a teacher:

Select Department
        ↓
Load Department Subjects
        ↓
Select Subjects
        ↓
Create Teacher
        ↓
Teacher Login
        ↓
My Subjects

The teacher can be assigned multiple subjects.

This is implemented using a Many-to-Many relationship between Teacher and Subject.

👨‍🎓 Student Features:

Students have access to their own academic information.

Student Dashboard

Students can access:

Dashboard
My Profile
My Course
My Attendance
My Results
My Profile

Students can view:

Student ID
Name
Email
Phone
Date of Birth
Gender
Course
Year
Address
My Course

Students can view:

Course name
Course code
Department
Course duration
Subjects available in the course
My Attendance

Students can view their attendance records.

My Results

Students can view their academic results.



🔐 Authentication and Authorization:

The project uses Django authentication and Django Groups for role-based access.

User Roles
Admin
Teacher
Student

Users are assigned to the appropriate group.

The navigation and protected views are designed according to the user's role.

🏗️ System Architecture

The major relationships in the application are:

Department
    │
    └── Course
          │
          └── Subject
                 │
                 └── Teacher

Students are connected to courses:

Department
    │
    └── Course
          │
          └── Student

Teachers can teach multiple subjects:

Teacher
   ↕
Subject
🗄️ Database

The application uses MySQL as its database.

Main Entities
User
Department
Course
Subject
Student
Teacher
Attendance
Result
Relationships
Department → Course

One department can have multiple courses.

Course → Subject

One course can have multiple subjects.

Course → Student

Students are assigned to a course.

Teacher ↔ Subject

Teachers can teach multiple subjects and subjects can be taught by multiple teachers.

User → Student / Teacher

Student and Teacher profiles are connected to Django user accounts for authentication.



💻 Technology Stack:

## Frontend:
HTML5
CSS3
JavaScript
## Backend:
Python
Django 5.2
## Database:
MySQL 8.0+
## Authentication:
Django Authentication
Django Groups
Role-based access control
Additional Python Packages
Django REST Framework
Simple JWT
mysqlclient


📁 Project Structure
STUDENT_MANAGEMENT_SYSTEM/
│
├── backend/
│   │
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── accounts/
│   │
│   ├── students/
│   │
│   ├── teachers/
│   │
│   ├── departments/
│   │
│   ├── courses/
│   │
│   ├── subjects/
│   │
│   ├── attendance/
│   │
│   ├── results/
│   │
│   ├── dashboard/
│   │
│   ├── templates/
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
├── requirements.txt
├── .gitignore
├── run.bat
└── README.md


⚙️ Installation
1. Clone the Repository
git clone https://github.com/Satya-Narayana2026/Student_Management_System.git

Go into the project:

cd Student_Management_System
2. Create Virtual Environment

Create a virtual environment:

python -m venv backend/venv

Activate it on Windows:

backend\venv\Scripts\activate
3. Install Dependencies

Install all required Python packages:

pip install -r requirements.txt


🗄️ MySQL Setup

Make sure MySQL Server is installed and running.

Create the database:

CREATE DATABASE student_management;

Configure the database in:

backend/config/settings.py

Example:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "student_management",
        "USER": "your_mysql_username",
        "PASSWORD": "your_mysql_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

For production use, database credentials should be stored in environment variables.

🔄 Database Migrations

Go to the backend folder:

cd backend

Run:

python manage.py makemigrations

Then:

python manage.py migrate
👤 Create Admin User

Create a Django superuser:

python manage.py createsuperuser

Enter the required username, email, and password.

▶️ Run the Application

Start the Django development server:

python manage.py runserver

Open:

http://127.0.0.1:8000/
🪟 Windows Quick Start

The project includes:

run.bat

From the project root, you can run:

run.bat

This starts Django using the project's virtual-environment Python interpreter.
