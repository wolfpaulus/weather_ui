# Dokerfile to create the container image for the wordgame app
FROM python:3.13-slim
LABEL maintainer="Wolf Paulus <wolf@paulus.com>"

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Phoenix /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY . /wordgame
RUN pip install --no-cache-dir --upgrade -r /wordgame/requirements.txt
RUN chmod +x /wordgame/healthcheck.sh
WORKDIR /wordgame/

EXPOSE 8000

#  prevents Python from writing .pyc files to disk
#  ensures that the python output is sent straight to terminal (e.g. the container log) without being first buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/wordgame

CMD ["python3.13",  "-m", "streamlit", "run", "--server.port", "8000", "src/app.py"]
