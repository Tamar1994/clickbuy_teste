from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import User
from flask_login import login_user, logout_user

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        pwd = request.form["password"]

        user = User(name, email, pwd)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        user = User.query.filter_by(email=email).first()

        print(user)

        if not user or not user.verify_password(pwd):
            return  redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

app.run(debug=True)