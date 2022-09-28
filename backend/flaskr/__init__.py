#----------------------------------------------------------------------------#
# Attribution
# https://github.com/bytrebase/cd0037-API-Development-and-Documentation-project/blob/main/backend/flaskr/__init__.py
#----------------------------------------------------------------------------#

from crypt import methods
from importlib import resources
from unicodedata import category
from flask import Flask, request, abort, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    def retrieveCategories():
        categories = Category.query.all()

        category_dict = dict()
        formatted_categories = [category.format() for category in categories]
        for cat in formatted_categories:
            key = str(cat['id'])
            value = cat['type']
            category_dict[key] = value

        return category_dict

    @app.route('/categories', methods=['GET'])
    def get_categories():
        return jsonify({
            'success': True,
            'categories': retrieveCategories()
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def paginate_questions(request, data):

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in data]
        current_questions = formatted_questions[start:end]
        return current_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()

        formatted_questions = paginate_questions(request, questions)
        if (len(formatted_questions) == 0):
            abort(404)

        categories = Category.query.all()
        formatted_categories = dict()
        
        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'categories': formatted_categories,
            'current_category': '',
            'total_questions': len(questions)
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'id': question_id
            })

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        if search_term != None:
            search_results = \
                Question.query.filter(Question.question.ilike(
                    '%{}%'.format(search_term))).all()
            
            formatted_results = [result.format() for result in search_results]
            return jsonify({
                'success': True,
                'questions': formatted_results,
                'total_questions': len(search_results),
                'current_category': retrieveCategories()
            })
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            try:
                question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
                question.insert()

                return jsonify({
                    'success': True,
                    'id': question.id
                })
            except:
                abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # @app.route('/questions', methods=['POST'])
    # def search_questions():
    #     body = request.get_json()

    #     search_term = body.get('searchTerm', None)

    #     try:
    #         if search_term != None:
    #             search_results = \
    #                 Question.query.filter(Question.question.ilike(
    #                     '%{}%'.format(search_term))).all()
    #             return jsonify({
    #                 'success': True,
    #                 'questions': search_results,
    #                 'totalQuestions': len(search_results),
    #                 'currentCategory': retrieveCategories()
    #             })
    #     except:
    #         abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_categorical_questions(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]
        category = Category.query.get(category_id).type

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        prev_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category:
            question = Question.query.filter(Question.category == str(quiz_category['id']))\
                .filter(Question.id.notin_(prev_questions)).order_by(func.random()).first()
        else:
            abort(400)

        if question is None:
            question = Question.query.filter(Question.id.notin_(prev_questions)).order_by(func.random()).first() 

        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }),
            400
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }),
            405,
        )

    return app
