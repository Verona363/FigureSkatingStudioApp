import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template( "index.html")
    #should b added here loginhtml


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: id is already taken"

    return "Account created"
    #no redirecting

@app.route("/login", methods=[ "GET", "POST"])
def login():
    if request.method == "GET":
    #if we just came to this page
        return render_template("login.html")

    if request.method =="POST":
    #we cant open login in the browser, the route only handles form submission(since there was no get before)
    #if user able to login directs him to the main page
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]
        #executes SELECT password_hash FROM users WHERE username = ?
        #The ? is replaced safely with username
        #[("pbkdf2:sha256:600000$abc123$xyz...",)]
        #A database query always returns: a list of rows
        #each row is a tuple of column
        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        #redirecting to the main page afer login
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")