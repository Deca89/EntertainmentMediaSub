import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import items
import users
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
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
        return render_template("register.html", error="VIRHE: Salasana ei voi olla tyhjä")
    if password1 != password2:
        return render_template("register.html", error="VIRHE: Salasanat eivät ole samat")
    user_created = users.create_user(username, password1)

    if user_created:
        return render_template("register.html", message="Tunnus luotu")
    else:
        return render_template("register.html", error="VIRHE: tunnus on jo varattu")


@app.route("/user/<int:user_id>")
def show_user(user_id):
    require_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = items.get_user_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)

        if not user_id:
            return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")
        else:
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
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
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()
    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    link = request.form["link"]
    descriptions = request.form["descriptions"]
    if not descriptions or len(descriptions) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()
    print(request.form.getlist("classes"))
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_item(title, link, descriptions, user_id, classes)

    item_id = db.last_insert_id()
    return redirect("/item/" + str(item_id))

@app.route("/item/<int:item_id>")
def show_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    return render_template("show_item.html", item=item, classes=classes, comments=comments)

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    if not comment or len(comment) > 500:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, comment)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item, classes=classes, all_classes=all_classes)

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
        check_csrf()
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
    check_csrf()
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
    descriptions = request.form["descriptions"]
    if not descriptions or len(descriptions) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_item(item_id, title, link, descriptions, classes)

    flash("Kohde päivitetty onnistuneesti")
    return redirect("/item/" + str(item_id))

@app.route("/find_item")
def find_item():
    require_login()
    query = request.args.get("query")
    if query:
        results = items.find_items_word(query)
    else:
        query = ""
        media_type = ""
        results = []
    return render_template("find_item.html", query=query, results=results)