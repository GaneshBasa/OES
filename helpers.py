# Imports
import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps
from secrets import randbelow
import smtplib
from textwrap import dedent

source = 'oes.test.email.id@gmail.com'
password = 'JBD4TF{kdgLxeqvH'


def srvlog(data):
    print("* * * Server Log * * *")
    print(data)


def apology(message, code=400):
    # Render message as an apology to user
    def escape(s):
        # Escape special characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    # Decorate routes to require login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_details(details):
    # Ensure Required Details were submitted
    for detail in details:
        # Ensure Detail was submitted
        if not request.form.get(detail):
            return apology(f"missing {detail}")


def genOTP(num):
    # Generate random OTP
    OTP = ""
    for i in range(num) :
        OTP += str(randbelow(10))
    return OTP


def sendOTP(email):
    # Send Verification Email with OTP
    OTP = genOTP(6)
    subject = 'OTP for your OES Account'
    body = f'The One Time Password for your OES Account is {OTP}'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (source, email, subject, body)

    try:
        print("Sending Email . . .")
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(source, password)
        smtp_server.sendmail(source, email, dedent(email_text))
        smtp_server.close()
        print("Email sent successfully!")
        return OTP
    except Exception as exception:
        print("Something went wrong . . . ", exception)


def sendVer(email):
    # TODO
    pass


def sendApr(email):
    # TODO
    pass

