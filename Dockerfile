FROM python:3.10
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# Set working directory in container
WORKDIR /flasky
# Copy Repo into Docker Container
COPY . .
# Expose Postgres port
EXPOSE 5432
# Expose Flask/Gunicorn port
EXPOSE 5000
# Declare bash script to trigger upon start up
ENTRYPOINT ["./docker-entrypoint.sh"]