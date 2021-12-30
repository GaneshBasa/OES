from cs50 import SQL
from random import randint

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/oes.db")

nostudents = 5
notests = 3
max = 10

for student_id in range(1, nostudents + 1):

    for index in range(1, notests + 1):
        # Calc attempted & correct
        attempted = randint(1, max)
        correct = randint(1, attempted)

        # Insert test details into database
        db.execute(
            f"INSERT INTO tests (taken_by, max, attempted, correct, start, end) VALUES (?, ?, ?, ?, datetime('now'), datetime('now', '+{randint(5, 10) / 10} hours'))",
            student_id + 8,
            max,
            attempted,
            correct
            )
