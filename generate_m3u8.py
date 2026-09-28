import os
from googleapiclient.discovery import build

# Lấy YOUTUBE_API_KEY tự động từ GitHub Secrets
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Danh sách Upload Playlist ID chuẩn của các kênh giải đấu chính thức (Đầu mã UU...)
LEAGUES = {
    "Premier League": {"playlist_id": "UUNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"playlist_id": "UU14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"playlist_id": "UU6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"playlist_id": "UUBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"playlist_id": "UUfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"playlist_id": "UU2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_videos(youtube, playlist_id, max_results=3):
    """Lấy danh sách video mới nhất từ Upload Playlist thông qua YouTube Data API v3"""
    videos = []
    try:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            title = snippet.get("title", "Football Highlight")
            video_id = snippet.get("resourceId", {}).get("videoId", "")
            
            if video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append({"title": title, "url": url})
    except Exception as e:
        print(f"[-] Lỗi khi gọi API cho playlist {playlist_id}: {e}")
    return videos

def generate_m3u8():
    if not YOUTUBE_API_KEY:
        print("[!] Không tìm thấy YOUTUBE_API_KEY trong Secrets. Vui lòng kiểm tra lại cấu hình GitHub Secrets!")
        return

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    total_videos = 0

    for league_name, info in LEAGUES.items():
        print(f"[+] Đang lấy video mới nhất: {league_name}...")
        videos = get_latest_videos(youtube, info["playlist_id"], max_results=3)

        for video in videos:
            m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
            m3u8_content += f'{video["url"]}\n\n'
            total_videos += 1

    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print(f"\n[✓] Hoàn tất! Đã cập nhật thành công {total_videos} video vào {output_file}")

if __name__ == "__main__":
    generate_m3u8()
