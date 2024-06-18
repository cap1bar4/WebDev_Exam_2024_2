from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Book, Genre, Cover, Comment
from tools import ImageSaver
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from markdown2 import markdown
from auth import checkRole
import bleach
import os

from configure import UPLOAD_FOLDER

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'blockquote', 'code', 'pre']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title']
}

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/create_book', methods=['GET', 'POST'])
@login_required
@checkRole('create') 
def create_book():
    book = Book()
    genres = db.session.execute(db.select(Genre)).scalars() 

    if request.method == "POST":
        title = request.form.get('name')
        description_md = request.form.get('short_desc')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        pages = request.form.get('pages')
        file = request.files.get('book_cover')
        genre_ids = request.form.getlist('genres')
        print('file', file)
        

        print("Received file:", file)
        if file:
            print("File name:", file.filename)
        else:
            print("File not received. Request files:", request.files)
        
        book = Book ( # создаем объект книги с полученными данными
            title=title,
            description=bleach.clean(markdown(description_md), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES), # чистка от опасных тегов
            year=year,
            publisher=publisher,
            author=author,
            pages=pages
        )

        book.genres = db.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()  # Связываем жанры с книгой
        
        try:
            img = None
            if file and file.filename:
                print('File exists, attempting to save')
                img = ImageSaver(file).save()
                print('Image saved with id:', img.id)
                book.cover_id = img.id
            if not img:
                raise ValueError("Обложка книги обязательна")
            
           
            
            db.session.add(book)
            db.session.commit()
            
            flash(f'Книга {book.title} была успешно добавлена!', 'success')
            return redirect(url_for('book.create_book'))
        
        except IntegrityError as err:
            flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
            db.session.rollback()
    
    return render_template('books/create_book.html', book=book, current_user=current_user, genres=genres)


@bp.route('/view_book/<int:book_id>', methods=['GET'])
@login_required
@checkRole('show')
def view_book(book_id):
    
    book = db.session.query(Book).filter_by(id=book_id).first()
    cover = db.session.query(Cover).filter_by(id=book.cover_id).first()
    user_review = db.session.query(Comment).filter_by(book_id=book_id, user_id=current_user.id).first()

    if not book:
        flash('Книга не найдена', 'danger')
        return redirect(url_for('index'))
    
    comments = db.session.query(Comment).filter_by(book_id=book_id).all()


    return render_template('books/viewing.html', book=book, comments=comments, cover=cover,  user_review=user_review)

@bp.route('/add_view/<int:book_id>',  methods=['GET', 'POST'])
@login_required
@checkRole('show')
def add_view(book_id):

    book = db.session.query(Book).filter_by(id=book_id).first()

    if request.method == "POST":
        rating = request.form.get('rating')
        review_text = request.form.get('text_review')
        
        comments = Comment( 
            book_id=book_id,
            user_id=current_user.id,
            rating=rating,
            text=bleach.clean(markdown(review_text), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES), # чистка от опасных тегов
        )

        db.session.add(comments)
        db.session.commit()

        flash(f'Рецензия успешно добавлена!', 'success')

        return redirect(url_for('book.view_book', book_id=book.id))

    
    return render_template('books/review_form.html', book=book)



@bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
@checkRole('edit')
def edit_book(book_id): # получаем книгу по идентификатору
    book = db.session.query(Book).filter_by(id=book_id).first()
    genres = db.session.execute(db.select(Genre)).scalars()
    
    if request.method == "POST":
        title = request.form.get('name')
        description_md = bleach.clean(markdown(request.form.get('short_desc')), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        pages = request.form.get('pages')
        genre_ids = request.form.getlist('genres')
        
        book.title = title
        book.description = description_md
        book.publisher = publisher
        book.author = author
        book.pages = pages
        book.year = year

        # Очистка предыдущих связей
        book.genres = []

        # Добавление новых связей
        new_genres = db.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        book.genres.extend(new_genres)

        try:
            db.session.add(book)
            db.session.commit()
            flash(f'Книга {book.title} была успешно обновлена!', 'success')
            return redirect(url_for('book.edit_book', book_id=book.id))
        
        except IntegrityError as err:
            flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
            db.session.rollback()
    
    return render_template('books/edit_book.html', book=book, current_user=current_user, genres=genres)

# Маршрут для удаления книги
@bp.route('/delete_book', methods=['POST'])
@login_required
@checkRole('delete')
def delete_book():
    book_id = request.form.get('book_id')
    book = db.session.query(Book).filter_by(id=book_id).first()
    if book:
        # Удаление файла обложки из файловой системы
        cover = db.session.query(Cover).filter_by(id=book.cover_id).first()
        if cover:
            try:
                # Формирование полного пути к файлу обложки
                
                file_path = os.path.join(UPLOAD_FOLDER, cover.md5_hash + '.' + cover.filename.split('.')[-1])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                else:
                    flash(f'Файл обложки id = {cover.id} не найден: {file_path}', 'warning')
            except Exception as e:
                flash(f'Не удалось удалить файл обложки id = {cover.id}: {e}', 'danger')
        else:
            flash(f'Обложка для книги id = {book.id} не найдена: {e}', 'warning')
        db.session.delete(book)
        db.session.commit()
        flash(f'Книга {book.title} была успешно удалена!', 'success')
    else:
        flash('Книга не найдена', 'danger')
    return redirect(url_for('index'))
