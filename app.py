from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import SECRET
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbbb.db'
db = SQLAlchemy(app)


class User(db.Model):
    '''Эта таблица будет содержать четыре столбца:
    id: уникальный идентификатор пользователя, который автоматически инкрементируется при добавлении новых записей в таблицу.
    username: имя пользователя, которое является обязательным и должно быть уникальным.
    password: пароль пользователя, который также является обязательным.
    date_create: дата создания профиля'''
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    '''
    Эта таблица будет содержать следующие столбцы:
    id: уникальный идентификатор записи, который автоматически инкрементируется при добавлении новых записей в таблицу.
    title: заголовок записи, который также является обязательным.
    description: описание записи, которое также является обязательным.
    date_posted: дата и время создания записи, которые также являются обязательными.
    user_id: связь между таблицами'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(128), db.ForeignKey('user.login'), nullable=False)


@app.before_first_request
def create_database():
    db.create_all()


@app.route('/list', methods=['GET', 'POST'])
def to_do_list():
    title = request.form.get('title')
    description = request.form.get('description')
    login = request.form.get('login')
    if request.method == 'POST':
        new_post = Post(title=title, description=description,user_id=login)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('to_do_list.html')


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if User.query.filter_by(login=login).first():
            flash('Данный пользователь уже существует', 'success')
        elif login.count('@') > 1 \
                and login[0] == '@' \
                and login.count('.') <= 0 \
                and len(login) < 4 \
                and password != password2 \
                and len(password) < 5:
            flash('Проверьте корректность введенных данных', 'error')
        elif password != password2:
            flash('Пароли не совпадают', 'error')
        else:
            pswd_hash = generate_password_hash(password)
            if check_password_hash(pswd_hash, password):
                new_user = User(login=login, password=pswd_hash)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('authoriz'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def authoriz():
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        if User.query.filter_by(login=login).first() is None \
                and User.query.filter_by(password=password).first() is None:
            flash('Пользователь не существует', 'error')
        elif User.query.filter_by(login=login).first() is None:
            flash('Введите логин', 'error')
        elif User.query.filter_by(password=password).first() is None:
            flash('Не верный пароль', 'error')
        else:
            redirect(url_for('to_do_list'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
