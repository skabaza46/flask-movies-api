FROM python:3.9

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD python api.py --run

CMD ["python", "app.py", "--run"]
