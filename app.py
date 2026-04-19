import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import items

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    if not username:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not password1:
        return render_template("register.html", error="VIRHE: Salasana ei voi olal tyhjä")
    if password1 != password2:
        return render_template("register.html", error="VIRHE: Salasanat eivät ole samat")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error="VIRHE: tunnus on jo varattu")

    return render_template("register.html", message="Tunnus luotu")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])
        
        if not result:
            return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")
        
        result = result[0]

        user_id = result["id"]
        password_hash = result["password_hash"]
        

        if not check_password_hash(password_hash, password):
            return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")
        else:
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    link = request.form["link"]
    media_type = request.form["media_type"]
    descriptions = request.form["descriptions"]
    if not descriptions or len(descriptions) > 1000:
        abort(403)
    user_id = session["user_id"]

    items.add_item(title, link, media_type, descriptions, user_id)

    flash("Kohde luotu onnistuneesti")
    return redirect("/")

@app.route("/item/<int:item_id>")
def show_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            flash("Kohde poistettu onnistuneesti")
            return redirect("/")
        else:
            flash("Kohdetta ei poistettu")
            return redirect("/item/" + str(item_id))


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    link = request.form["link"]
    media_type = request.form["media_type"]
    descriptions = request.form["descriptions"]
    if not descriptions or len(descriptions) > 1000:
        abort(403)
    user_id = session["user_id"]

    items.update_item(item_id, title, link, media_type, descriptions)

    flash("Kohde päivitetty onnistuneesti")
    return redirect("/item/" + str(item_id))

@app.route("/find_item")
def find_item():
    require_login()
    query = request.args.get("query")
    media_type = request.args.get("media_type")
    if query and media_type:
        results = items.find_items(query, media_type)
    elif query:
        media_type = ""
        results = items.find_items_word(query)
    elif media_type:
        query = ""
        results = items.find_items_genre(media_type)
    else:
        query = ""
        media_type = ""
        results = []
    print(query) # tyhjä tai syöte
    print(media_type) # None tai numero
    return render_template("find_item.html", query=query, media_type=media_type, results=results)