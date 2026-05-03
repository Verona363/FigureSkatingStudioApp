import sqlite3
from flask import Flask
from flask import flash
from flask import abort, make_response, redirect, render_template, request, session
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
    all_coaches= users.get_coaches()
    #returns a list of rows, each is a dictionary
    user=None
    if "user_id" in session:
        user = users.get_user(session["user_id"])
    return render_template( "index.html", items=all_items, coaches=all_coaches, user=user)
    #should b added here loginhtml

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items=users.get_items(user_id)
    image= users.get_image(user_id)
    return render_template("show_user.html", user=user, items=items, image=image)

@app.route("/images/<int:user_id>")
def edit_images(user_id):
    require_login()

    current_user = users.get_user(session["user_id"])
    target_user = users.get_user(user_id)

    if not target_user:
        abort(404)
    #  RULES:
    # Admin can edit:
    #   - himself
    #   - coaches
    # Admin CANNOT edit clients
    # Non-admins can only edit themselves
    if current_user["role"] == "admin":
        if target_user["role"] == "client" and target_user["id"] != current_user["id"]:
            abort(403)
    else:
        if target_user["id"] != current_user["id"]:
            abort(403)
    
    image= users.get_image(user_id)
    return render_template("images.html", user=target_user, image=image)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    current_user = users.get_user(session["user_id"])
    target_user_id = int(request.form["user_id"])
    target_user = users.get_user(target_user_id)

    if not target_user:
        abort(404)

    if current_user["role"] == "admin":
        if target_user["role"] == "client" and target_user["id"] != current_user["id"]:
            abort(403)
    else:
        if target_user["id"] != current_user["id"]:
            abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".jpg"):
        return "ERROR: wrong file format"

    image = file.read()

    users.update_image(target_user_id, image)
    return redirect("/user/" + str(target_user_id))

