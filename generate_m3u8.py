import urllib.request
import xml.etree.ElementTree as ET

# Danh sách Channel ID chuẩn của các giải đấu
LEAGUES = {
    "Premier League": {"channel_id": "UCNAf1k0yIjyGu3k9BwAg3LG", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"channel_id": "UC14UlmYlSNiQCcq9mWb72vg", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"channel_id": "UC6UL29enLNe4xmWfU43qEag", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"channel_id": "UCBJeMCIe9X5aL12cv5ekkgA", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"channel_id": "UCfh1019X3q0iE1YvLw_2Cvg", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"channel_id": "UC2K3J2_m04xJp85u23E0aTQ", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_latest_videos_rss(channel_id, max_results=3):
    """Lấy trực tiếp video mới nhất qua RSS feed public của YouTube (không cần API Key)"""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    videos = []
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req).read()
        root = ET.fromstring(xml_data)
        
        # Namespace XML của Atom feed
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns)[:max_results]:
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:link', ns).attrib['href']
            videos.append({"title": title, "url": link})
    except Exception as e:
        print(f"[-] Lỗi khi lấy RSS cho channel {channel_id}: {e}")
    return videos

def generate_m3u8():
    m3u8_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    total_videos = 0
    
    for league_name, info in LEAGUES.items():
        print(f"[+] Đang cào highlight: {league_name}...")
        videos = get_latest_videos_rss(info["channel_id"], max_results=3)
        
        for video in videos:
            m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}", {video["title"]}\n'
            m3u8_content += f'{video["url"]}\n\n'
            total_videos += 1

    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)
        
    print(f"\n[✓] Hoàn tất! Đã lưu {total_videos} video vào {output_file}")

if __name__ == "__main__":
    generate_m3u8()
