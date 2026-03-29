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
    sql = """SELECT items.title,
    items.training_type,
    items.specialization,
    items.format,
    items.training_level,
    items.coach,
    items.training_date,
    items.training_time,
    items.training_description,
    users.username

    FROM items, users
    WHERE items.user_id=users.id AND
    items.id=?"""
    return db.query(sql, [item_id]) [0]