import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    question = [question.format() for question in selection]
    current_questions = question[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    function for creating an endpoint to handle GET
    requests for all available categories.
    returns:
        list of categories
    '''

    @app.route('/categories')
    def get_categories():

        categories = list(map(Category.format, Category.query.all()))
        result = {
            "success": True,
            "categories": categories
        }
        return jsonify(result)

    '''
    function for handle GET requests for questions.
    returns:
        list of questions
    '''

    @app.route('/questions')
    def get_questions():

        try:
            selection = Question.query.all()
            categories = Category.query.all()
            categoriesDict = {}

            for category in categories:
                categoriesDict[category.id] = category.type

            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            result = {
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(current_questions),
                'categories': categoriesDict,
                'current_category': None,
            }

            return jsonify(result)

        except BaseException:
            abort(422)

    '''
    function for delete a question based on its id
    returns:
        json message of the deleted question.
    '''

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)

            result = {
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(current_questions),
                'deleted': question_id,
            }

            return jsonify(result)

        except:
            abort(404)

    '''
    function for posting a new question
    returns:
        json message of the added question.
    '''

    @app.route('/questions', methods=["POST"])
    def add_question():

        body = request.get_json()
        new_question = body["question"]
        new_answer = body['answer']
        new_difficulty = body['difficulty']
        new_category = body['category']

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )

            question.insert()

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except BaseException:
            abort(422)

    '''
    function for getting questions based on a search term.
    returns:
        list of questions that matches the search term
    '''

    @app.route('/questions/<searchTerm>', methods=["POST"])
    def search_question(searchTerm):
        try:

            res_search = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            current_questions = paginate_questions(request, res_search)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(current_questions),
                'currentCategory': ''
            })

        except BaseException:
            abort(422)

    '''
    function for getting questions based on category.
    returns:
        list of questions based on its category.
    '''

    @app.route('/categories/<int:id>/questions', methods=["GET"])
    def get_gategory(id):

        try:
            categories = Category.query.all()

            if id <= len(categories):
                questions = Question.query.filter_by(category=str(id)).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                    'currentCategory': id + 1
                })
            else:
                abort(404)

        except BaseException:
            abort(422)

    '''
  function for getting questions to play the quiz.
  returns:
      list of categories and questions of the realated category
  '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()

        prv_question = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        category_id = category.get('id', None)
        
        if category_id == 0:
            if prv_question is not None:
                questions = Question.query.filter(
                    Question.id.notin_(prv_question)).all()
            else:
                questions = Question.query.all()

        else:
            category = Category.query.get(category_id)
            if prv_question is not None:
                questions = Question.query.filter(
                    Question.id.notin_(prv_question),
                    Question.category == str(category_id)).all()
            else:
                questions = Question.query.filter(
                    Question.category == str(category_id)).all()

        next_question = questions[random.randrange(
            0, len(questions))].format() if len(
                questions) > 0 else None

        if next_question is None:
            next_question = False

        return jsonify({
            'success': True,
            'question': next_question
        })


    '''
    ##############
    error handlers for all expected errors
    ##############
    '''

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({"success": False, "error": 400,
                        "message": "Bad request."}), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "We couldn't process your request.",
                }
            ),
            422,
        )

    return app
