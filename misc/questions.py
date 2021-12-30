from cs50 import SQL
from secrets import randbelow
from random import randint

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/oes.db")

noquestions = 100

options = ['A', 'B', 'C', 'D']

for index in range(1, noquestions + 1):

    # Insert user details into database
    db.execute(
        f"INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
        f'Question Content {index}',
        'Opt A',
        'Opt B',
        'Opt C',
        'Opt D',
        options[randbelow(4)],
        randint(5, 8)
        )
