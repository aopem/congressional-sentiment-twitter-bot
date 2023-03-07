# https://hub.docker.com/_/microsoft-dotnet
#
# BUILD stage
#
FROM python:3.11.2

WORKDIR /

# install utilities
RUN apt-get update -y && \
    apt-get install -y curl gcc build-essential

# install pip3
RUN pip3 install --upgrade pip setuptools

# install Microsoft ODBC 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc && \
    . ~/.bashrc

# optional: for unixODBC development headers
# optional: kerberos library for debian-slim distributions
RUN apt-get install -y unixodbc-dev && \
    apt-get install -y libgssapi-krb5-2

# copy and install requirements
COPY ./sentiment_tweet_job/requirements.txt /
RUN pip3 install -r requirements.txt

# copy app files
COPY ./sentiment_tweet_job .

# run app
CMD [ "python3", "main.py" ]