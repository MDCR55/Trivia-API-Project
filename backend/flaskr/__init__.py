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
    function for creating an endpoint to handle GET requests for all available categories.
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
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
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

          except:
            abort(422)

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
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
            abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  § 1q
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

        except:
            abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
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

          except:
            abort(422)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:id>/questions', methods=["GET"])
    def get_gategory(id):

        try:
            categories = Category.query.all()

            if id <= len(categories):
                questions = Question.query.join(
                    Category, Question.category == id+1).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(questions),
                    'currentCategory': id+1
                })
            else:
                abort(400)

        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            body = request.get_json()
            prv_question = body['previous_questions']
            category = body["quiz_category"]["id"]
            if category == 0:
                if prv_question is not None:
                    questions = Question.query.filter(
                                Question.id.notin_(prv_question)).all()
                else:
                    questions = Question.query.all()
            
            else:
                category = Category.query.get(category)
                if prv_question is not None:
                    questions = Question.query.filter(
                                Question.id.notin_(prv_question),
                                Question.category == category.id).all()
                else:
                    questions = Question.query.filter(
                                Question.category == category.id).all()
            next_question = random.choice(questions).format()
            if next_question is None:
                next_question = False
            return jsonify({
                'success': True,
                'question': next_question
            })
        except:
            abort(422)
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
