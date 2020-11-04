Bulletin Example App
====================

Example chat room API 


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
    * The app does not have to be deployed however there should be instructions on how to run it locally
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
Production Deployment: Lambda (serverless)
Testing: Pytest


Explanation
-----------



Future Enhancements
-------------------

- Private rooms with invite-only