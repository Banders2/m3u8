FROM selenium/standalone-chrome
USER root
WORKDIR /tmp
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt
CMD "python3 app.py"