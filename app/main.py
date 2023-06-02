from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bancogeral.sqlite3"
app.config["SECRET_KEY"] = "secret"

login_manager = LoginManager(app)

db = SQLAlchemy(app)

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

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