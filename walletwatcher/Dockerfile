FROM python:3.9.7-slim-buster

RUN apt-get update
RUN apt-get -y install cron
RUN pip install --upgrade pip

RUN echo "*/1 * * * * root /app/balanceimporter.py > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/balanceimporter_job
RUN chmod 0644 /etc/cron.d/balanceimporter_job

RUN mkdir -p /var/log
RUN touch /var/log/cron.log

RUN mkdir /app
ADD . /app/
RUN chmod u+x /app/balanceimporter.py
RUN pip install -r /app/requirements.txt

CMD cron && tail -f /var/log/cron.log