import os
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_videos(youtube, channel_id, max_results=3):
    videos = []
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results
        )
        response = request.execute()

        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            if video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append({"title": title, "url": url})
    except Exception as e:
        print(f"[-] Lỗi khi gọi API cho channel {channel_id}: {e}")
    return videos

def generate_m3u8():
    if not YOUTUBE_API_KEY:
        print("[!] Không tìm thấy YOUTUBE_API_KEY trong Secrets.")
        return

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    total_videos = 0

    for league_name, info in LEAGUES.items():
        print(f"[+] Đang lấy video: {league_name}...")
        videos = get_latest_videos(youtube, info["channel_id"], max_results=3)

        for video in videos:
            m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
            m3u8_content += f'{video["url"]}\n\n'
            total_videos += 1

    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print(f"\n[✓] Hoàn tất! Đã lưu {total_videos} video vào file {output_file}")

if __name__ == "__main__":
    generate_m3u8()
