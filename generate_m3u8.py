import os
from googleapiclient.discovery import build

# Lấy API Key từ GitHub Secrets
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_highlights(youtube, channel_id, max_results=3):
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            q="highlight",
            order="date",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            # Link định dạng phát chuẩn YouTube mở được trên mọi trình phát IPTV/VLC
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({"title": title, "url": url})
        return videos
    except Exception as e:
        print(f"[-] Lỗi API cho channel {channel_id}: {e}")
        return []

def generate_m3u8():
    if not YOUTUBE_API_KEY:
        print("[!] Thiếu YOUTUBE_API_KEY trong Secrets.")
        return

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    
    total_videos = 0
    for league_name, info in LEAGUES.items():
        print(f"[+] Đang cào highlight: {league_name}...")
        videos = get_latest_highlights(youtube, info["channel_id"], max_results=2)
        
        for video in videos:
            m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
            m3u8_content += f'{video["url"]}\n\n'
            total_videos += 1

    # Tạo file bất kể có dữ liệu hay không
    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)
        
    print(f"[✓] Đã tạo thành công {output_file} với {total_videos} video!")

if __name__ == "__main__":
    generate_m3u8()
