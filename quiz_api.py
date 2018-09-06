from flask import render_template, request, redirect, url_for, session
import json
from models import Student, Teacher, Quiz, Question, Score, app


@app.route("/api/teacher/id/<int:id>")
@app.route("/api/teacher/username/<string:username>")
def get_teacher_data(id=None,username=None):
    if id is None:
        teacher = Teacher.query.filter_by(username=username).first()
    if username is None:
        teacher = Teacher.query.filter_by(id=id).first()
    if teacher is None:
        return "Nothing is found!"
    else:
        teacher_data = dict({'id': teacher.id, 'Name': teacher.username, 'Password': teacher.password})
    return json.dumps(teacher_data)


@app.route("/api/student/id/<int:id>")
@app.route("/api/student/username/<string:username>")
def get_student_data(id=None,username=None):
    if id is None:
        student = Student.query.filter_by(username=username).first()
    if username is None:
        student = Student.query.filter_by(id=id).first()
    if student is None:
        return "Nothing is found!"
    else:
        student_data = dict({'id': student.id, 'Name': student.username, 'Password': student.password})
    return json.dumps(student_data)


@app.route("/api/quiz/id/<int:id>", methods=['Get'])
@app.route("/api/quiz/name/<string:name>", methods=['Get'])
def get_quiz_detail(id=None, name=None):
    if name is None:
        quiz = Quiz.query.filter_by(id=id).first()
    if id is None:
        quiz = Quiz.query.filter_by(name=name).first()
    if quiz is None:
        return "Nothing is found!"
    else:
        questions = Question.query.filter_by(quiz_id=quiz.id)
        if questions is None:
            return "this quiz has no question"
        else:
            question_list = list()
            for question in questions:
                question_list.append(dict({'id': question.id, 'statement': question.statement,
                                           'correct_answer': question.correct_ans,
                                           'Option_A': question.option_a, 'Option_B': question.option_b,
                                           'Option_C': question.option_c, 'Option_D': question.option_d,
                                           'quiz_id': quiz.id, 'quiz_name': quiz.name}))
            return json.dumps(question_list)


@app.route("/api/marks/id/<int:id>")
@app.route("/api/marks/username/<string:username>")
def get_student_score(id=None, username=None):
    if username is None:
        student = Student.query.filter_by(id=id).first()
    if id is None:
        student = Student.query.filter_by(username=username).first()
    if student is None:
        return "Nothing Found!"
    else:
        scores = Score.query.filter_by(student_id=student.id)
        if scores is None:
            return "no quiz attempted yet"
        else:
            marks = list()
            for score in scores:
                quiz = Quiz.query.filter_by(id=score.quiz_id).first()
                marks.append(dict({'id': student.id, 'Name': student.username,
                                   'score': score.marks, 'quiz_name': quiz.name}))
            return json.dumps(marks)
