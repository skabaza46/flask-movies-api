FROM python:3.9.16-slim-bullseye

WORKDIR /api
# ADD . /api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080

# CMD python api.py --run
CMD ["python", "app.py", "--run"],

