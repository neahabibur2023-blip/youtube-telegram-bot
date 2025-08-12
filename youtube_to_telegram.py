import os
import requests
import time
from flask import Flask
from threading import Thread

# Flask app for Render keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube → Telegram bot is running!"

# Environment variables (এখানে সরাসরি সেট করা হয়েছে)
BOT_TOKEN = "7874904494:AAH-MrzRbbBXPqsR66MT3N6dHTikdrc2L4I"
CHAT_ID = "5942277435"
YOUTUBE_API_KEY = "AIzaSyBOLnfr4geGr7rglTtTKVLugn0KaDfNtkE"
CHANNEL_ID = "UC3GqJxjrfoMcH44hXp8a9gA"

# Get latest YouTube video
def get_latest_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1"
    response = requests.get(url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        latest_video = data["items"][0]
        video_id = latest_video["id"]["videoId"]
        title = latest_video["snippet"]["title"]
        return video_id, title
    return None, None

# Send message to Telegram
def send_to_telegram(video_id, title):
    message = f"🎥 New Video Uploaded:\n{title}\nhttps://youtu.be/{video_id}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Background worker
def background_worker():
    last_video_id = None
    while True:
        try:
            video_id, title = get_latest_video()
            if video_id and video_id != last_video_id:
                send_to_telegram(video_id, title)
                last_video_id = video_id
        except Exception as e:
            print("Error:", e)
        time.sleep(300)  # প্রতি ৫ মিনিটে চেক করবে

# Start background worker in thread
if __name__ == "__main__":
    Thread(target=background_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
