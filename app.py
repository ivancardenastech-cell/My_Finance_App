from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import password_validation

app = Flask(__name__)

# configure session to use fylesistem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure response AFTER REQUEST
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["pragma"] = "no-cache"
    return response

# set up the data-base by using CS50 library
db = SQL("sqlite:///finance.db")


@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def log_in():
    # clear the session
    session.clear()

    # get the username and password from the form and check if they are correct
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return redirect("/")
        
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # check if the username exists and if the password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/")
        
        
        # store the user id in the session
        session["user_id"] = rows[0]["id"]
        return render_template("index.html")
    
    # if the request method is GET, render the login page
    elif request.method == "GET":
        return render_template("login.html")
    

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # validate username
        if not name:
            return render_template("signup.html", is_valid=False, message="Name is required")
        if len(name) < 3:
            return render_template("signup.html", is_valid=False, message="Name must be at least 3 characters long")

        # validate username
        if not username:
            return render_template("signup.html", is_valid=False, message="Username is required")
        if len(username) < 1:
            return render_template("signup.html", is_valid=False, message="Username must be at least 1 character long")

        # validate email
        if not email:
            return render_template("signup.html", is_valid=False, message="Email is required")
        if @ not in email:
            return render_template("signup.html", is_valid=False, message="Email must contain @")

        
        # validate the password using the password_validation function from helpers.py
        is_valid, message = password_validation(password)
        if is_valid == False:
            return render_template("signup.html", is_valid=is_valid, message=message)
        
        
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("signup.html", is_valid=False, message="Passwords do not match")

        password = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (name, username, email, hash) VALUES (?, ?, ?, ?)", name, username, email, password)
        except ValueError:
            return render_template("landing.html")

        return render_template("index.html")






