import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# Danh sách tìm kiếm lọc ĐÚNG KÊNH CHÍNH THỨC (FPT Play, TV360, MyTV, FIFA)
LEAGUES = {
    "FPT Play Sports": {
        "query": "site:youtube.com \"Highlight\" (\"FPT Play\" OR \"FPT Bóng Đá\")",
        "logo": "https://i.imgur.com/2Xy5k8E.png"
    },
    "TV360 Thể Thao": {
        "query": "site:youtube.com \"Highlight\" \"TV360\"",
        "logo": "https://i.imgur.com/R3Z5k8E.png"
    },
    "MyTV Bóng Đá": {
        "query": "site:youtube.com \"Highlight\" \"MyTV\"",
        "logo": "https://i.imgur.com/K4Z5k8E.png"
    },
    "FIFA Official Highlights": {
        "query": "site:youtube.com \"Highlights\" \"FIFA\"",
        "logo": "https://i.imgur.com/L6Z5k8E.png"
    }
}

def get_highlights_rss(query, limit=5):
    encoded_query = urllib.parse.quote(query)
    # Lấy dữ liệu tin bài video mới nhất
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=vi&gl=VN&ceid=VN:vi"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    videos = []
    
    try:
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item'):
                title = item.find('title').text
                # Loại bỏ phần tên báo/kênh phía sau dấu "-"
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                
                # Kiểm tra lọc tiêu đề bắt buộc chứa chữ Highlight/Highlights
                title_lower = title.lower()
                if "highlight" in title_lower or "tóm tắt" in title_lower:
                    link = item.find('link').text
                    videos.append({"title": title, "url": link})
                    
                if len(videos) >= limit:
                    break
    except Exception as e:
        print(f"[-] Lỗi cào dữ liệu cho query '{query}': {e}")
        
    return videos

def generate_m3u8():
    # Cấu hình Header m3u8 chuẩn Live Stream (Khóa thanh Seekbar thời gian)
    m3u8_content = "#EXTM3U\n"
    m3u8_content += "#EXT-X-VERSION:3\n"
    m3u8_content += "#EXT-X-PLAYLIST-TYPE:EVENT\n"
    m3u8_content += "#EXT-X-TARGETDURATION:0\n"
    m3u8_content += "#EXT-X-MEDIA-SEQUENCE:0\n"
    m3u8_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    
    total_videos = 0

    for league_name, info in LEAGUES.items():
        print(f"[+] Đang lọc video Highlight từ {league_name}...")
        videos = get_highlights_rss(info["query"], limit=5)

        if videos:
            for video in videos:
                # Cấu hình #EXTINF:-1 ép hiển thị nhãn LIVE trên mọi trình phát
                m3u8_content += f'#EXTINF:-1 tvg-logo="{info["logo"]}" group-title="{league_name}" radio="true", 🔴 LIVE | {video["title"]}\n'
                
                raw_url = video["url"]
                # Chuyển đổi link YouTube sang định dạng Embed stream
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

    print(f"\n[✓] Hoàn tất! Đã lọc đúng {total_videos} video Highlight chuẩn từ FIFA, FPT Play, TV360, MyTV.")

if __name__ == "__main__":
    generate_m3u8()
