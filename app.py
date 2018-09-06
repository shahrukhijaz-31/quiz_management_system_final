from flask import Flask, render_template, request, redirect, url_for, session
import json,admin,teacher,student,quiz_api
from models import Student, Teacher, db, app


db.create_all()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['type']
    if user_type == 'Teacher':
        user = Teacher.query.filter_by(username=username).first()
        if user is None:
            return "incorrect username"
        else:
            if user.password == password:
                session['username'] = username
                session['id'] = user.id
                return redirect(url_for('teacher_index'))
            else:
                return "incorrect password"
    if user_type == 'Admin':
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))
    else:
        user = Student.query.filter_by(username=username).first()
        if user is None:
            return "incorrect username"
        else:
            if user.password == password:
                session['username'] = username
                session['id'] = user.id
                return redirect(url_for('student_index'))
            else:
                return "incorrect password"


@app.route("/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
