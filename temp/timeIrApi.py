import requests
from collections import defaultdict


def get_month_events_and_holidays(year, month):
    url = "https://api.time.ir/v1/event/fa/events/calendar"
    headers = {
        "x-api-key": "ZAVdqwuySASubByCed5KYuYMzb9uB2f7",
        "accept": "application/json",
        "referer": "https://www.time.ir/",
        "origin": "https://www.time.ir",
        "user-agent": "Mozilla/5.0",
    }
    params = {
        "year": year,
        "month": month,
        "day": 0,
        "base1": 0,
        "base2": 1,
        "base3": 2,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()["data"]

    days = defaultdict(lambda: {"date_string": "", "events": [], "is_official_holiday": False})

    for d in data["day_list"]:
        index = d["index_in_base1"]
        if d["enabled"]:
            days[index]["is_official_holiday"] = d["is_holiday"]

    for event in data["event_list"]:
        day = event["jalali_day"]
        days[day]["date_string"] = event["date_string"]
        days[day]["events"].append({
            "title": event["title"],
            "is_holiday_event": event["is_holiday"]
        })

    sorted_days = sorted(days.items(), key=lambda x: x[0])
    return sorted_days


# events = get_month_events_and_holidays(1404, 3)
# print(events)

#
# for day, info in events:
#     print(f"{info['date_string']} {'[تعطیل رسمی]' if info['is_official_holiday'] else ''}:")
#     for event in info["events"]:
#         prefix = "[تعطیل مناسبتی] " if event["is_holiday_event"] else ""
#         print(f"  - {prefix}{event['title']}")


def prettier_event(events):
    result = ""
    for day, info in events:
        result += f"{info['date_string']} {'[تعطیل رسمی]' if info['is_official_holiday'] else ''}:"
        for event in info["events"]:
            prefix = "[تعطیل مناسبتی] " if event["is_holiday_event"] else ""
            result += f"  - {prefix}{event['title']}"

        result += "\n"

    return result
