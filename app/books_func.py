from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Book, Genre, Cover
from tools import ImageSaver
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from markdown2 import markdown
import bleach
import os

from configure import UPLOAD_FOLDER

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    book = Book()
    genres = db.session.execute(db.select(Genre)).scalars() # scalar / scalars

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
            description=bleach.clean(markdown(description_md)),
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
            if not img:
                raise ValueError("Обложка книги обязательна")
            
            book.cover_id = img.id
            
            db.session.add(book)
            db.session.commit()
            
            flash(f'Книга {book.title} была успешно добавлена!', 'success')
            return redirect(url_for('book.create_book'))
        
        except IntegrityError as err:
            flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
            db.session.rollback()
    
    return render_template('books/create_book.html', book=book, current_user=current_user, genres=genres)

@bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id): # получаем книгу по идентификатору
    book = db.session.query(Book).filter_by(id=book_id).first()
    genres = db.session.execute(db.select(Genre)).scalars()
    
    if request.method == "POST":
        title = request.form.get('name')
        description_md = bleach.clean(markdown(request.form.get('short_desc')))
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