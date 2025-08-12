import os
import requests
import time
from flask import Flask
from threading import Thread

# Flask App
app = Flask(__name__)

# Environment Variables (Render এ সেট করা থাকবে)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7874904494:AAH-MrzRbbBXPqsR66MT3N6dHTikdrc2L4I")
CHAT_ID = os.getenv("CHAT_ID", "5942277435")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyBOLnfr4geGr7rglTtTKVLugn0KaDfNtkE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "UC3GqJxjrfoMcH44hXp8a9gA")

# ইউটিউব API দিয়ে নতুন ভিডিও পাওয়ার ফাংশন
def get_latest_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults=1"
    response = requests.get(url)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        latest_video = data["items"][0]
        video_id = latest_video["id"]["videoId"]
        title = latest_video["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return title, video_url
    return None, None

# Telegram-এ মেসেজ পাঠানোর ফাংশন
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

# ব্যাকগ্রাউন্ডে নতুন ভিডিও চেক করা
def background_worker():
    last_video = None
    while True:
        try:
            title, video_url = get_latest_video()
            if title and video_url and video_url != last_video:
                send_to_telegram(f"📢 New video uploaded: {title}\n{video_url}")
                last_video = video_url
            time.sleep(300)  # প্রতি ৫ মিনিটে চেক করবে
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

@app.route("/")
def home():
    return "YouTube to Telegram Bot is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    Thread(target=background_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=port)