@app.route("/remove_image", methods=["POST"])
def remove_image():
    require_login()

    current_user = users.get_user(session["user_id"])
    target_user_id = int(request.form["user_id"])
    target_user = users.get_user(target_user_id)

    if not target_user:
        abort(404)

    if current_user["role"] == "admin":
        if target_user["role"] == "client" and target_user["id"] != current_user["id"]:
            abort(403)
    else:
        if target_user["id"] != current_user["id"]:
            abort(403)

    users.remove_image(target_user_id)

    return redirect("/user/" + str(target_user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/find_item")
def find_item():
    user=None
    if "user_id" in session:
        user = users.get_user(session["user_id"])
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
    return render_template( "find_item.html", query=query, results=results, user=user)
    #for this part query=qury (1st is what html sees as a variable,
    #2ND is our python code variable name)
    #html_template_variable = python_variable

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    participants=items.get_participants(item_id)
    user=None
    booked=False

    if "user_id" in session:
        user = users.get_user(session["user_id"])
        booked = items.is_booked(item_id, session["user_id"])
    return render_template ("show_item.html", item=item,
                            participants=participants, booked=booked,
                            user=user)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes() 
    coaches=users.get_coaches()
    user = users.get_user(session["user_id"])
    if user["role"] not in ("coach", "admin"):
        abort(403)
    return render_template( "new_item.html", coaches=coaches, classes=classes, user=user)


@app.route("/book_training", methods=["POST"])
def book_training():
    require_login()
    item_id = request.form["item_id"]
    
    item = items.get_item(item_id)
    if not item:
        abort(403)
    
    user_id = session["user_id"]
    try:
        items.add_booking(item_id, user_id)
        flash("You booked a training")
    except:
        flash("You are already registered")
        #pass #later show message "Already registered" and add cancel function

    return redirect("/item/"+ str (item_id))

@app.route("/cancel_booking", methods=["POST"])
def cancel_booking():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]
    try:
        items.cancel_booking(item_id, user_id)
        flash("Booking is cancelled")
    except:
        pass #later show message "Already registered" and add cancel function

    return redirect("/item/"+ str (item_id))

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    user_id = session["user_id"]
    user=users.get_user(user_id)

    if user["role"] not in ("coach", "admin"):
        abort(403)

    CLASS_FIELDS = ["training_type", "specialization", "format", "training_level"]
    OPTIONAL_FIELDS = {"specialization"}

    all_classes = items.get_all_classes()
    validated_classes = {}

    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)

    for field in CLASS_FIELDS:
        value = request.form.get(field)

        # 🔒 field must exist
        if value is None:
            abort(403)

        # ✅ optional handling
        if value == "":
            if field in OPTIONAL_FIELDS:
                validated_classes[field] = None
                continue
            else:
                abort(403)

        # 🔒 field name must be valid
        if field not in all_classes:
            abort(403)

        # 🔒 value must be one of allowed options
        if value not in all_classes[field]:
            abort(403)

        validated_classes[field] = value

    if user["role"] == "admin":
        coach_id = int(request.form["coach_id"])  # admin can choose
    else:
        coach_id = session["user_id"]  # coach can only assign themselves

    coach = users.get_user(coach_id)
    if not coach:
        abort(403)

    training_date = request.form["training_date"]
    if not training_date:
        abort(403)

    training_time = request.form["training_time"]
    if not training_time:
        abort(403)

    training_description = request.form["training_description"]
    if len(training_description) > 1000:
        abort(403)


    items.add_item(
        title,
        validated_classes["training_type"],
        validated_classes["specialization"],
        validated_classes["format"],
        validated_classes["training_level"],
        coach_id,
        training_date,
        training_time,
        training_description,
        user_id
    )

    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    user_id = session["user_id"]
    user=users.get_user(user_id)
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["coach_id"] != session["user_id"] and user["role"] != "admin":
        abort(403)

    
    coaches = users.get_coaches()
    return render_template( "edit_item.html", item=item, coaches=coaches, user=user)


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"] #something what is different from create item function
    #requesting item id from html edit_item
    item=items.get_item(item_id)
    user_id = session["user_id"]
    user=users.get_user(user_id)
    if not item:
        abort(404)
    if item["coach_id"] != session["user_id"] and user["role"] != "admin":
        abort(403)
    
    title = request.form["title"]
    if not title or len(title)>80:
        abort(403)

    CLASS_FIELDS = ["training_type", "specialization", "format", "training_level"]
    OPTIONAL_FIELDS = {"specialization"}
    all_classes = items.get_all_classes()
    validated_classes = {}
    for field in CLASS_FIELDS:
        value = request.form.get(field)

        # 🔒 field must exist
        if value is None:
            abort(403)

        # ✅ optional handling
        if value == "":
            if field in OPTIONAL_FIELDS:
                validated_classes[field] = None
                continue
            else:
                abort(403)

        # 🔒 field name must be valid
        if field not in all_classes:
            abort(403)

        # 🔒 value must be one of allowed options
        if value not in all_classes[field]:
            abort(403)

        validated_classes[field] = value

    if user["role"] == "admin":
        coach_id = int(request.form["coach_id"])  # admin can choose
    else:
        coach_id = session["user_id"]  # coach can only assign themselves

    coach = users.get_user(coach_id)
    if not coach:
        abort(403)

    training_date = request.form["training_date"]
    if not training_date:
        abort(403)

    training_time = request.form["training_time"]
    if not training_time:
        abort(403)

    training_description = request.form["training_description"]
    if len(training_description) > 1000:
        abort(403)

    items.update_item(
        item_id,
        title,
        validated_classes["training_type"],
        validated_classes["specialization"],
        validated_classes["format"],
        validated_classes["training_level"],
        coach_id,
        training_date,
        training_time,
        training_description)
    return redirect("/item/"+str(item_id))


@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item=items.get_item(item_id)
    user_id = session["user_id"]
    user=users.get_user(user_id)
    if not item:
        abort(404)
    if item["coach_id"] != session["user_id"] and user["role"] != "admin":
        abort(403)
        
    if request.method == "GET":
        return render_template( "remove_item.html", item=item, user=user)
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
    role=request.form["role"]

    #1 Validate passwords
    if password1 != password2:
        return "ERROR: passwords do not match"
    #2 Validate role
    if role not in ("client", "coach"):
        abort(403)
    #3 Create User
    try:
        users.create_user(username, password1, role)
    except sqlite3.IntegrityError:
        return "ERROR: id is already taken"

    return "Account created"
    #Later add a button back to the main later on!!
    #no redirecting

@app.route("/login", methods=[ "GET", "POST"])
def login():
    user=None
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
    #if we just came to this page
        return render_template("login.html", user=user)

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
            user=users.get_user(user_id)
            session["user_id"]=user_id
            session["username"] = username
            role=user["role"]
            session["role"]=role
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