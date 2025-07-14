# main.py

from fastapi import FastAPI, HTTPException
from calendar_utils import fetch_calendar_data

app = FastAPI(
    title="Persian Calendar API",
    description="نمایش اطلاعات تقویم شمسی با مناسبت‌ها و تعطیلات",
    version="1.0"
)


@app.get("/calendar/{year}/{month}")
def get_calendar(year: int, month: int):
    if year < 1300 or year > 1500:
        raise HTTPException(status_code=400, detail="سال معتبر نیست.")
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="ماه باید بین ۱ تا ۱۲ باشد.")

    try:
        data = fetch_calendar_data(year, month)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
