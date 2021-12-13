from flask import Flask, redirect, url_for, request, make_response
from flask.helpers import make_response
import requests
import os
from dotenv import load_dotenv
import math
import time
import base64

app = Flask(__name__)
load_dotenv(".env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SECRET = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
state = 102911
FADE_GAP = 0.1
FADE_TIME = 2
MAX_VOL = 70
MIN_VOL = 30

# Root page shows what the auth URL is


@app.get('/')
def root():
    return redirect(f"https://accounts.spotify.com/authorize?response_type=code&state={state}&client_id={CLIENT_ID}&scope=user-read-playback-state user-modify-playback-state&redirect_uri=http://localhost:5000/callback")


@app.get('/callback')
def callback():
    code = request.args.get('code')

    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "code": code,
            "redirect_uri": "http://localhost:5000/callback",
            "grant_type": "authorization_code"
        },
        headers={
            # Base64 tokens must not have freegin space
            "Authorization": "Basic " + SECRET,
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    response = make_response(redirect(url_for("devices")))
    response.set_cookie("access_token", r.json().get("access_token"))

    return response


@app.get('/devices')
def devices():
    token = request.cookies.get("access_token")
    print(token)
    r = requests.get(
        "https://api.spotify.com/v1/me/player",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    os.environ["cur_vol"] = str(r.json()["device"]["volume_percent"])
    os.environ["player_id"] = str(r.json()["device"]["id"])
    return r.json()


@app.get("/fade_up")
def fade_up():
    token = request.cookies.get("access_token")
    cur_vol = int(os.environ.get("cur_vol"))
    player_id = os.environ.get("player_id")
    counts = FADE_TIME/FADE_GAP
    increment = math.floor((MAX_VOL-cur_vol) / counts)
    while cur_vol < MAX_VOL and increment != 0:
        cur_vol += increment
        r = requests.put(
            "https://api.spotify.com/v1/me/player/volume",
            params={
                "volume_percent": cur_vol,
                "device_id": player_id
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print(r.status_code)
        time.sleep(FADE_GAP)
    os.environ["cur_vol"] = str(MAX_VOL)
    return "Fade up done"


@app.get("/fade_down")
def fade_down():
    token = request.cookies.get("access_token")
    cur_vol = int(os.environ.get("cur_vol"))
    player_id = os.environ.get("player_id")
    counts = FADE_TIME/FADE_GAP
    decrement = math.floor((cur_vol-MIN_VOL) / counts)
    while cur_vol > MIN_VOL and decrement != 0:
        cur_vol -= decrement
        r = requests.put(
            "https://api.spotify.com/v1/me/player/volume",
            params={
                "volume_percent": cur_vol,
                "device_id": player_id
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print(r.status_code)
        time.sleep(FADE_GAP)
    os.environ["cur_vol"] = str(MIN_VOL)
    return "Fade down done"
