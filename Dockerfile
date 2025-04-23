FROM python:3.12-slim

WORKDIR /code

COPY requirement.txt requirement.txt

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

RUN python -m spacy download en_core_web_sm

EXPOSE 8000

CMD ["uvicorn","myenv.app:app","--host","0.0.0.0","--port","8000"]

