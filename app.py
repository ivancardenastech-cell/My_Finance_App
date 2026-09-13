from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

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
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("landing.html")

        password = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (name, username, email, hash) VALUES (?, ?, ?, ?)", name, username, email, password)
        except ValueError:
            return render_template("landing.html")

        return render_template("index.html")






