# Imports
from datetime import datetime
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, sendOTP, srvlog

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/oes.db")

# List Roles
roles = ['Admin', 'Teacher', 'Student']
# Default Rows of Data per Page & Pagination Gap
def_rows_per_page = 10
def_gap = 2


""" Routes """


# Home
@app.route("/")
@login_required
def home():
	rows = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))

	for detail in rows[0]:
		session[detail] = rows[0][detail]

	return render_template("home.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
	"""Log user in"""

	# Check if user is logged in already and prevent accidental log out
	# TODO
	# Forget any user_id
	session.clear()

	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":

		# Ensure email was submitted
		if not request.form.get("email"):
			return apology("must provide email", 403)

		# Ensure password was submitted
		elif not request.form.get("password"):
			return apology("must provide password", 403)

		# Query database for email
		rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

		# Ensure email exists and password is correct
		if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
			return apology("invalid email and/or password", 403)

		# Remember which user has logged in
		session["user_id"] = rows[0]["id"]

		# Redirect user to home page
		return redirect("/")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
	"""Log user out"""

	# Forget any user_id
	session.clear()

	# Redirect user to login form
	return redirect("/")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
	"""Register user"""

	# Check if user is logged in already and prevent accidental log out
	# TODO
	# Forget any user_id
	session.clear()

	# User reached route via POST (as by submitting a form via POST)
	if request.method == "POST":

		# Ensure email was submitted
		if not request.form.get("email"):
			return apology("missing email")

		form_email = request.form.get("email")

		# Query database for email
		rows = db.execute("SELECT * FROM users WHERE email = ?", form_email)

		# Ensure email is not already taken
		if len(rows) != 0:
			return apology("email is already taken")

		# Ensure Required Details were submitted
		details = ['first_name', 'middle_name', 'last_name', 'password', 'confirmation']
		for detail in details:
			# Ensure Detail was submitted
			if not request.form.get(detail):
				return apology(f"missing {detail}")

		form_password = request.form.get("password")
		form_confirm = request.form.get("confirmation")

		# Match passwords for confirmation
		if form_password != form_confirm:
			return apology("passwords don't match")

		# Gather details from form
		form_fname = request.form.get("first_name")
		form_mname = request.form.get("middle_name")
		form_lname = request.form.get("last_name")
		form_role = request.form.get("role")

		# Insert user into database & Remember which user has logged in
		session["user_id"] = db.execute("INSERT INTO users (email, first_name, middle_name, last_name, hash, role, registered) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))", form_email, form_fname, form_mname, form_lname, generate_password_hash(form_password), form_role)

		# Redirect user to home page
		return redirect("/")

	# User reached route via GET (as by clicking a link or via redirect)
	else:
		return render_template("register.html", roles = roles)


# Profile
@app.route("/profile")
@login_required
def profile():
		return render_template("profile.html")


# Forgot
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
	if request.method == "POST":
		if not request.form.get("email"):
			return apology("missing email")
		email = request.form.get("email")

		rows = db.execute("SELECT id FROM users WHERE email = ?", email)
		if len(rows) != 1:
			return apology("email not found")

		# Temporarily Log User In
		session["user_id"] = rows[0]["id"]
		session["OTP"] = sendOTP(email)

		return redirect("/reset")
	else:
		return render_template("forgot.html")


# Reset
@app.route("/reset", methods=["GET", "POST"])
@login_required
def reset():
	if request.method == "POST":
		# Log User Out
		id = session["user_id"]
		otp = session["OTP"]
		session.clear()

		# Ensure Required Details were submitted
		details = ['otp', 'password', 'confirmation']
		for detail in details:
			# Ensure Detail was submitted
			if not request.form.get(detail):
				return apology(f"missing {detail}")

		# Check OTP
		if request.form.get("otp") != otp:
			return apology("OTP does not match")

		form_password = request.form.get("password")
		form_confirm = request.form.get("confirmation")

		# Match passwords for confirmation
		if form_password != form_confirm:
			return apology("passwords don't match")

		db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(form_password), id)

		# Log User In
		session["user_id"] = id

		# Redirect user to home page
		return redirect("/")
	else:
		return render_template("reset.html")


