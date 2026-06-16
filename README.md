# FlaskBook

A small student–sports enrollment app, used as a practice project to
consolidate Flask, SQL and object-oriented design.

Students log in by id and name, enroll in or drop sports, and search
available sports in real time (AJAX). Built on Flask, SQLite and Jinja2.

## Project evolution

This repo is a learning project, refactored in stages:

- **v1 — CS50 practice.** First version, written to revisit Flask
  fundamentals: routes, GET/POST, sessions, and SQL queries. Database
  access lived in standalone functions, with the student id passed
  around as an argument everywhere.
- **v2 — OOP refactor (current).** Database logic reorganized around a
  `Student` class. The student id now lives as object state instead of
  being threaded through every function. Enrolled and unenrolled sports
  are exposed as properties (always fresh from the DB), while creation
  and validation stay as module-level functions since they don't need
  an existing instance.
- **v3 — decorators (planned).** Introduce a `login_required` decorator
  to remove the repeated session check across protected routes.

## Stack

Python · Flask · SQLite · Jinja2 · JavaScript · CSS

## Features

- Student registration and login by id
- Session-based authentication
- Enroll in and drop sports per student
- Real-time AJAX search of available sports
- SQLite database with three tables and foreign keys

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create the database with its initial data:

   ```bash
   sqlite3 flaskbook.db < schema.sql
   ```

3. Run the app:

   ```bash
   flask run
   ```

## Note

This is a practice project, not production software. The OOP refactor
is the main point of interest — see the `Student` class in `app.py`.