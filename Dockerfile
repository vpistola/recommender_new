FROM python:3

WORKDIR /app

RUN apt-get update && apt-get -y install gcc unixodbc build-essential nano

# The following RUN command is for install the Microsoft ODBC driver for SQL Server (Linux)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && ACCEPT_EULA=Y apt-get install -y mssql-tools18 && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN apt-get install -y unixodbc-dev

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn
RUN pip install numpy cython
RUN git clone https://github.com/NicolasHug/surprise.git && cd surprise && python setup.py install

COPY . .
RUN chmod +x ./boot.sh
RUN export FLASK_APP=app.py

# RUN chown -R epistola:epistola ./
# USER epistola

EXPOSE 5000
CMD /usr/local/bin/gunicorn -b :5000 'app:app'
#ENTRYPOINT ["./boot.sh"]