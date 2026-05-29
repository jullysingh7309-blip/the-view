FROM python:3.11-slim

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m nltk.downloader averaged_perceptron_tagger punkt stopwords wordnet vader_lexicon -d /usr/local/nltk_data

COPY src/ app/
WORKDIR /app

ENV PORT=8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 app:app
