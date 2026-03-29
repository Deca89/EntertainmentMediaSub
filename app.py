import sqlite3
from flask import Flask
from flask import redirect, render_template, request, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register.html", error="VIRHE: salasanat eivät ole samat")
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

        result = db.query("SELECT password_hash FROM users WHERE username = ?", [username])
        
        if not result:
            return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")

        password_hash = result[0][0]

        if not check_password_hash(password_hash, password):
            return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")
        else:
            session["username"] = username
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")