FROM python:3.13.0-alpine3.20

WORKDIR /app

RUN addgroup -g 1000 app && adduser -D -u 1000 -G app app 
# we create the group. then we create the user, we define its id as app too, and we add it to the group app

COPY --chown=app . .
# we copy all the files and designate app as the owner of the files
# if we dont want to upload the venv we add a .dockerignore file with the venv folder

RUN apk update &&\
    apk add --no-cache curl &&\
    pip install --no-cache-dir --upgrade pip &&\
    pip install -r requirements.txt

#pip install --no-cache-dir gunicorn Flask flask-cors pymongo marshmallow flasgger

EXPOSE 8000 
#gunicorn will run on port 8000, thats why we expose it

HEALTHCHECK CMD curl --fail http://localhost:8000/healthcheck || exit 1
# we only execute exit 1 if curl fails

USER app

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-w 4", "app:app"]
#--bind: anyone can access the server
# well be listening on 0.0.0.0:8000
# -w 4: tells gunicorn to run 4 workers to handle the requests