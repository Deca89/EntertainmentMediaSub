import db

def add_item(title, link, media_type, descriptions, user_id):
    sql = """INSERT INTO items (title, link, media_type, descriptions, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, link, media_type, descriptions, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.link,
                    items.media_type,
                    items.descriptions,
                    users.id user_id,
                    users.username
             FROM  items, users
             WHERE items.user_id = users.id AND
                   items.id =?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, link, media_type, descriptions):
    sql = """UPDATE items SET title = ?,
                              link = ?,
                              media_type = ?,
                              descriptions = ?
                           WHERE id = ?"""
    db.execute(sql, [title, link, media_type, descriptions, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query, media_type):
    sql = """ SELECT id, title
              FROM items
              WHERE (title LIKE ? OR descriptions LIKE ?)
                AND media_type LIKE ?
              ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%", media_type])

def find_items_word(query):
    sql = """ SELECT id, title
              FROM items
              WHERE title LIKE ? OR descriptions LIKE ?
              ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
    

def find_items_genre(media_type):
    sql = """ SELECT id, title
              FROM items
              WHERE media_type = ?
              ORDER BY id DESC"""
    return db.query(sql, [media_type])

