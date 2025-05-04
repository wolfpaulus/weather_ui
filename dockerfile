# Dokerfile to create the container image for the wordgame app
FROM python:3.13-slim
LABEL maintainer="Wolf Paulus <wolf@paulus.com>"

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Phoenix /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY . /weather
RUN pip install --no-cache-dir --upgrade -r /weather/requirements.txt
RUN chmod +x /weather/healthcheck.sh
WORKDIR /weather/

EXPOSE 8000

#  prevents Python from writing .pyc files to disk
#  ensures that the python output is sent straight to terminal (e.g. the container log) without being first buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/weather

CMD ["python3.13",  "-m", "streamlit", "run", "--server.port", "8000", "src/Forecast.py"]
