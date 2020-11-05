Bulletin Example App
====================

Example chat room API


Instructions
------------

**Manual**

1. Install dependencies `pip3 install -r requirements.txt`
2. Initialize database `python3 manage.py migrate`
3. Generate static files `python3 manage.py collectstatic --no-input`
4. Create your user `python3 manage.py createsuperuser`
5. Run server `python3 manage.py runserver 0.0.0.0:8080`
6. Navigate to http://localhost:8080/admin

**Scripts**

1. Install project `script/setup`
2. Create your user `python3 manage.py createsuperuser`
3. Run project `script/server`
4. Navigate to http://localhost:8080/admin

**Docker**

1. Run docker compose `docker-compose up`
2. In a separate console,
    - Run database migrations `docker-compose exec app python3 /deploy/app/manage.py migrate`
    - Create user `docker-compose exec app python3 /deploy/app/manage.py createsuperuser`
3. Navigate to http://localhost:8080/admin


Acceptance Criteria
-------------------

1. Users
    * Users must have a unique username ✓
    * Users can sign up with username & password ✓
    * Users can login with username & password ✓
2. Topic
    * Any authenticated user can create a new topic ✓
    * Authenticated users can list topics by most recently active ✓
3. Messages
    * Authenticated users can post messages in topics ✓
    * Authenticated users can list the last 50 messages for a ~~room~~ topic ✓
4. Authentication
    * Should be Bearer Auth ✓
5. Deployment
    * The app does not have to be deployed however there should be instructions on how to run it locally ✓
    * While the app doesn't need to be deployed please design it as if you were going to deploy it and be prepared to describe how you would deploy it to production including CI/CD, Cloud Provider and services and why you would choose those.
6. UI
    * Please create a basic UI with the following
        * Users can login & logout
        * Authenticated users can create topics & see list of topics
        * Authenticated users can view recent messages in topic & post message to topic
        * The UI doesn't have to be real time but be prepared to talk about how you might make it real time & the implications of your choices for deployment & scaling
        * Using a SPA framework is encouraged but not strictly required. Be prepared to talk about why you chose the UI framework you used
        
        
Technologies
------------

Language: Python
Framework: Django
Database: Postgres
Cache: Redis
UI: React (Ionic)
Local Deployment: Docker
Cloud Service: AWS Lambda (with serverless)
CI/CD: Travis CI
Testing: Pytest


Explanation
-----------



Future Enhancements
-------------------

- Private rooms with invite-only