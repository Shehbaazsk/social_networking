Social Media API

This project is a basic social media application API built using Django and Django REST Framework. It allows users to register, log in, send friend requests, respond to friend requests, and list their accepted friends.
Features

    User Registration and Login
    Send Friend Requests
    Accept or Reject Friend Requests
    List Friends Who Have Accepted a Friend Request
    Custom Throttling to Limit the Number of Friend Requests Sent
    JWT Authentication

Installation
1. Clone the Repository

bash

git clone https://github.com/your-username/social-media-api.git
cd social-media-api

2. Set Up a Virtual Environment

bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies

bash

pip install -r requirements.txt

4. Set Up the Database

Apply the database migrations to set up the necessary tables:

bash

python manage.py migrate

5. Create a Superuser

Create a superuser to access the Django admin:

bash

python manage.py createsuperuser

6. Run the Development Server

Start the Django development server:

bash

python manage.py runserver

The server will be running at http://127.0.0.1:8000/.
API Endpoints
1. User Registration

    URL: /signup/
    Method: POST
    Description: Register a new user.
    Request Body:

    json

{
  "email": "user@example.com",
  "password": "password",
  "first_name": "First",
  "last_name": "Last"
}

Response:

json

    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "First",
      "last_name": "Last"
    }

2. User Login

    URL: /login/
    Method: POST
    Description: Authenticate a user and return a JWT token.
    Request Body:

    json

{
  "email": "user@example.com",
  "password": "password"
}

Response:

json

    {
      "refresh": "jwt_refresh_token",
      "access": "jwt_access_token"
    }

3. Send Friend Request

    URL: /friend-request/send/
    Method: POST
    Description: Send a friend request to another user.
    Request Body:

    json

{
  "receiver_id": 2
}

Response:

json

    {
      "message": "Friend request sent successfully."
    }

4. Respond to Friend Request

    URL: /friend-request/respond/
    Method: POST
    Description: Accept or reject a friend request.
    Request Body:

    json

{
  "friend_request_id": 1,
  "action": "accept"  // Or "reject"
}

Response:

json

    {
      "status": "friend request accepted"
    }

5. List Accepted Friends

    URL: /friends/
    Method: GET
    Description: List all friends who have accepted the friend request.
    Response:

    json

    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "First",
      "last_name": "Last",
      "friends": [
        {
          "id": 2,
          "email": "friend1@example.com",
          "first_name": "Friend",
          "last_name": "One"
        },
        {
          "id": 3,
          "email": "friend2@example.com",
          "first_name": "Friend",
          "last_name": "Two"
        }
      ]
    }

6. List Pending Friend Requests

    URL: /friend-request/pending/
    Method: GET
    Description: List all pending friend requests received by the user.
    Response:

    json

    [
      {
        "id": 1,
        "sender": {
          "id": 2,
          "email": "friend1@example.com",
          "first_name": "Friend",
          "last_name": "One"
        },
        "receiver": {
          "id": 1,
          "email": "user@example.com",
          "first_name": "First",
          "last_name": "Last"
        },
        "status": "pending",
        "created_at": "2024-01-01T12:00:00Z"
      }
    ]

Running the Project with Docker
1. Build and Run the Docker Container

If you prefer to run the project using Docker, use the following commands:

bash

docker-compose build
docker-compose up

The API will be available at http://localhost:8000/.
Testing the API

To test the API, you can use Postman or any other API testing tool. Import the provided Postman collection (if available) to get started quickly.
Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.
License

This project is licensed under the MIT License - see the LICENSE file for details.