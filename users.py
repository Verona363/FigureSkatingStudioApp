import db
from werkzeug.security import check_password_hash, generate_password_hash

def create_user(username, password1, role):
    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, role])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])[0]
    if not result:
        return None 
    # result looks like {id": 1, "password_hash": "hashed_password_here"}
    user_id=result["id"]
    password_hash=result["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_user(user_id):
    sql = """SELECT id, username, role
    FROM users
    WHERE id=?"""
    result= db.query(sql, [user_id])
    return result[0] if result else None

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def remove_image(user_id):
    sql="UPDATE users SET image = NULL WHERE id = ?"
    db.execute(sql, [user_id])

def get_image(user_id):
    sql="SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0]["image"] if result else None #👉 Returns: bytes

#👉 db.query() returns a list of rows
#Each row behaves like a dictionary.



def get_all_users():
    sql = "SELECT id, username FROM users"
    return db.query(sql)

def get_coaches():
    sql = """SELECT id, username, role FROM users
             WHERE role="coach" OR role="admin" """
    return db.query(sql)

def get_items(user_id):
    sql = """SELECT id,
    title,
    training_type,
    training_level,
    training_date,
    training_time
    FROM items
    WHERE coach_id=?
    ORDER BY id DESC"""
    return db.query(sql, [user_id]) 

