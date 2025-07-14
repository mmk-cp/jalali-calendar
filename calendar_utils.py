# calendar_utils.py

import os
import json
import requests
import jdatetime

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

PERSIAN_WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]


def get_jalali_month_days(year, month):
    for day in range(31, 27, -1):
        try:
            jdatetime.date(year, month, day)
            return day
        except ValueError:
            continue
    return 27


def load_from_cache(year, month):
    path = os.path.join(CACHE_DIR, f"calendar_{year}_{month}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_to_cache(year, month, data):
    path = os.path.join(CACHE_DIR, f"calendar_{year}_{month}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_calendar_data(year: int, month: int):
    cached = load_from_cache(year, month)
    if cached:
        return cached

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

    day_info_map = {}
    for d in data["day_list"]:
        if not d["enabled"]:
            continue
        day_num = d["index_in_base1"]
        weekday_index = jdatetime.date(year, month, day_num).weekday()
        weekday_name = PERSIAN_WEEKDAYS[weekday_index]
        day_info_map[day_num] = {
            "day": day_num,
            "weekday": weekday_name,
            "is_holiday": d["is_holiday"],
            "occasion": None
        }

    for event in data["event_list"]:
        day = event["jalali_day"]
        if day not in day_info_map:
            continue
        if event["is_holiday"]:
            day_info_map[day]["is_holiday"] = True
            if not day_info_map[day]["occasion"]:
                day_info_map[day]["occasion"] = event["title"]
        elif not day_info_map[day]["occasion"]:
            day_info_map[day]["occasion"] = None

    first_day_index = jdatetime.date(year, month, 1).weekday()
    start_index = (first_day_index + 2) % 7

    weeks = []
    week = [None] * start_index
    total_days = get_jalali_month_days(year, month)

    for day in range(1, total_days + 1):
        day_data = day_info_map.get(day)
        week.append(day_data)
        if len(week) == 7:
            weeks.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)

    month_name = next(
        (m["month_title"] for base in data["calendar_detail_list"] if base["base"] == 0
         for m in base["month_list"] if m["month_index"] == month),
        f"ماه {month}"
    )

    result = {
        "year": year,
        "month": month_name,
        "weeks": weeks
    }

    save_to_cache(year, month, result)
    return result
