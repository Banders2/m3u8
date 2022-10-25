FROM selenium/standalone-chrome
EXPOSE 5000
USER root
WORKDIR /tmp
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
RUN chmod 777 app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]