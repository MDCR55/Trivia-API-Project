import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.test_question = {
            'question': 'What is the capital of KSA',
            'answer': 'Riyadh',
            'difficulty': '1',
            'category': '1'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    ################## Test cases ##################
    """

    def test_get_questions_page(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(res.status_code, 200)

    def test_get_questions_page_failure(self):
        res = self.client().get('/questions?page=111')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "We couldn't process your request.")

    def test_get_categoreis_page(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_questions_from_category(self):

        res = self.client().get(f"/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(data['currentCategory'], 2)

    def test_get_questions_from_category_failure(self):

        res = self.client().get(f"/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "We couldn't process your request.")

    def test_add_questions(self):
        res = self.client().post('/questions', json=self.test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_delete_questions(self):
        res = self.client().post('/questions', json=self.test_question)
        data = json.loads(res.data)

        question_id = data["question"]["id"]

        res = self.client().delete(f"questions/{question_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        deleted_question = Question.query.get(question_id)
        self.assertEqual(deleted_question, None)

    def test_delete_questions_failure(self):
        res = self.client().delete("questions/124432432")

        self.assertEqual(res.status_code, 404)

    def test_search(self):

        search_term = 'man'
        res = self.client().post(f'/questions/{search_term}')
        data = json.loads(res.data)
        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).count()
        self.assertEqual(data['totalQuestions'], questions)

    def test_quiz(self):
        response = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [5],
                "quiz_category": {"type": "Geography", "id": "3"},
            },
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])

    def test_quiz_failure(self):
        response = self.client().post(
            "/quizzes",
            json={
                'quiz_category':
                {'type': 'Test',
                 'id': 1}},
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
