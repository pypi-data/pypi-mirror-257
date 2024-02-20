ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION}
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR ${APP_HOME}
#RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 libmagic-dev
COPY ./requirements.txt ${APP_HOME}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . ${APP_HOME}
CMD ["python3", "-m", "rcee"]
