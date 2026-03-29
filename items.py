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