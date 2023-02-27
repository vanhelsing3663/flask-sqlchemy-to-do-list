from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import SECRET
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
