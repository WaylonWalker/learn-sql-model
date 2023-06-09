from python:3.10

WORKDIR /app
Copy pyproject.toml /app
COPY learn_sql_model/__about__.py /app/learn_sql_model/__about__.py
COPY README.md /app
RUN pip3 install '.[all]'
COPY . /app
RUN pip3 install '.[all]'

EXPOSE 5000

ENTRYPOINT ["learn-sql-model", "api", "run"]
