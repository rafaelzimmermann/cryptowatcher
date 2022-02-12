FROM python:3.9.7-slim-buster

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/app
RUN mkdir $HOME
RUN mkdir $HOME/cache
WORKDIR $HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat

# Mac running on M1 chip fix
RUN apt update -y && apt install -y build-essential libpq-dev
COPY requirements.txt .
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
# M1 fix
RUN pip install psycopg2-binary --no-binary psycopg2-binary
RUN pip install -r requirements.txt

# copy entrypoint-prod.sh
COPY ./script/entrypoint.sh $HOME

# copy project
COPY . $HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

ENTRYPOINT ["bash", "/app/entrypoint.sh"]