# Change
@app.route("/pwchange", methods=["GET", "POST"])
@login_required
def pwchange():
	if request.method == "POST":
		# Ensure Required Details were submitted
		details = ['old', 'password', 'confirmation']
		for detail in details:
			# Ensure Detail was submitted
			if not request.form.get(detail):
				return apology(f"missing {detail}")

		# Fetch Old Pasword Hash
		rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

		# Check Old Password Submitted by User
		if not check_password_hash(rows[0]["hash"], request.form.get("old")):
			return apology("OTP does not match")

		form_password = request.form.get("password")
		form_confirm = request.form.get("confirmation")

		# Match passwords for confirmation
		if form_password != form_confirm:
			return apology("passwords don't match")

		db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(form_password), session["user_id"])
		return redirect("/")
	else:
		return render_template("pwchange.html")


# Verify
@app.route("/verify", methods=["GET", "POST"])
@login_required
def verify():
	if request.method == "POST":
		if request.form.get("otp") == session["OTP"]:
			db.execute("UPDATE users SET verified = 1 WHERE id = ?", session.get("user_id"))
			return apology("verified!", 200)
		else:
			return apology("not verified")
	else:
		rows = db.execute("SELECT verified FROM users WHERE id = ?", session.get("user_id"))
		if not bool(int(rows[0]["verified"])):
			OTP = sendOTP(session.get("email"))
			if OTP:
				session["OTP"] = OTP
				return render_template("verify.html")
			else:
				return apology("unable to send verification email")
		else:
			return apology("already verified")


# Unapproved
@app.route("/unapproved")
@login_required
def unapproved():
	if session.get("role") != "Admin":
		return apology("unauthorized action")

	rows = db.execute("SELECT id, email, role FROM users WHERE verified = 1 AND approved = 0")

	return render_template("unapproved.html", users = rows)


# Approve
@app.route("/approve", methods=["GET", "POST"])
@login_required
def approve():
	if session.get("role") != "Admin":
		return apology("unauthorized action")

	if request.method == "POST":
		db.execute("UPDATE users SET approved = 1, approved_by = ? WHERE id = ?", session.get("user_id"), request.form.get("id"))
		return redirect("/unapproved")
	else:
		if not request.args.get("id"):
			return apology("missing user id for approval")

		rows = db.execute("SELECT email, first_name, middle_name, last_name, role, registered FROM users WHERE id = ? AND verified = 1 AND approved = 0", request.args.get("id"))

		if len(rows) == 0:
			return apology("specified user not found")

		return render_template("approve.html", details = rows[0], id = request.args.get("id"))


# Add
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
	if session.get("role") != "Teacher":
		return apology("unauthorized action")

	options = ['A', 'B', 'C', 'D']

	if request.method == "POST":
		# Ensure Required Details were submitted
		details = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']
		for detail in details:
			# Ensure Detail was submitted
			if not request.form.get(detail):
				return apology(f"missing {detail}")

		if request.form.get('answer') not in options:
			return apology("invalid answer / option submitted")

		db.execute(f"INSERT INTO questions ({', '.join(details)}, updated_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
		request.form.get("question"),
		request.form.get("option_a"),
		request.form.get("option_b"),
		request.form.get("option_c"),
		request.form.get("option_d"),
		request.form.get("answer"),
		session.get("user_id")
		)

		return redirect("/questions")
	else:
		return render_template("add.html", options = options)


# Questions
@app.route("/questions")
@login_required
def questions():
	if session.get("role") != "Teacher":
		return apology("unauthorized action")

	rows = db.execute("SELECT COUNT(id) FROM questions")
	pages = rows[0]["COUNT(id)"] // def_rows_per_page

	if not request.args.get("page"):
		return redirect("/questions?page=1")

	page = request.args.get("page", type = int)

	if page < 1:
		return redirect("/questions?page=1")

	if page > pages:
		return redirect(f"/questions?page={pages}")

	offset = (page - 1) * def_rows_per_page
	rows = db.execute("SELECT id, question FROM questions ORDER BY id LIMIT ? OFFSET ?", def_rows_per_page, offset)

	return render_template("questions.html", questions = rows, page = page, pages = pages, gap = def_gap)


