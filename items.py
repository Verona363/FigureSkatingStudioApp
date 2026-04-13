import db
def add_item(title, training_type, specialization, format, training_level, coach, training_date, training_time, training_description, user_id):
    sql = """INSERT INTO items
    (title, training_type, specialization, format, training_level, coach, training_date, training_time, training_description, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [
        title, training_type, specialization, format,
        training_level, coach, training_date, training_time,
        training_description, user_id
    ])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
    items.title,
    items.training_type,
    items.specialization,
    items.format,
    items.training_level,
    items.coach,
    items.training_date,
    items.training_time,
    items.training_description,
    users.id user_id,
    users.username

    FROM items, users
    WHERE items.user_id=users.id AND
    items.id=?"""
    result= db.query(sql, [item_id])
    return result[0] if result else None
    
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




def update_item(item_id, title, training_type, specialization, format, training_level, coach, training_date, training_time, training_description):
    sql = """UPDATE items SET title=?,
                        training_type=?,
                        specialization=?,
                        format=?,
                        training_level=?,
                        coach=?,
                        training_date=?,
                        training_time=?,
                        training_description=?
                        where id = ?"""
    db.execute(sql, [title, training_type, specialization, format,
        training_level, coach, training_date, training_time,
        training_description, item_id])
    #The db.execute function runs the query and replaces the ? placeholders
    # with the actual values passed in the list.
    #The last value in the list is item_id, which tells the database which record to update.

    #The order of the values in the list for "db.execute "" must match the order of the ? placeholders in the SQL query exactly.
    #There is 1 ? placeholder in the WHERE clause → for the item_id.
    
def remove_item(item_id):
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
        coach LIKE ? OR
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