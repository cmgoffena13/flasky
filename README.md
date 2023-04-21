# Flasky Website
## Tutorial Followed: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### Modifications that I introduced:
- Using Postgres instead of SQLite
- Added custom naming convention for SQLAlchemy constraints
- Changed Models ID columns to be more verbose: ex. post_id
- Added additional DEFAULT column so server handles timestamp: created_on
- Added datetimestamp as naming convention for migration files
- Used pytest instead of unittest
- Added additional CLI commands for testing purposes
- Added use of Docker container
- Added in Docker scripts for ease of development, docker start includes volume mount so modification of repo code is reflected without needing to start/stop again
- Added in .env.example and .flaskenv.example files

### Notes:
- Skipping the azure translator service currently
- Currently working through Chapter 20
- Might look into adding logging, tutorial skipped it and could add more detail than gunicorn or flask provides
- Need postgres and elasticsearch locally installed, might look into docker-compose to get around this