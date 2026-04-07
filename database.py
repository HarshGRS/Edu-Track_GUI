import sqlite3

def connect_db():
    return sqlite3.connect("edutrack.db")

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Login table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Insert default users
    cur.execute("INSERT OR IGNORE INTO users VALUES ('admin','admin123','Admin')")
    cur.execute("INSERT OR IGNORE INTO users VALUES ('teacher','teach123','Teacher')")

    # Student table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll INTEGER PRIMARY KEY,
        name TEXT,
        sub1 INTEGER,
        sub2 INTEGER,
        sub3 INTEGER,
        total INTEGER,
        percentage REAL,
        grade TEXT
    )
    """)

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    data = cur.fetchone()
    conn.close()
    return data

def insert_student(data):
    conn = connect_db()
    cur = conn.cursor()
    
    # Calculate total, percentage, and grade
    total = data['sub1'] + data['sub2'] + data['sub3']
    percentage = (total / 300) * 100

    if percentage >= 90:
        grade = 'A+'
    elif percentage >= 80:
        grade = 'A'
    elif percentage >= 70:
        grade = 'B+'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    else:
        grade = 'F'

    cur.execute(
        "INSERT INTO students VALUES (?,?,?,?,?,?,?,?)",
        (data['roll'], data['name'], data['sub1'], data['sub2'], data['sub3'], total, percentage, grade)
    )
    conn.commit()
    conn.close()

def fetch_students():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_student(roll):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY roll")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(data):
    conn = connect_db()
    cur = conn.cursor()

    # Calculate total, percentage, and grade
    total = data['sub1'] + data['sub2'] + data['sub3']
    percentage = (total / 300) * 100

    if percentage >= 90:
        grade = 'A+'
    elif percentage >= 80:
        grade = 'A'
    elif percentage >= 70:
        grade = 'B+'
    elif percentage >= 60:
        grade = 'B'
    elif percentage >= 50:
        grade = 'C'
    else:
        grade = 'F'

    cur.execute("""
        UPDATE students
        SET name=?, sub1=?, sub2=?, sub3=?, total=?, percentage=?, grade=?
        WHERE roll=?
    """, (data['name'], data['sub1'], data['sub2'], data['sub3'], total, percentage, grade, data['roll']))

    conn.commit()
    conn.close()
