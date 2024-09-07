from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from flask_login import LoginManager
from flask import Blueprint

db = SQLAlchemy()
DB_NAME = path.join(getcwd(), "instance", "database.db")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "1111"
    # qaysi malumotlar bazasiga ulanishi
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # databasega appni ulash
    db.init_app(app)

    # blueprint
    from .views import views
    from .auth import auth
    from .models import User

    # prefix bu urlda mazil berish masalan:
    # 1) url_prefix="/" bo'lsa / manziligan keyin viewni mazili keladi: http://127.0.0.1:5000/login
    # 2) url_prefix="/auth/" bo'lsa o'sha viewni ichidagi routelar bu ko'rinishda bo'ladi: http://127.0.0.1:5000/auth/login
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # qaysi appda db yaratish uchun ishlatiladi
    with app.app_context():
        # db bor bo'lsa yasamaydi yo'q bo'lsa db yasaydi
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    # appga login managerni ulash
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

