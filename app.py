
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, validate

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ishare.db")

# Creating the necessary tables (users, listing(items), transactions)
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NON NULL, hash TEXT NON NULL)")
db.execute("CREATE TABLE IF NOT EXISTS listing (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, title TEXT NON NULL, description TEXT NON NULL, date DATE, available TEXT NON NULL DEFAULT 'Yes', image TEXT NON NULL DEFAULT 'static/no_image.jpg', FOREIGN KEY (user_id) REFERENCES users(id))")
db.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, type TEXT NON NULL, product_id INTEGER NOT NULL, title TEXT NON NULL, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES listing(product_id))")


# Landing page : Site introduction + items available
@app.route("/")
def index():
    # Getting all listed items
    listing = db.execute("SELECT * FROM listing")

    return render_template("index.html", listing=listing)


# Page for the user to submit what they want to borrow
@app.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow():
    # Via GET you should display borrow page

    if request.method == "POST":
        product_id = request.form.get("product_id")

        # Updating product available status to "No"
        db.execute("UPDATE listing SET available = 'No' WHERE product_id = (?)", product_id)
        title = db.execute("SELECT title FROM listing WHERE product_id = (?)", product_id)

        # - Connect borrow item to the user (transaction)
        db.execute("INSERT INTO transactions (user_id, type, product_id, title) VALUES (?,'Borrow',?,?)",
                   session["user_id"], product_id, title[0]["title"])

        return redirect("/")

    # Getting all the items that are NOT from the current user
    listing = db.execute("SELECT * FROM listing WHERE user_id <> (?)", session["user_id"])
    return render_template("borrow.html", listing=listing)


# Page showing all transactions
@app.route("/history", methods=["GET", "POST"])
@login_required
def history():

    listing = db.execute("SELECT type, product_id, title FROM transactions WHERE user_id = (?)", session["user_id"])

    return render_template("history.html", listing=listing)


# Page to list items
@app.route("/lend", methods=["GET", "POST"])
@login_required
def lend():

    listing = db.execute("SELECT * FROM listing WHERE user_id = (?)", session["user_id"])

    if request.method == "POST":
        # 1 - Marking item as returned or unavailable
        if request.form.get("product_id"):
            available_status = request.form.get("available")
            db.execute("UPDATE listing SET available = (?) WHERE product_id = (?)",
                       available_status, request.form.get("product_id"))
            listing = db.execute("SELECT * FROM listing WHERE user_id = (?)", session["user_id"])
            return render_template("lend.html", listing=listing)

        # 2 - Adding a new item to listing
        title = request.form.get("title")
        description = request.form.get("description")
        start_date = request.form.get("date")

        # Adding the into to the db
        db.execute("INSERT INTO listing (user_id, title, description, date) VALUES (?, ?, ?, ?)", session["user_id"], title, description, start_date)
        # Getting the product_id that has just been added
        item = db.execute("SELECT * FROM listing ORDER BY product_id DESC LIMIT 1;")
        db.execute("INSERT INTO transactions (user_id, type, product_id, title) VALUES (?,'Listed',?,?)",
                   session["user_id"], item[0]["product_id"], item[0]["title"])

        return redirect("/")

    return render_template("lend.html", listing=listing)

# LogIN
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    return redirect("/")

# Product page
@app.route("/product-page", methods=["GET","POST"])
@login_required
def product_page():
    if request.method == "POST":

        product_id = request.form.get("product_id")

        # Getting the item's info
        listing = db.execute("SELECT * FROM listing WHERE product_id = ?", product_id)

        return render_template("product_page.html", listing=listing)

    return render_template("borrow.html")

# Simple profile page
@app.route("/profile")
@login_required
def profile():

    return render_template("profile.html")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == ("POST"):
        # If required attribute used -> nothing is empty
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")


        # Check if username already taken
        users = db.execute("SELECT username FROM users")
        for user in users:
            if user["username"] == username:
                return apology("Username already taken")

        # Check if password and password confirmation don't match
        if password != password2:
            return apology("Passwords don't match")

        # Generating hash
        hash_value = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_value)

        return redirect("/login")

    return render_template("register.html")