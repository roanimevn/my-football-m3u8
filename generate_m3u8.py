import json
import urllib.request

# Danh sách Channel ID chuẩn của các giải đấu
LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

# Danh sách các Public Invidious API instances (dự phòng nếu 1 server bận)
INVIDIOUS_INSTANCES = [
    "https://inv.hostux.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.drgns.space",
    "https://vid.puppethead.online"
]

def get_latest_videos_invidious(channel_id, limit=3):
    """Lấy danh sách video mới nhất qua Invidious API (Tốc độ cao, không cần API Key)"""
    videos = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for instance in INVIDIOUS_INSTANCES:
        url = f"{instance}/api/v1/channels/videos/{channel_id}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    # Invidious trả về danh sách video dạng list
                    for item in data[:limit]:
                        title = item.get("title", "Football Highlight")
                        video_id = item.get("videoId")
                        if video_id:
                            videos.append({
                                "title": title,
                                "url": f"https://www.youtube.com/watch?v={video_id}"
                            })
                    if videos:
                        break # Đã lấy thành công thì dừng không cần thử instance khác
        except Exception as e:
            print(f"[-] Server {instance} gặp lỗi: {e}. Đang thử server dự phòng...")

    return videos

def generate_m3u8():
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    total_videos = 0

    for league_name, info in LEAGUES.items():
        print(f"[+] Đang cào highlight giải: {league_name}...")
        videos = get_latest_videos_invidious(info["channel_id"], limit=3)

        if videos:
            for video in videos:
                m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
                m3u8_content += f'{video["url"]}\n\n'
                total_videos += 1
            print(f"    -> Thành công lấy {len(videos)} video.")
        else:
            print(f"    [-] Không thể lấy video cho {league_name}.")

    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print(f"\n[✓] Hoàn tất! Tổng cộng đã ghi {total_videos} video vào file {output_file}")

if __name__ == "__main__":
    generate_m3u8()
