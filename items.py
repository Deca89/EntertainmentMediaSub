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
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, link, media_type, descriptions):
    sql = """UPDATE items SET title = ?,
                              link = ?,
                              media_type = ?,
                              descriptions = ?
                           WHERE id = ?"""
    db.execute(sql, [title, link, media_type, descriptions, item_id])
