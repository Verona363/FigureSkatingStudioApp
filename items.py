import db

def get_all_classes():
    sql="SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes={}
    for title, value in result:
        classes[title]=[]
    for title, value in result:
        classes[title].append(value)

    return classes



def add_item(title, training_type, specialization, format, training_level, coach_id, training_date, training_time, training_description, user_id):
    sql = """INSERT INTO items
    (title, training_type, specialization, format, training_level, coach_id, training_date, training_time, training_description, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [
        title, training_type, specialization, format,
        training_level, coach_id, training_date, training_time,
        training_description, user_id
    ])

def add_booking(item_id, user_id):
#order of parameters(user_id, item_id) must be the same as in app.py
    sql = """INSERT INTO participants
    (item_id, user_id)
    VALUES (?, ?)"""
    db.execute(sql, [item_id, user_id])
#INSERT INTO participants (item_id, user_id)
##the column names must match the column names defined in table in schema.sql
#VALUES (?, ?)
#👉 Python must pass values in that exact order:
#db.execute(sql, [item_id, user_id])

def cancel_booking(item_id, user_id):
#order of parameters(user_id, item_id) must be the same as in app.py
    sql = """DELETE FROM participants
    WHERE item_id=? AND user_id=?"""
    db.execute(sql, [item_id, user_id])

def get_participants(item_id):
    sql="""SELECT users.id as user_id, users.username
    FROM participants, users 
    WHERE participants.user_id=users.id AND
    participants.item_id=?
    ORDER BY participants.id DESC"""
    return db.query(sql, [item_id])

def is_booked(item_id, user_id):
    sql = """
    SELECT 1 FROM participants
    WHERE item_id = ? AND user_id = ?
    LIMIT 1
    """
    result = db.query(sql, [item_id, user_id])
    return len(result) > 0
#“Is this user already booked for this training?”
#Returns:
#True → user is booked
#False → user is not booked
#LATER can write  return bool(db.query(sql, [item_id, user_id]))

def get_bookings(user_id):
    sql=""" SELECT participants.item_id, items.title, 
    items.training_date, items.training_time, items.training_level,
    items.coach_id, users.username
    FROM participants, items, users
    WHERE items.id=participants.item_id AND items.coach_id=users.id 
    AND participants.user_id=?"""
    return db.query(sql, [user_id])

def get_items():
    sql = """SELECT items.id, items.title, items.training_date, 
    items.training_time, items.training_level, items.coach_id, users.username
    FROM items, users
    WHERE items.coach_id=users.id
    ORDER BY items.id DESC"""
    return db.query(sql)


#new function
def get_item(item_id):
    sql = """ SELECT items.id,
    items.title,
    items.training_type,
    items.specialization,
    items.format,
    items.training_level,
    items.training_date,
    items.training_time,
    items.training_description,

    creator.id AS user_id,
    creator.username AS creator_name,


    coach.id AS coach_id,
    coach.username AS coach_name

    FROM items
    JOIN users AS creator ON items.user_id= creator.id
    JOIN users AS coach ON items.coach_id = coach.id
    WHERE items.id=? """
    result= db.query(sql, [item_id])
    return result[0] if result else None
#Explanation about roles, same table "users" used twice
#    creator.id AS user_id,
#    creator.username AS creator_name,

    #  later I'm joining users as creator,
    #  so creator.id originally was users.id
    #  creator.username originally was users.username


# example result from this query is
#{
#  "id": 10,
#  "title": "Spins",
#
#  "user_id": 1,
#  "creator_name": "main_coach",
#
#  "coach_id": 2,
#  "coach_name": "anna"
#}

   
    #db.query() returns a list of dictionaries, where:
    #List = all rows returned by the SQL query
    #Dictionary = one row (column → value)
    #[row1_dict,
    #row2_dict,
    #row3_dict]
    #results = db.query(sql, [item_id]) might return
#    [
#   {
#        "id": 1,
#        "title": "Python Basics",
#        "username": "johndoe"
#    } 
#]
#What [0] does: give me first row from the result list
#{ "id": 1, "title": "Python Basics" }




def update_item(item_id, title, training_type, specialization, format, training_level, coach_id, training_date, training_time, training_description):
    sql = """UPDATE items SET title=?,
                        training_type=?,
                        specialization=?,
                        format=?,
                        training_level=?,
                        coach_id=?,
                        training_date=?,
                        training_time=?,
                        training_description=?
                        where id = ?"""
    db.execute(sql, [title, training_type, specialization, format,
        training_level, coach_id, training_date, training_time,
        training_description, item_id])
    #The db.execute function runs the query and replaces the ? placeholders
    # with the actual values passed in the list.
    #The last value in the list is item_id, which tells the database which record to update.

    #The order of the values in the list for "db.execute "" must match the order of the ? placeholders in the SQL query exactly.
    #There is 1 ? placeholder in the WHERE clause → for the item_id.
    
def remove_item(item_id):
    sql="DELETE FROM participants WHERE item_id=?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items where id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """
    SELECT id, title
    FROM items
    WHERE 
        title LIKE ? OR
        training_type LIKE ? OR
        specialization LIKE ? OR
        format LIKE ? OR
        training_level LIKE ? OR
        coach_id LIKE ? OR
        training_date LIKE ? OR
        training_time LIKE ? OR
        training_description LIKE ?
    ORDER BY id DESC
    """

    like = "%" + query + "%"
    #SQL LIKE needs wildcards (%), and query alone does NOT have them.
    #without % title LIKE 'python"---This only matches exactly "python"
    #% % allow to search anywhere in the text

    return db.query(sql, [like] * 9)
    # It creates a list that repeats the same value 9 times.
    #like=jumps

