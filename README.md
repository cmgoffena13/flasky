# Flasky Website
## Tutorial Followed: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Local Development Setup
1. Create .env and .flaskenv files based upon example files (Doesn't require azure translator service)
2. Install local Postgres server and create database flasky
3. Install local elasticsearch server, I ran into a maxmem error when trying docker
4. Run docker command `docker compose up`

### Application Functionality (Simple Social Media App)
- Register/Login pages: User registration, login/logout, and reset password capability
- Profile page: Shows current user posts, general information, and ability to modify if current user
- Timeline page: Create text posts as a user,
- Explore page: Explore posts that have been written by all users, pagination included
- Profile page: Export posts functionality using task queue, shows progress bar and is emailed
- Profile page: Follow/Unfollow other users to show their posts on your timeline
- Profile page: Message other users that you follow
- Popup of user profiles when mouse hovering
- Message notifications
- Search capability on posts
- Can be switched to other languages once translation files are filled out
- Logs to text files, stdout stream, and emails ADMIN upon errors depending upon configuration
- API functionality

### Modifications that I introduced:
- Using Postgres instead of SQLite
- Added custom naming convention for SQLAlchemy constraints
- Changed Models ID columns to be more verbose: ex. post_id
- Added additional DEFAULT column so server handles timestamp: created_on
- Added datetimestamp as naming convention for migration files
- Used pytest instead of unittest
- Added additional CLI commands for testing purposes
- Added use of Docker container
- Added in Docker scripts for ease of development, docker start includes volume mount so modification of repo code is reflected without needing to start/stop again (switched to docker-compose for ease of use)
- Added in .env.example and .flaskenv.example files
- Added in Docker-Compose to orchestrate the redis queue and rq worker services
- Added flask-smorest package for API and marshmallow schemas for validation (re-structured to accommodate)
- Includes API swagger documentation at localhost:5000/swagger-ui
- Setup Postman collections and environment to test the API calls

### Notes:
- Skipping the azure translator service currently
- Currently working through Chapter 23, adding API functionality
- Might look into adding more logging, tutorial skipped it and could add more detail than gunicorn/flask provides
- Need postgres and elasticsearch locally installed, had issues with max mem for docker elasticsearch so kept local
- Might explore a use-case for postgres stored procedures to put computation on the server side