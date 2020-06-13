# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

## API Docs

- **GET "/categories"**

  - Returns a JSON object of the questions categories:

  - ```JSON
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
      "success": true
    }
    ```

- **GET "/questions?page=1"**

  - Returns paginated questions based on the page number	

  - ```json
      {
        "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
        }, 
        "current_category": null, 
        "questions": [
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
          }, 
          {
            "answer": "Agra", 
            "category": 3, 
            "difficulty": 2, 
            "id": 15, 
            "question": "The Taj Mahal is located in which Indian city?"
          }, 
          {
            "answer": "Escher", 
            "category": 2, 
            "difficulty": 1, 
            "id": 16, 
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          }, 
          {
            "answer": "Mona Lisa", 
            "category": 2, 
            "difficulty": 3, 
            "id": 17, 
            "question": "La Giaconda is better known as what?"
          }
        ], 
        "success": true, 
        "totalQuestions": 10
      }
      ```

- **POST"/questions/**

  - Add a new question to the database

  - Require the following information to be filled in the body

    - `question`: the question itself
    - `answer`: the answer of that question
    - `category`: the category of that question
    - `difficulty`: the difficulty level of that question

  - Sample body:

    - ```json
      {
          "question":"What is the capital of Saudi Arabia",
          "answer":"Riyadh",
          "category": "3",
          "difficulty":"1"
      }
      ```

  - Response would be like:

    - ```json
      {
         "question":{
            "answer":"Riyadh",
            "category":3,
            "difficulty":1,
            "id":25,
            "question":"What is the capital of Saudi Arabia"
         },
         "success":true
      }
      ```

- **DELETE "/questions/int:question_id"**

  - Will delete a question from the database based on the `question_id` and will return a JSON object with the id of the deleted question and the remaining questions 

  - ```json
    {
      "deleted": 10,
      "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
      ],
      "success": true,
      "totalQuestions": 10
    }
    ```
  
- **POST "/search"**

  - Search for full question or part of that question

  - Use `searchTerm` as a parameter in the URL to get the response like `http://localhost:3000/questions/saudi` using POST will return the following:

  - ```json
    {
      "currentCategory": "", 
      "questions": [
        {
          "answer": "Riyadh", 
          "category": 3, 
          "difficulty": 1, 
          "id": 25, 
          "question": "What is the capital of Saudi Arabia"
        }
      ], 
      "success": true, 
      "totalQuestions": 1
    }
    ```

  - **GET "/categories/int:category_id/questions"**

    - Return the questions of a specific category

    - Response would be like this:

    - ```json
      {
        "currentCategory": 2, 
        "questions": [
          {
            "answer": "Escher", 
            "category": 2, 
            "difficulty": 1, 
            "id": 16, 
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          }
        ], 
        "success": true, 
        "totalQuestions": 4
      }
      ```
      
    - **POST "/quizzes"**
    
  - Will search for questions based on selected category
    
  - The request body will be like:
    
    - `previous_questions`: List of previous questions that have been answered
        - `quiz_category`: The category selected in the quiz

      - Response body:
    
    - ```json
          {
        "question": {
              "answer": "Jackson Pollock", 
              "category": 2, 
              "difficulty": 2, 
              "id": 19, 
              "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            }, 
            "success": true
          }
          ```
