import db

def add_item(title, link, media_type, descriptions, user_id):
    sql = """INSERT INTO items (title, link, media_type, descriptions, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, link, media_type, descriptions, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
                    items.link,
                    items.media_type,
                    items.descriptions,
                    users.username
             FROM  items, users
             WHERE items.user_id = users.id AND
                   items.id =?"""
    return db.query(sql, [item_id])[0]