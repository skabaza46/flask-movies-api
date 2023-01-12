FROM python:3.9

WORKDIR /api
EXPOSE 8080
EXPOSE 5000
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD python api.py --run

CMD ["python", "app.py", "--run"]