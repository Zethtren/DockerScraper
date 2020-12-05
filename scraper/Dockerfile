FROM python:3.9-slim-buster


ENV DEBIAN_FRONTEND noninteractive

ENV SA_PASSWORD=asdffdsaasdffdsa1234!
ENV TABLE_NAME=BTC-USD
ENV DB_NAME=ticks
ENV LOG_INSERTS=True
ENV SERVER_NAME=sql-server
ENV ACCEPT_EULA=Y

RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev


RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc


RUN pip install --upgrade pip
RUN pip install pyodbc
RUN pip install copra


RUN apt-get -y clean

COPY . /app
WORKDIR /app
CMD ["-u", "scraper.py"]
ENTRYPOINT ["python"]