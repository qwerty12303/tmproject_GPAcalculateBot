import sqlite3
from dataclasses import dataclass

@dataclass
class Subject:
    id: int
    name: str
    grade: float
    credits: int
    user_id: int

def connect_db():
    return sqlite3.connect('gpa_calculator.db')

def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade REAL,
            credits INTEGER,
            user_id INTEGER
        )
        ''')
        conn.commit()

def add_subject(user_id, name, grade, credits):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO subjects (name, grade, credits, user_id)
        VALUES (?, ?, ?, ?)
        ''', (name, grade, credits, user_id))
        conn.commit()

def get_subjects(user_id):
    subjects = []
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM subjects WHERE user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            subjects.append(Subject(id=row[0], name=row[1], grade=row[2], credits=row[3], user_id=row[4]))
    return subjects

def delete_subject(subject_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM subjects WHERE id = ?
        ''', (subject_id,))
        conn.commit()

init_db()