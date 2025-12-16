# Local webhook receiver

Quickstart

1) Create a venv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

2) Run a reverse proxy (e.g, [ngrok](https://ngrok.io) or [Tailscale Funnel](https://tailscale.com/kb/1223/funnel))
3) Configure an API client in the Portal, and configure it with the reverse proxy address
4) Add the API client to a team
5) Add the team to a fleet / region, with the appropriate notifications enabled
6) Configure the script with the downloaded HMAC secret from step 3, and an optional bearer token
   (provided by the end user)
7) Run the server:

```bash
python app.py
```

Server listens on http://localhost:8000

Endpoints

- POST /webhook -> accepts an asynchronous webhook call from the Thoro Portal

Example expected payload shape

```json
{
  "event": "ai.thoro.device.power_on",
  "message": "Power on event",
  "body": {
    "robot_id": "0016338",
    "fleet_id": "1",
    "timestamp": 1765890030
  }
}
```

Example curl

```bash
curl -X POST http://localhost:8000/webhook \
  -H 'Content-Type: application/json' \
  -d '{
    "event":"ai.thoro.device.power_on",
    "message":"Power on event",
    "body":{"robot_id":"0016338","fleet_id":"1","timestamp":1765890030}
  }'
```
