from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models import db, Cover, Book, Genre, Comment, book_genre_table
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.sql import func
from flask_migrate import Migrate
from auth import bp as auth_bp, init_login_manager
from tools import ImageSaver
import os

app = Flask(__name__)
# application = app

app.config.from_pyfile('configure.py') # качаем конфиг

db.init_app(app)
migrate = Migrate(app, db) # соединяем app и базу данных

init_login_manager(app) # инициализируем Login manager из auth.py

from auth import bp as bp_auth  #  bp_auth и bp_books переменные которые после будут зарегистрированы в app
from books_func import bp as bp_books

app.register_blueprint(bp_auth)
app.register_blueprint(bp_books)

@app.errorhandler(SQLAlchemyError) # ловит ошибки в sql алхимии
def handle_sqlalchemy_error(err):
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    return f'{error_msg} (Подробнее: {err})', 500

@app.route('/') # декоратор
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    # books = db.session.query(Book).order_by(Book.year.desc()).all()
    books = db.session.query(Book).order_by(Book.year.desc()).paginate(page=page, per_page=per_page)
    books_with_genres = []
    for book in books:
        average_rating = db.session.query(func.avg(Comment.rating)).filter(Comment.book_id == book.id).scalar()
        review_count = db.session.query(func.count(Comment.id)).filter(Comment.book_id == book.id).scalar()
        genres = [genre.name for genre in book.genres]
        books_with_genres.append({
            'id': book.id,
            'title': book.title,
            'year': book.year,
            'genres': genres,
            'average_rating': average_rating or 0,
            'review_count': review_count or 0
        })
    return render_template('index.html', books=books_with_genres, pagination_book=books)

@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Cover, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], img.storage_filename)

