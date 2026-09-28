import scrapetube

# Danh sách Channel ID chuẩn của các giải đấu
LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_videos(channel_id, limit=3):
    """Lấy danh sách video mới nhất qua InnerTube API bằng scrapetube (Chống chặn IP)"""
    videos_list = []
    try:
        videos = scrapetube.get_channel(channel_id, limit=limit)
        for video in videos:
            video_id = video.get("videoId")
            
            # Lấy tiêu đề video
            title_runs = video.get("title", {}).get("runs", [])
            title = title_runs[0].get("text") if title_runs else "Highlight Football"
            
            if video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
                videos_list.append({"title": title, "url": url})
    except Exception as e:
        print(f"[-] Lỗi khi cào dữ liệu kênh {channel_id}: {e}")
        
    return videos_list

def generate_m3u8():
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    total_videos = 0
    
    for league_name, info in LEAGUES.items():
        print(f"[+] Đang cào highlight: {league_name}...")
        videos = get_latest_videos(info["channel_id"], limit=3)
        
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
