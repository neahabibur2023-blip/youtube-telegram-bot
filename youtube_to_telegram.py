import os
import requests
import time

# Environment Variables থেকে মান নেওয়া
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

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

# মেইন ফাংশন
def main():
    last_video = None
    while True:
        try:
            title, video_url = get_latest_video()
            if title and video_url and video_url != last_video:
                send_to_telegram(f"📢 New video uploaded: {title}\n{video_url}")
                last_video = video_url
            time.sleep(300)  # প্রতি 5 মিনিটে চেক করবে
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
