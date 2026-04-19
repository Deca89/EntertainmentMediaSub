import db

def add_item(title, link, descriptions, user_id, classes):
    sql = """INSERT INTO items (title, link, descriptions, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, link, descriptions, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.link,
                    items.descriptions,
                    users.id user_id,
                    users.username
             FROM  items, users
             WHERE items.user_id = users.id AND
                   items.id =?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, link, descriptions, classes):
    sql = """UPDATE items SET title = ?,
                              link = ?,
                              descriptions = ?
                           WHERE id = ?"""
    db.execute(sql, [title, link, descriptions, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    sql = "DELETE FROM comments WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items_word(query):
    sql = """ SELECT id, title
              FROM items
              WHERE title LIKE ? OR descriptions LIKE ?
              ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def get_user_items(user_id):
    sql = "SELECT id, title FROM items WHERE user_id = ? ORDER BY id DESC"
    result = db.query(sql, [user_id])
    return result if result else []

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def add_comment(item_id, user_id, comment):
    sql = """INSERT INTO comments (item_id, user_id, comment)
             VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """SELECT comments.comment, users.id user_id, users.username
             FROM comments, users
             WHERE comments.item_id = ? AND comments.user_id = users.id
             ORDER BY comments.id ASC"""
    return db.query(sql, [item_id])