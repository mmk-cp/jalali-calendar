from fastapi import FastAPI
import requests

from fullCalendar import fetch_calendar_structure
from timeIrApi import get_month_events_and_holidays

app = FastAPI()


def get_month_holidays_unofficial(year, month):
    holidays = []
    for day in range(1, 32):
        try:
            url = f"https://holidayapi.ir/jalali/{year}/{month:02}/{day:02}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_holiday") or data.get("event"):
                    holidays.append(data)
        except Exception as e:
            pass  # skip not valid day
    return holidays


@app.get('/calendar/{year}/{month}')
def index(year: int, month: int):
    data = get_month_events_and_holidays(year, month)
    full = fetch_calendar_structure(year, month)

    result = {
        "data": data,
        "full": full,
        "year": year,
        "month": month,
    }
    return result
