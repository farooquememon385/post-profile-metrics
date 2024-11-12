## Post and Profile Metrics Calculator

## Project Requirements

- Python 3+
- FastAPI
- Uvicorn
- SQLAlchemy
- psycopg2-binary
- pydantic
- python-multipart
- python-dotenv
- pandas
- numpy
- Docker (if you want to run the project in docker container)

## Database Diagram

[Database Diagram](https://dbdiagram.io/d/67304c62e9daa85acae8f2ef)

![Diagram](/public/MetricsTable.png)

## How to run

### Run on Your Local Machine

1. Create a virtual environment

```
python3 -m venv env
source env/bin/activate
```

2. cd into app

```
cd app
```

3. install requuirements

```
pip install -r requirements.txt
```

5. run the project

```
uvicorn main:app --reload
```

### Run on Docker

1.  cd into app

```
cd app
```

2. run the project

```
docker-compose up --build
```

3. shutdown the project (when needed)

```
docker-compose down
```

## View the project after running successfully

- [http://localhost:8000/](http://localhost:8000/)
- [http://localhost:8000/docs](http://localhost:8000/docs) for testing APIs
