FROM python:3.8
WORKDIR app/
COPY 'requirements.txt' .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .