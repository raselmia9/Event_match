import json
import urllib.request
from datetime import datetime

SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Upcoming-and-Live-Sports-Data/refs/heads/main/Sports_data.json"
OUTPUT_FILE = "matches.json"

def fetch_and_convert():
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    converted = []
    matches = data.get("matches", [])

    for m in matches:
        ev_info = m.get("eventInfo", {})
        cat = m.get("Category", "").strip()
        ev_name = ev_info.get("eventName", "").strip()

        if cat and ev_name and cat.lower() not in ev_name.lower():
            event_title = f"{cat.upper()} | {ev_name}"
        else:
            event_title = ev_name or m.get("event_name", "").strip()

        start_time_raw = ev_info.get("startTime", "").strip()
        try:
            dt = datetime.strptime(start_time_raw, "%d/%m/%Y %I:%M:%S %p")
            match_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            match_time = start_time_raw

        team1_title = ev_info.get("teamA", "").strip()
        team2_title = ev_info.get("teamB", "").strip()
        team1_logo = ev_info.get("teamAFlag", "").strip()
        team2_logo = ev_info.get("teamBFlag", "").strip()

        stream_parts = []
        for s in m.get("streams", []):
            url = s.get("stream_url", "").strip()
            if not url:
                continue
            cname = s.get("channel_name", "").strip()

            headers = []
            if s.get("referer"):
                headers.append(f"Referer={s['referer']}")
            if s.get("user_agent"):
                headers.append(f"User-Agent={s['user_agent']}")

            header_str = ("|" + "|".join(headers)) if headers else ""
            stream_parts.append(f"{cname},,{url}{header_str}")

        stream_link = ",) ".join(stream_parts)
        is_hot = (m.get("status", "").upper() == "LIVE")

        item = {
            "eventTitle": event_title,
            "matchTime": match_time,
            "team1Logo": team1_logo,
            "team2Logo": team2_logo,
            "team1Title": team1_title,
            "team2Title": team2_title,
            "streamLink": stream_link,
            "isHot": is_hot
        }
        converted.append(item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, indent=4, ensure_ascii=False)

    print(f"Successfully converted {len(converted)} matches to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_convert()
