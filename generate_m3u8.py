import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

LEAGUES = {
    "Premier League": {"query": "site:youtube.com Premier League Highlights", "logo": "https://i.imgur.com/2Xy5k8E.png"},
    "La Liga": {"query": "site:youtube.com La Liga Highlights", "logo": "https://i.imgur.com/R3Z5k8E.png"},
    "Bundesliga": {"query": "site:youtube.com Bundesliga Highlights", "logo": "https://i.imgur.com/K4Z5k8E.png"},
    "Serie A": {"query": "site:youtube.com Serie A Highlights", "logo": "https://i.imgur.com/M5Z5k8E.png"},
    "UEFA Champions League": {"query": "site:youtube.com Champions League Highlights", "logo": "https://i.imgur.com/L6Z5k8E.png"},
    "MLS": {"query": "site:youtube.com MLS Highlights", "logo": "https://i.imgur.com/P7Z5k8E.png"}
}

def get_highlights_rss(query, limit=3):
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    videos = []
    
    try:
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:limit]:
                title = item.find('title').text
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                
                link = item.find('link').text
                videos.append({"title": title, "url": link})
    except Exception as e:
        print(f"[-] Lỗi cào dữ liệu cho query '{query}': {e}")
        
    return videos

def generate_m3u8():
    # Cấu hình Header m3u8 chuẩn Live Stream (Xóa bỏ thanh Seekbar thời gian)
    m3u8_content = "#EXTM3U\n"
    m3u8_content += "#EXT-X-VERSION:3\n"
    m3u8_content += "#EXT-X-PLAYLIST-TYPE:EVENT\n"
    m3u8_content += "#EXT-X-TARGETDURATION:0\n"
    m3u8_content += "#EXT-X-MEDIA-SEQUENCE:0\n"
    m3u8_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    
    total_videos = 0

    for league_name, info in LEAGUES.items():
        print(f"[+] Đang xử lý: {league_name}...")
        videos = get_highlights_rss(info["query"], limit=3)

        if videos:
            for video in videos:
                # Ép thời lượng về -1 và nhúng thẻ live-stream
                m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}" radio="true", 🔴 LIVE | {video["title"]}\n'
                
                # Chuyển đổi link YouTube sang định dạng stream embed trực tiếp cho trình phát
                raw_url = video["url"]
                if "watch?v=" in raw_url:
                    video_id = raw_url.split("watch?v=")[1].split("&")[0]
                    stream_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
                else:
                    stream_url = raw_url
                    
                m3u8_content += f'{stream_url}\n\n'
                total_videos += 1

    output_file = "highlight_football.m3u8"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m3u8_content)

    print(f"\n[✓] Đã tạo thành công {total_videos} kênh Live chuẩn HLS!")

if __name__ == "__main__":
    generate_m3u8()
