from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    score = db.relationship('Score', backref='Quiz', lazy=True)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    quizes = db.relationship('Quiz', backref='Teacher', lazy='dynamic')

    def __init__(self, username, password):
        self.password = password
        self.username = username


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)

    def __init__(self, name, teacher_id):
        self.name = name
        self.teacher_id = teacher_id


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correct_ans = db.Column(db.String(3), nullable=False)
    statement = db.Column(db.String(80), nullable=False)
    option_a = db.Column(db.String(80), nullable=False)
    option_b = db.Column(db.String(80), nullable=False)
    option_c = db.Column(db.String(80), nullable=False)
    option_d = db.Column(db.String(80), nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'),
                        nullable=False)
