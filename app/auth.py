from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from functools import wraps
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id): # функция загрузки пользователя из бд по ID
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    return user

def checkRole(action):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            user = None
            if user_id:
                user = load_user(user_id)
            if current_user.can(action,record=user):
                return f(*args, **kwargs)
            flash("У вас нет доступа к этой странице", "danger")
            return redirect(url_for("index"))
        return wrapper
    return decorator


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        
        if login and password:
            user = db.session.query(User).filter_by(username=username).first()
            print(generate_password_hash(password), "1001")
            print(user.password_hash, "1002")
            if user:
                if check_password_hash(user.password_hash, password):
                    login_user(user)
                    flash('Вы успешно аутентифицированы.', 'success')
                    next = request.args.get('next')
                    return redirect(next or url_for('index'))
                else:
                    flash('Невозможно аутентифицироваться с указанными логином и паролем.', 'danger')
            else:
                flash('Пользователь не найден.', 'danger')
                
       
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required # декоратор указывающий на то, что маршрут доступен только аутентифицированным
def logout():
    logout_user()
    return redirect(url_for('index'))
