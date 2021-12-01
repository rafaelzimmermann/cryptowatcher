FROM python:3.9.7-slim-buster

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/app
RUN mkdir $HOME
WORKDIR $HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $HOME

# copy project
COPY . $HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

ENTRYPOINT ["bash", "/app/entrypoint.sh"]