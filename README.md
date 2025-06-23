# ConstantLine
![Made with Python](https://forthebadge.com/images/badges/made-with-python.png)
![Built with love](https://forthebadge.com/images/badges/built-with-love.png)

Light Python tool that logs whenever the network is down.

# Docker Container
If you plan to run ConstantLine on an ARM device (like Raspberry Pi), you can use our Docker Image.

Put the following in a `docker-compose.yaml`:

``` docker
services:
  constantline:
    image: sleepyspeller/constantline
    volumes:
      - /change/me/to/logs/folder:/logs
    environment:
      - HOSTNAMES=
      - TIMEOUT=2
      - SLEEP_TIME=1.2
      - SLEEP_TIME_DISCONNECTED=0.5
    restart: unless-stopped
```
Make sure to change `HOSTNAMES` and `volumes`. For example

`HOSTNAMES=1.1.1.1,google.com,8.8.8.8,yourwebsite.lol`\
`  - /home/user/logs:/logs`
(the folder has to mount as `/logs`)

Run `sudo docker compose up`. ([running as sudo is necessary](https://github.com/alessandromaggio/pythonping/issues/27))

Until we provide an amd64 image, you can use the [Dockerfile](https://github.com/SleepySpeller/ConstantLine/blob/main/Dockerfile) in the repo to build the image on your own.

# Reading logs
The output of consant line is in form of [JSONLine](https://jsonlines.org/), where each new line is a seperate JSON object.\
Here is an example:
``` json
{"timestamp": "2025-06-17T11:16:09.128088", "status": "starting", "ip": "122.10.144.143"}
{"timestamp": "2025-06-18T02:56:44.980575", "status": "disconnected", "ip": "122.10.144.143"}
{"timestamp": "2025-06-18T02:57:00.699254", "status": "reconnected", "ip": "122.10.144.200"}
```
The logs are stored in the `logs.jsonl` file in the `:/logs` mount provided in `docker-compose.yaml`
