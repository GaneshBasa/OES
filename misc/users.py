from cs50 import SQL
from secrets import randbelow
from random import randint
from helpers import genOTP, generate_random_password
from werkzeug.security import generate_password_hash

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/oes.db")

noadmins = 3
noteachers = 4
nostudents = 5

with open('misc/users.txt', 'at') as users:

    # Admin(s)
    users.write('Admin(s)\n\n')

    for index in range(1, noadmins + 1):

        # Ensure Required Address Details were submitted
        address_details = ['line_1', 'line_2', 'landmark', 'city', 'district', 'state', 'pin']

        # Insert required address details into database
        address_id = db.execute(
            f"INSERT INTO addresses ({', '.join(address_details)}) VALUES ({'?, ' * (len(address_details) - 1)}?)",
            "Flat No. XXX, Dummy CHS",
            "Street Name, Locality / Area",
            "Landmark Details",
            "City Name",
            "District Name",
            "State Name",
            genOTP(6)
        )

        # Generate user log in details
        email = f"admin{index}@domain.tld"
        password = generate_random_password(16)

        # Save user log in details to users.txt
        users.write(f'{email}\t\t{password}\n')

        # Insert user details into database & log the user in
        db.execute(
            f"INSERT INTO users (email, contact, hash, role, first_name, middle_name, last_name, gender, dob, registered, address_id, verified, approved, approved_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0)",
            email,
            genOTP(10),
            generate_password_hash(password),
            'Admin',
            f'ABC{index}',
            f'Admin{index}',
            f'XYZ{index}',
            'M' if randbelow(2) == 0 else 'F',
            f'{randint(1960, 2000)}-{randint(1, 12)}-{randint(1, 31)}',
            f'2021-{randint(10, 12)}-{randint(1, 31)} {randint(0, 23)}:{randint(0, 59)}:{randint(0, 59)}',
            address_id
            )

    users.write('\n')


    # Teacher(s)
    users.write('Teacher(s)\n\n')

    for index in range(1, noteachers + 1):

        # Ensure Required Address Details were submitted
        address_details = ['line_1', 'line_2', 'landmark', 'city', 'district', 'state', 'pin']

        # Insert required address details into database
        address_id = db.execute(
            f"INSERT INTO addresses ({', '.join(address_details)}) VALUES ({'?, ' * (len(address_details) - 1)}?)",
            "Flat No. XXX, Dummy CHS",
            "Street Name, Locality / Area",
            "Landmark Details",
            "City Name",
            "District Name",
            "State Name",
            genOTP(6)
        )

        # Generate user log in details
        email = f"teacher{index}@domain.tld"
        password = generate_random_password(16)

        # Save user log in details to users.txt
        users.write(f'{email}\t\t{password}\n')

        # Insert user details into database & log the user in
        db.execute(
            f"INSERT INTO users (email, contact, hash, role, first_name, middle_name, last_name, gender, dob, registered, address_id, verified, approved, approved_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, {randint(2,4)})",
            email,
            genOTP(10),
            generate_password_hash(password),
            'Teacher',
            f'ABC{index}',
            f'Teacher{index}',
            f'XYZ{index}',
            'M' if randbelow(2) == 0 else 'F',
            f'{randint(1960, 2000)}-{randint(1, 12)}-{randint(1, 31)}',
            f'2021-{randint(10, 12)}-{randint(1, 31)} {randint(0, 23)}:{randint(0, 59)}:{randint(0, 59)}',
            address_id
            )

    users.write('\n')


    # Student(s)
    users.write('Student(s)\n\n')

    for index in range(1, nostudents + 1):

        # Ensure Required Address Details were submitted
        address_details = ['line_1', 'line_2', 'landmark', 'city', 'district', 'state', 'pin']

        # Insert required address details into database
        address_id = db.execute(
            f"INSERT INTO addresses ({', '.join(address_details)}) VALUES ({'?, ' * (len(address_details) - 1)}?)",
            "Flat No. XXX, Dummy CHS",
            "Street Name, Locality / Area",
            "Landmark Details",
            "City Name",
            "District Name",
            "State Name",
            genOTP(6)
        )

        # Generate user log in details
        email = f"student{index}@domain.tld"
        password = generate_random_password(16)

        # Save user log in details to users.txt
        users.write(f'{email}\t\t{password}\n')

        # Insert user details into database & log the user in
        db.execute(
            f"INSERT INTO users (email, contact, hash, role, first_name, middle_name, last_name, gender, dob, registered, address_id, verified, approved, approved_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, {randint(2,4)})",
            email,
            genOTP(10),
            generate_password_hash(password),
            'Student',
            f'ABC{index}',
            f'Student{index}',
            f'XYZ{index}',
            'M' if randbelow(2) == 0 else 'F',
            f'{randint(1960, 2000)}-{randint(1, 12)}-{randint(1, 31)}',
            f'2021-{randint(10, 12)}-{randint(1, 31)} {randint(0, 23)}:{randint(0, 59)}:{randint(0, 59)}',
            address_id
            )

    users.write('\n')
