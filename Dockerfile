FROM python:3.8.7
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:6003", "--log-file", "-", "--access-logfile", "-", "--error-logfile", "-"]
EXPOSE 6003