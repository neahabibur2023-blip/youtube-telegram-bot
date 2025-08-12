
import os
import requests
import time

# ==== CONFIG ====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHECK_INTERVAL = 300  # প্রতি ৫ মিনিট পর চেক করবে
MAX_RESULTS = 5
# ===============

last_video_id = None

def get_latest_video():
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults={MAX_RESULTS}"
    response = requests.get(url)
    data = response.json()

    for item in data.get("items", []):
        if item["id"]["kind"] == "youtube#video":
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            return video_id, title
    return None, None

def send_to_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

def main():
    global last_video_id
    while True:
        try:
            video_id, title = get_latest_video()
            if video_id and video_id != last_video_id:
                last_video_id = video_id
                video_url = f"https://youtu.be/{video_id}"
                send_to_telegram(f"🎬 নতুন ভিডিও: {title}\n{video_url}")
                print(f"Sent: {title}")
        except Exception as e:
            print("Error:", e)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
