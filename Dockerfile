FROM python:3.11

WORKDIR /code

EXPOSE 8000

RUN pip install "poetry==1.6.0"

COPY poetry.lock pyproject.toml /code/

RUN poetry config installer.max-workers 10

RUN poetry config virtualenvs.create false \
  && poetry install --no-root

COPY .  .

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]