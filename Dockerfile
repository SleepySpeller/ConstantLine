FROM python:3.12-slim-bookworm
WORKDIR /app

RUN apt update -y && apt install git -y
RUN git clone https://github.com/sleepyspeller/constantline

WORKDIR /app/constantline

RUN pip install -r requirements.txt

VOLUME ["/logs"]

ENV TIMEOUT=2
ENV SLEEP_TIME=1.2
ENV SLEEP_TIME_DISCONNECTED=0.5

# This is needed in order for the script to run at all.
ENV PYTHONUNBUFFERED=1 

CMD ["python", "main.py"]
