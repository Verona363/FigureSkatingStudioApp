import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import items

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template( "index.html", items=all_items)
    #should b added here loginhtml

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    return render_template("show_item.html", item=item)

@app.route("/new_item")
def new_item():
    return render_template( "new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    training_type= request.form["training_type"]
    specialization= request.form["specialization"]
    format= request.form["format"]
    training_level= request.form["training_level"]
    coach= request.form["coach"]
    training_date= request.form["training_date"]
    training_time= request.form["training_time"]
    training_description=request.form["training_description"]
    user_id=session["user_id"]

    items.add_item(title, training_type, specialization, format, training_level, coach, training_date, training_time, training_description, user_id)
    return redirect("/")


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

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        # result looks like {id": 1, "password_hash": "hashed_password_here"}
        user_id=result["id"]
        password_hash=result["password_hash"]
        #password_hash=db.query(sql, [username])[0][0]
        #executes SELECT password_hash FROM users WHERE username = ?
        #The ? is replaced safely with username
        #[("pbkdf2:sha256:600000$abc123$xyz...",)]
        #A database query always returns: a list of rows
        #each row is a tuple of column
        if check_password_hash(password_hash, password):
            session["user_id"]=user_id
            session["username"] = username
            return redirect("/")
        #redirecting to the main page afer login
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")