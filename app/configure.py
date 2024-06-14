import os

SECRET_KEY = 'b3baa1cb519a5651c472d1afa1b3f4e04f1adf6909dae88a4cd39adc0ddd9732'

MYSQL_USER = 'std_2413_exam'
MYSQL_PASSWORD = 'password1'
MYSQL_HOST = 'std-mysql'
MYSQL_DATABASE = 'std_2413_exam'

#  строка подключения к бд с параметрами
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False # отключение отслеживания изменений объектов sqlalchemy
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
