FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_PROGRESS_BAR=off \
    TQDM_DISABLE=1

# Language runtimes and inspection tools shared by every coding task.
RUN apt-get update && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        sqlite3 \
        nodejs \
        npm \
        default-jdk-headless \
        xvfb \
        xauth \
        xdotool \
        imagemagick \
        chromium \
        poppler-utils \
        qpdf \
    && rm -rf /var/lib/apt/lists/*

# Common Python libraries for implementing and testing the delivered software.
RUN pip install --no-cache-dir \
        pytest==8.3.2 \
        requests \
        flask==3.0.3 \
        pypdf \
        PyPDF2 \
        fastapi \
        uvicorn \
        httpx

WORKDIR /workspace
