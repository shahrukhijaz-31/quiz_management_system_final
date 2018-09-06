from flask import render_template, request, redirect, url_for
from models import Teacher, Student, Score, Quiz, app, db


@app.route('/admin')
def admin():
    if 'username' is None:
        return redirect(url_for("index"))
    teachers = Teacher.query.all()
    students = Student.query.all()
    user_data = {'students': students, 'teachers': teachers}
    return render_template("admin.html", user_data=user_data)


@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    student_quiz_scores = Score.query.filter_by(student_id=student.id).all()
    for student_score in student_quiz_scores:
        db.session.delete(student_score)
        db.session.commit()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/delete_teacher/<teacher_id>')
def delete_teacher(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    # quizes_of_teacher = Quiz.query.filter_by(teacher_id=teacher.id)
    for quiz in Quiz.query.filter_by(teacher_id=teacher.id):
        db.session.delete(quiz)
        db.session.commit()
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/update_teacher', methods=['POST', 'GET'])
def update_teacher():
    teacher_id = request.form['t_id']
    teacher_username = request.form['t_username']
    teacher_password = request.form['t_password']

    teacher = Teacher.query.filter_by(id=teacher_id).first()
    teacher.username = teacher_username
    teacher.password = teacher_password
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/update_student', methods=['POST', 'GET'])
def update_student():
    student_id = request.form['s_id']
    student_username = request.form['s_username']
    student_password = request.form['s_password']

    student = Student.query.filter_by(id=student_id).first()
    student.username = student_username
    student.password = student_password
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/insert_teacher", methods=['POST'])
def insert_teacher():
    name = request.form["teacher_name"]
    password = request.form["teacher_password"]
    teacher = Teacher.query.filter_by(username=name).first()
    if teacher is None:
        teacher = Teacher(username=name, password=password)
        db.session.add(teacher)
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for("admin"))
    else:
        return "404 Duplicate Name Error!"


@app.route("/insert_student", methods=['POST'])
def insert_student():
    name = request.form["student_name"]
    password = request.form["student_password"]
    student = Student.query.filter_by(username=name).first()
    if student is None:
        student = Student(username=name, password=password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("admin"))
    else:
        return "404 Duplicate Name Error!"