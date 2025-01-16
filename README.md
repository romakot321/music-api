# Music generation API in Python3 FastAPI
Simple to use API for generating music with lyrics.

## Documentation:
Available at http://localhost:8000/docs as Swagger after run.

## Run:

### Development mode
- Specify the API Key from https://www.topmediai.com/api/ai-music-generator-api/ in .env file(example is in example.env)
- Create virtual environment: `python3 -m venv env && activate env/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Install project source: `pip install -e .`
- Run redis: `docker compose up -d redis`
- Run app: `uvicorn app.main:fastapi_app --reload`

### Production mode
- Specify the API Key from https://www.topmediai.com/api/ai-music-generator-api/ in .env file(example is in example.env)
- `docker compose up -d --build`
