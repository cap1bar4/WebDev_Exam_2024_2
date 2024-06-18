from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models import db, Cover, Book, Genre, Comment, book_genre_table
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.sql import func
from flask_migrate import Migrate
from auth import bp as auth_bp, init_login_manager
from tools import ImageSaver 
from sqlalchemy import and_
import os

app = Flask(__name__)

app.config.from_pyfile('configure.py')

db.init_app(app)
migrate = Migrate(app, db)

init_login_manager(app)

from auth import bp as bp_auth
from books_func import bp as bp_books

app.register_blueprint(bp_auth)
app.register_blueprint(bp_books)

@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(err):
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    return f'{error_msg} (Подробнее: {err})', 500

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    genres_names = []
    year_arr = []

    books_with_genres = []

    if request.method == "POST":
        books_query = db.session.query(Book)
        year_arr = [book.year for book in books_query]

        title = request.form.get('name')
        if title:
            books_query = books_query.filter(Book.title.ilike(f"%{title}%"))

        yearlist = request.form.getlist('year')
        if yearlist:
            books_query = books_query.filter(Book.year.in_(yearlist))
        
        publisher = request.form.get('publisher')
        if publisher:
            books_query = books_query.filter(Book.publisher.ilike(f"%{publisher}%"))
        
        author = request.form.get('author')
        if author:
            books_query = books_query.filter(Book.author.ilike(f"%{author}%"))
        
        pages_one = request.form.get('pages_one')
        pages_two = request.form.get('pages_two')
        print(pages_one, pages_two, "Errrrrrrrr")
        if pages_one and pages_two:
            books_query = books_query.filter(and_(Book.pages >= pages_one, Book.pages <= pages_two))
        elif pages_one:
            books_query = books_query.filter(Book.pages >= pages_one)
        elif pages_two:
            books_query = books_query.filter(Book.pages <= pages_two)

        genrelist = request.form.getlist('genres')
        if genrelist:
            genre_ids = db.session.query(Genre.id).filter(Genre.name.in_(genrelist)).all()
            genre_ids = [id for id, in genre_ids]
            if genre_ids:
                books_query = books_query.join(book_genre_table).filter(book_genre_table.c.genre_id.in_(genre_ids))

        books = books_query.paginate(page=page, per_page=per_page)

    else:
        books_query = db.session.query(Book).order_by(Book.year.desc())
        
        if request.args:
            title = request.args.get('name')
            if title:
                books_query = books_query.filter(Book.title.ilike(f"%{title}%"))
            yearlist = request.args.getlist('year')
            if yearlist:
                books_query = books_query.filter(Book.year.in_(yearlist))
            publisher = request.args.get('publisher')
            if publisher:
                books_query = books_query.filter(Book.publisher.ilike(f"%{publisher}%"))
            author = request.args.get('author')
            if author:
                books_query = books_query.filter(Book.author.ilike(f"%{author}%"))
            pages = request.args.get('pages')
            if pages:
                books_query = books_query.filter(Book.pages == pages)
            genrelist = request.args.getlist('genres')
            if genrelist:
                genre_ids = db.session.query(Genre.id).filter(Genre.name.in_(genrelist)).all()
                genre_ids = [id for id, in genre_ids]
                if genre_ids:
                    books_query = books_query.join(book_genre_table).filter(book_genre_table.c.genre_id.in_(genre_ids))

        books = books_query.paginate(page=page, per_page=per_page)

    genres_arr = db.session.execute(db.select(Genre)).scalars().all()
    genres_names = [genre.name for genre in genres_arr]

    for book in books.items:
        average_rating = db.session.query(func.avg(Comment.rating)).filter(Comment.book_id == book.id).scalar()
        review_count = db.session.query(func.count(Comment.id)).filter(Comment.book_id == book.id).scalar()
        genres = [genre.name for genre in book.genres]
        if request.method != "POST":
            year_arr.append(book.year)
        
        books_with_genres.append({
            'id': book.id,
            'title': book.title,
            'year': book.year,
            'genres': genres,
            'average_rating': average_rating or 0,
            'review_count': review_count or 0
        })

    print(year_arr, "Hello")

    return render_template('index.html', books=books_with_genres, pagination_book=books, genres_arr=genres_names, year_arr=sorted(set(year_arr)))

@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Cover, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], img.storage_filename)