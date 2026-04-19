import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import items
import users
app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template( "index.html", items=all_items)
    #should b added here loginhtml

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items=users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)


@app.route("/find_item")
def find_item():
    query=request.args.get("query")
    #"query" matches the HTML input name="query"
    if query:
        results= items.find_items(query)
    #it returns from database
    #results = [
    #{"id": 1, "title": "Python Basics"},
    #{"id": 2, "title": "Advanced Python"}]

    else:
        query=""
        results=[]
    return render_template( "find_item.html", query=query, results=results)
    #for this part query=qury (1st is what html sees as a variable,
    #2ND is our python code variable name)
    #html_template_variable = python_variable

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/new_item")
def new_item():
    require_login()
    coaches=users.get_all_users()
    return render_template( "new_item.html", coaches=coaches)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    title = request.form["title"]
    if not title or len(title)>80:
        abort(403)
    training_type= request.form["training_type"]
    if not training_type:
        abort(403)
    specialization= request.form["specialization"]
    format= request.form["format"]
    if not format:
        abort(403)
    training_level= request.form["training_level"]
    coach_id= int(request.form["coach_id"])
    coach=users.get_user(coach_id)
    if not coach:
        abort(403)
    training_date= request.form["training_date"]
    if not training_date:
        abort(403)
    training_time= request.form["training_time"]
    if not training_time:
        abort(403)
    training_description=request.form["training_description"]
    if len(training_description)>1000:
        abort(403)
    user_id=session["user_id"]

    items.add_item(title, training_type, specialization, format, training_level, coach_id, training_date, training_time, training_description, user_id)
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if item["user_id"] != session["user_id"] and item["coach_id"] != session["user_id"]:
        abort(403)
    if not item:
        abort(404)
    
    coaches = users.get_all_users()
    return render_template( "edit_item.html", item=item, coaches=coaches)


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"] #something what is different from create item function
    #requesting item id from html edit_item
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"] and item["coach_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title)>80:
        abort(403)
    training_type= request.form["training_type"]
    if not training_type:
        abort(403)
    specialization= request.form["specialization"]
    format= request.form["format"]
    if not format:
        abort(403)
    training_level= request.form["training_level"]
    coach_id= int(request.form["coach_id"])
    coach=users.get_user(coach_id)
    if not coach:
        abort(403)
    training_date= request.form["training_date"]
    if not training_date:
        abort(403)
    training_time= request.form["training_time"]
    if not training_time:
        abort(403)
    training_description=request.form["training_description"]
    if len(training_description)>1000:
        abort(403)

    items.update_item(item_id, title, training_type, specialization, format, training_level, coach_id, training_date, training_time, training_description)
    
    return redirect("/item/"+str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"] and item["coach_id"] != session["user_id"]:
        abort(403)
        
    if request.method == "GET":
        return render_template( "remove_item.html", item=item)
    if request.method == "POST":
        if "remove" in request.form:
    #If we press remove, then it does the following:
            items.remove_item(item_id)
            return redirect("/")
    #Remove is the name="remove" of the button
    #under method post in the html file
    #remove_item.html
        else:
            return redirect("/item/"+ str(item_id))

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
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "ERROR: id is already taken"
    return "Account created"
    #Later add a button back to the main later on!!
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
        user_id=users.check_login(username, password)
        #password_hash=db.query(sql, [username])[0][0]
        #executes SELECT password_hash FROM users WHERE username = ?
        #The ? is replaced safely with username
        #[("pbkdf2:sha256:600000$abc123$xyz...",)]
        #A database query always returns: a list of rows
        #each row is a tuple of column
        if user_id:
            session["user_id"]=user_id
            session["username"] = username
            return redirect("/")
        #redirecting to the main page afer login
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")