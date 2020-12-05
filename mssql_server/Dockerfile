  
FROM mcr.microsoft.com/mssql/server:2019-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=asdffdsaasdffdsa1234!
ENV DB_NAME=ticks
ENV MSSQL_PID=Developer 

EXPOSE 1433
USER root
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN chmod +x /usr/src/app/run-initialization.sh
USER mssql
ENTRYPOINT /bin/bash ./entrypoint.sh
