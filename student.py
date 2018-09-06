from flask import render_template, request, redirect, url_for, session
import json
from models import Student, Question, Score, Teacher, Quiz, db, app


@app.route("/student_index")
def student_index():
    if 'username' in session:
        student_name = session['username']
        quizes = Quiz.query.all()
        student = Student.query.filter_by(username=student_name).first()
        attempted_quizes = Score.query.filter_by(student_id=student.id)
        attempted_quizes_list = list()
        unattempted_quizes_list = list()
        for quiz in quizes:
            is_attempted = Score.query.filter_by(quiz_id=quiz.id, student_id=student.id).first()
            if is_attempted is not None:
                attempted_quizes_list.append(quiz)
            else:
                unattempted_quizes_list.append(quiz)
        if len(attempted_quizes_list) == 0:
            quizes_data = {'attempted_quizes': None, 'unattempted_quizes': unattempted_quizes_list}
            return render_template("student_index.html", quizes=quizes_data)
        if len(unattempted_quizes_list) == 0:
            quizes_data = {'attempted_quizes': attempted_quizes_list, 'unattempted_quizes': None}
            return render_template("student_index.html", quizes=quizes_data)
        if len(attempted_quizes_list) == 0 and len(unattempted_quizes_list) == 0:
            quizes_data = {'attempted_quizes': None, 'unattempted_quizes': None}
            return render_template("student_index.html", quizes=quizes_data)
        else:
            quizes_data = {'attempted_quizes': attempted_quizes_list, 'unattempted_quizes': unattempted_quizes_list}
            return render_template("student_index.html", quizes=quizes_data)
    else:
        return redirect(url_for('index'))


@app.route('/get_marks', methods=['GET', 'POST'])
def get_marks():
    quiz_id = request.form.get("quiz_id")
    quiz_marks = Score.query.filter_by(quiz_id=quiz_id).first()
    return "YOUR MARKS ARE " + str(quiz_marks.marks)


@app.route('/start_quiz/<int:quiz_id>/<string:student_username>', methods=['GET', 'POST'])
def start_quiz(quiz_id, student_username):
    questions = Question.query.filter_by(quiz_id=quiz_id)
    no_of_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    if no_of_questions == 0:
        quiz_data = {'questions': None, 'student_username': student_username}
        return render_template("attempt_quiz.html", quiz_data=quiz_data)
    else:
        quiz_data = {'questions': questions, 'student_username': student_username}
        return render_template("attempt_quiz.html", quiz_data=quiz_data)


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    username = request.form["username"]
    score = 0
    quiz_solution = list()
    quiz_id = request.form["quiz_id"]
    questions = Question.query.filter_by(quiz_id=quiz_id)
    for question in questions:
        selected_ans = request.form['option'+str(question.id)]
        correct_ans = question.correct_ans
        if correct_ans == "A":
            correct_ans = question.option_a
        if correct_ans == "B":
            correct_ans = question.option_b
        if correct_ans == "C":
            correct_ans = question.option_c
        if correct_ans == "D":
            correct_ans = question.option_d
        if correct_ans == selected_ans:
            score += 1
        question_solution = {'question_statement': question.statement,
                             'correct_ans': correct_ans, 'selected_ans': selected_ans}
        quiz_solution.append(question_solution)
    result = {'score': score, 'solution': quiz_solution, 'username': username, 'quiz_id': quiz_id}
    return render_template("result.html", result=result)


@app.route('/save_marks/<username>/<score>/<quiz_id>')
def save_marks(username, score, quiz_id):
    student = Student.query.filter_by(username=username).first()
    score = Score(student_id=student.id, marks=score, quiz_id=quiz_id)
    db.session.add(score)
    db.session.commit()
    return redirect(url_for("student_index"))


@app.route('/attempt_quiz', methods=['GET', 'POST'])
def attempt_quiz():
    return render_template("attempt_quiz.html")


@app.route('/get_student', methods=['GET', 'POST'])
def get_student():
    student_id = request.form.get('student_id')
    student = Student.query.filter_by(id=student_id).first()
    student_info = {'username': student.username, 'id': student.id, 'password': student.password}
    return json.dumps(student_info)


@app.route('/get_teacher', methods=['GET', 'POST'])
def get_teacher():
    teacher_id = request.form.get('teacher_id')
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    teacher_info = {'username': teacher.username, 'id': teacher.id, 'password': teacher.password}
    return json.dumps(teacher_info)
