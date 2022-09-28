# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET `/category`

- General:
  - Fetches all categories available in a json object
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains an object of `id: category_string` key:value pairs.

    ```json
    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      }
    }
    ```

#### GET `/questions?page=1`

- General:
  - Fetches a dataset containing paginated questions, the total number of questions, all categories and current category string.
  - Request Arguments: `page` - integer. If it is not passed expicitly, it defaults to 1.
  - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

    ```json
    {
      "categories": [
          {
            "id": 1, 
            "type": "Science"
          }, 
          {
            "id": 2, 
            "type": "Art"
          }, 
          {
            "id": 3, 
            "type": "Geography"
          }, 
          {
            "id": 4, 
            "type": "History"
          }, 
          {
            "id": 5, 
            "type": "Entertainment"
          }, 
          {
            "id": 6, 
            "type": "Sports"
          }
      ], 
    "current_category": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "total_questions": 19
    }

    ```

### DELETE `/questions/<id>`

- General:
  - Deletes a specified question using the id of the question
  - Request Arguments: `id` - integer
  - Returns: the `id` of the deleted question

    ```json
    {
      "success": True,
      "id": question_id
    }
    ```

### GET `/categories/<id>/questions`

- General:
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: `id` - integer
    - Returns: An object with questions for the specified category, total questions, and current category string

      ```json
      {
        "current_category": "Science", 
        "questions": [
          {
            "answer": "The Liver", 
            "category": 1, 
            "difficulty": 4, 
            "id": 20, 
            "question": "What is the heaviest organ in the human body?"
          }, 
          {
            "answer": "Alexander Fleming", 
            "category": 1, 
            "difficulty": 3, 
            "id": 21, 
            "question": "Who discovered penicillin?"
          }, 
          {
            "answer": "Blood", 
            "category": 1, 
            "difficulty": 4, 
            "id": 22, 
            "question": "Hematology is a branch of medicine involving the study of what?"
          }
        ], 
        "success": true, 
        "total_questions": 3
      }
      ```

### POST `/questions`
- General:
    - Inserts a new question to the list of questions
    - Request Body:

      ```json
      {
        "question": "How many planets are in our solar system?",
        "answer": "Nine",
        "difficulty": 1,
        "category": 1
      }
      ```
    - Returns the question id of the newly inserted question
      ```json
      {
        "success": True,
        "id": question.id
      }
      ```

### POST `/questions`
- General:
    - Searches for a question with the given search query
    - Request Body:
      ```json
      {
        "searchTerm": "this is the term the user is looking for"
      }
      ```
    - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

      ```json
      {
        "questions": [
          {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
          }
        ],
        "total_questions": 100,
        "current_category": "Entertainment"
      }
      ```

### GET `/quizzes`
- General:
    - Sends a post request in order to get the next question
    - Request Body:

      ```json
      {
          "previous_questions": [1, 4, 20, 15]
          "quiz_category": {
            "id": "1",
            "type": "Science"
          }
      }
      ```

    - Returns: a single new question object

      ```json
      {
        "question": {
          "id": 1,
          "question": "Who discovered penicillin?",
          "answer": "Alexander Fleming",
          "difficulty": 3,
          "category": 1
        }
      }
      ```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```