# Flasky Website
## Tutorial Followed: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Setup
1. Create .env and .flaskenv files based upon example files
2. A local ElasticSearch server is required if you have an elasticsearch URL

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

### Notes:
- Skipping the azure translator service currently
- Currently working through Chapter 23
- Might look into adding more logging, tutorial skipped it and could add more detail than gunicorn/flask provides
- Need postgres and elasticsearch locally installed, had issues with max mem for docker elasticsearch so kept local
- Might explore a use-case for postgres stored procedure