# Update
@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
	if session.get("role") != "Teacher":
		return apology("unauthorized action")

	options = ['A', 'B', 'C', 'D']

	if request.method == "POST":
		# Ensure Required Details were submitted
		details = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']
		for detail in details:
			# Ensure Detail was submitted
			if not request.form.get(detail):
				return apology(f"missing {detail}")

		if request.form.get('answer') not in options:
			return apology("invalid answer / option submitted")

		query = f"UPDATE questions SET {' = ?, '.join(details)} = ?, updated_by = ? WHERE id = ?"

		db.execute(query, request.form.get("question"), request.form.get("option_a"), request.form.get("option_b"), request.form.get("option_c"), request.form.get("option_d"), request.form.get("answer"), session.get("user_id"), request.form.get("id"))

		return redirect("/questions")
	else:
		if not request.args.get("id"):
			return apology("missing question id for updation")

		rows = db.execute("SELECT * FROM questions WHERE id = ?", request.args.get("id"))

		if len(rows) == 0:
			return apology("specified question not found")

		return render_template("update.html", options = options, details = rows[0])


# Test
@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
	if session.get("role") != "Student":
		return apology("unauthorized action")

	if request.method == "POST":
		attempted = 0
		correct = 0
		max = len(session.get("Qids"))

		# srvlog(session["Qids"])

		# Fetch Answers
		listint = session.get("Qids")
		# srvlog(listint)

		listint.sort()
		# srvlog(listint)

		liststr = []
		for Qid in listint:
			liststr.append(str(Qid))
		# srvlog(liststr)

		querystr = ", ".join(liststr)
		# srvlog(querystr)

		query = f"SELECT id, answer FROM questions WHERE id in ({querystr})"
		# srvlog(query)

		rows = db.execute(query)
		# srvlog(rows)

		for index, Qid in enumerate(listint):
			# srvlog(f"{index} -> {Qid}")
			# Check if attempted
			if request.form.get(str(Qid)):
				# srvlog(f"Q No : {Qid} -> Ans : {request.form.get(str(Qid))}")
				attempted += 1
				# Check answer
				if request.form[str(Qid)] == rows[index]["answer"]:
					correct += 1

		# srvlog(f" Max : {max} | Attempted : {attempted} | Correct : {correct} ")

		# Save Test Results
		session["latestTest"] = db.execute("INSERT INTO tests (student_id, max, attempted, correct) VALUES (?, ?, ?, ?)", session.get("user_id"), max, attempted, correct)

		if request.form["timeout"] == "True":
			session["timeout"] = True
		else:
			session["timeout"] = False

		session["test_submitted"] = True

		return redirect("/submit")
	else:
		# Select a fixed number of questions at random
		rows = db.execute("SELECT id, question, option_a, option_b, option_c, option_d FROM questions ORDER BY RANDOM() LIMIT 10")

		session["Qids"] = []
		for row in rows:
			session["Qids"].append(row["id"])

		# session["test_start"] =

		return render_template("test.html", questions = rows)


# Submit
@app.route("/submit")
@login_required
def submit():
	if session.get("role") != "Student":
		return apology("unauthorized action")

	# srvlog(type(session.get("timeout")))
	# srvlog(session.get("timeout"))

	return render_template("submit.html", timeout = session.get("timeout"))


#Result
@app.route("/result")
@login_required
def result():
	if session.get("role") != "Student":
		return apology("unauthorized action")

	details = 'tests.id, first_name, middle_name, last_name, email, max, attempted, correct'

	query = f"SELECT {details} FROM users JOIN tests ON users.id = tests.student_id WHERE users.id = {session.get('user_id')} ORDER BY tests.id DESC LIMIT 1"
	# srvlog(query)

	rows = db.execute(query)
	# srvlog(rows)

	return render_template("result.html", details = rows[0])

# Feedback
@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
	if session.get("role") != "Student":
		return apology("unauthorized action")

	if not session.get("test_submitted"):
		return apology("already submitted feedback")

	if request.method == "POST":
		if request.form.get("comments"):
			db.execute("INSERT INTO feedbacks (provided_by, rating, recommendation, comments) VALUES (?, ?, ?, ?)", session.get("user_id"), request.form.get("rating"), request.form.get("recommendation"), request.form.get("comments"))
		else:
			db.execute("INSERT INTO feedbacks (provided_by, rating, recommendation) VALUES (?, ?, ?)", session.get("user_id"), request.form.get("rating"), request.form.get("recommendation"))

		session["test_submitted"] = False

		return redirect("/")
	else:
		return render_template("feedback.html")


# Handle error
def errorhandler(e):
	if not isinstance(e, HTTPException):
		e = InternalServerError()
	return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
	app.errorhandler(code)(errorhandler)
