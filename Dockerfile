FROM python:3.10-slim

LABEL maintainer="Shubham Bansal <shubhambansal17@hotmail.com>"

# Environment varialbes to control python and pip behaviour.
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt


CMD ["python", "scraper/scraper.py"]

