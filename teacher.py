from flask import render_template, request, redirect, url_for, session
import json
from models import Question, Teacher, Quiz, db, app


@app.route("/teacher_index")
def teacher_index():
    if 'username' in session:
        return render_template("teacher_index.html")
    return "You are not logged in <br><a href = '/index'></b>" + \
        "click here to log in</b></a>"


@app.route("/create_quiz")
def create_quiz():
    return render_template("create_quiz.html")


@app.route("/create_quiz_body", methods=['POST', 'GET'])
def create_quiz_body():
    question_number = request.form['question_number']
    quiz_name = request.form['quiz_name']
    question_number = 1 + int(question_number)
    quiz_detail = dict({'quiz_name': quiz_name, 'question_number': question_number})
    return render_template("create_quiz_body.html", quiz_detail=quiz_detail)


@app.route("/save_quiz", methods=['POST', 'GET'])
def save_quiz():
    questions = list()
    question_number = request.form['question_number']
    quiz_name = request.form['quiz_name']
    teacher_name = request.form['teacher_name']
    teacher = Teacher.query.filter_by(username=teacher_name).first()

    quiz = Quiz(name=quiz_name, teacher_id=teacher.id)
    db.session.add(quiz)
    db.session.commit()

    for question_id in range(1, int(question_number)):
        question_statement = request.form['question' + str(question_id)]
        correct_ans = request.form['correct_ans'+str(question_id)]
        options = list()
        options.append(dict({'A': request.form['option_a'+str(question_id)]}))
        options.append(dict({'B': request.form['option_a'+str(question_id)]}))
        options.append(dict({'C': request.form['option_a'+str(question_id)]}))
        options.append(dict({'D': request.form['option_a'+str(question_id)]}))
        quiz = Quiz.query.filter_by(name=quiz_name).first()
        question = Question()
        question.quiz_id = quiz.id
        question.correct_ans = correct_ans
        question.statement = question_statement
        question.option_a = request.form['option_a'+str(question_id)]
        question.option_b = request.form['option_b'+str(question_id)]
        question.option_c = request.form['option_c'+str(question_id)]
        question.option_d = request.form['option_d'+str(question_id)]
        db.session.add(question)
        db.session.commit()

        question = {'question': question_statement, 'correct_ans': correct_ans, 'options': options,
                    'teacher_name': teacher_name, 'quiz_name': quiz_name}
        questions.append(question)
    return redirect(url_for('teacher_index'))


@app.route("/quiz_management", methods=['POST', 'GET'])
@app.route("/quiz_management/<string:username>", methods=['POST', 'GET'])
@app.route("/quiz_management/<int:quiz_id>", methods=['POST', 'GET'])
def quiz_management(username=None, quiz_id=None):
    if username is None and quiz_id is None:
        quiz_id = session['id']
        quizes = Quiz.query.filter_by(teacher_id=quiz_id)
        quiz_details = list()
        for quiz in quizes:
            quiz_details.append({'quiz_id': quiz.id, 'name': quiz.name})
        return render_template("quiz_management.html", quiz_details=quiz_details)
    else:
        if quiz_id is None:
            teacher = Teacher.query.filter_by(username=username).first()
            quizes = Quiz.query.filter_by(teacher_id=teacher.id)
            quiz_details = list()
            for quiz in quizes:
                quiz_details.append({'quiz_id': quiz.id, 'name': quiz.name})
            return json.dumps(quiz_details)
        else:
            quizes = Quiz.query.filter_by(teacher_id=quiz_id)
            quiz_details = list()
            for quiz in quizes:
                quiz_details.append({'quiz_id': quiz.id, 'name': quiz.name})
            return json.dumps(quiz_details)


@app.route("/delete_quiz/<quiz_id>", methods=['GET', 'POST'])
def delete_quiz(quiz_id):
    if 'username' in session:
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz is None:
            return "Error! 404"
        else:
            db.session.delete(quiz)
            db.session.commit()
        return redirect(url_for('quiz_management'))
    else:
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz is None:
            return "Enter valid quiz id please!"
        else:
            db.session.delete(quiz)
            db.session.commit()
            return redirect(url_for("quiz_management"))


@app.route("/edit_quiz/<quiz_id>", methods=['GET', 'POST'])
@app.route("/edit_quiz", methods=['GET', 'POST'])
def edit_quiz(quiz_id=None):
    if 'username' in session:
        questions = get_questions(quiz_id)
        if questions == '[]':
            questions = {'questions': None, 'quiz_id': quiz_id}
            return render_template('edit_quiz.html', questions=questions)
        else:
            questions = {'questions': json.loads(questions), 'quiz_id': quiz_id}
            return render_template('edit_quiz.html', questions=questions)
    else:
        return "Login Please"


@app.route("/get_questions/<quiz_id>", methods=['GET'])
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id)
    question_details = list()
    for question in questions:
        options = list()
        options.append(dict({'option_a': question.option_a}))
        options.append(dict({'option_b': question.option_b}))
        options.append(dict({'option_c': question.option_c}))
        options.append(dict({'option_d': question.option_d}))
        question_details.append(dict({'id': question.id, 'statement': question.statement,
                                      'options': options, 'correct_ans': question.correct_ans,
                                      'quiz_id': question.quiz_id}))
    return json.dumps(question_details)


@app.route("/edit_question", methods=['GET', 'POST'])
def edit_question():
    question_id = request.form.get('question_id')
    question = Question.query.filter_by(id=question_id).first()
    question_body = {'id': question.id, 'statement': question.statement,
                     'option_a': question.option_a, 'option_b': question.option_b,
                     'option_c': question.option_c, 'option_d': question.option_d,
                     'correct_ans': question.correct_ans}
    return json.dumps(question_body)


@app.route("/update_question", methods=['POST'])
def update_question():
    question_id = request.form["question_id"]
    question_statement = request.form["question_statement"]
    option_a = request.form["option_a"]
    option_b = request.form["option_b"]
    option_c = request.form["option_c"]
    option_d = request.form["option_d"]
    ans = request.form["ans"]

    question = Question.query.filter_by(id=question_id).first()
    question.correct_ans = ans
    question.statement = question_statement
    question.option_a = option_a
    question.option_b = option_b
    question.option_c = option_c
    question.option_d = option_d
    db.session.commit()
    return redirect(url_for("edit_quiz", quiz_id=question.quiz_id))


@app.route("/delete_question/<question_id>/<quiz_id>", methods=['POST', 'GET'])
def delete_question(question_id, quiz_id):
    question = Question.query.filter_by(id=question_id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("edit_quiz", quiz_id=quiz_id))


@app.route("/add_question", methods=['POST'])
def add_question():
    statement = request.form['statement']
    option_a = request.form['option_1']
    option_b = request.form['option_2']
    option_c = request.form['option_3']
    option_d = request.form['option_4']
    correct_answer = request.form["correct_answer"]
    quiz_id = request.form['quiz_id']
    question = Question(statement=statement, option_a=option_a, option_b=option_b,
                        option_c=option_c, option_d=option_d, correct_ans=correct_answer,
                        quiz_id=quiz_id)
    db.session.add(question)
    db.session.commit()
    return "Success"
