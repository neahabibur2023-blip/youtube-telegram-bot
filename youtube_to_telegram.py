import os
import requests
import time
from flask import Flask

# Flask App
app = Flask(__name__)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "7874904494:AAH-MrzRbbBXPqsR66MT3N6dHTikdrc2L4I")
CHAT_ID = os.getenv("CHAT_ID", "5942277435")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyBOLnfr4geGr7rglTtTKVLugn0KaDfNtkE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "UC3GqJxjrfoMcH44hXp8a9gA")

last_video_id = None

def get_latest_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1"
    response = requests.get(url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        latest_video = data["items"][0]
        video_id = latest_video["id"]["videoId"]
        title = latest_video["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        return video_id, title, url
    return None, None, None

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/check")
def check():
    global last_video_id
    video_id, title, url = get_latest_video()
    if video_id and video_id != last_video_id:
        last_video_id = video_id
        send_to_telegram(f"📢 New video uploaded: {title}\n{url}")
        return "New video sent!"
    return "No new video."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
