from flask import render_template, Blueprint, url_for, request, flash, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, current_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfuly", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("try again idiot", category="error")
        else:
            flash("email wrong", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email olingan", category="error")
        elif len(email) < 4:
            flash("3dan uzunroq qil", category="error")
        elif len(first_name) < 2:
            flash("2tadan uzunroq qil", category="error")
        elif password1 != password2:
            flash("togri yoz", category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("New user created", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
