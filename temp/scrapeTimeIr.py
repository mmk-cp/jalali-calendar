import requests
from bs4 import BeautifulSoup
import urllib3

# for problem for ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.time.ir/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(response.content, "html.parser")

events_container = soup.find("div", class_="EventList_root__events__container__6bHdH")
if not events_container:
    print("Event container not found.")
    exit()

events = events_container.find_all("div", class_="EventListItem_root__pHV2b")

for event in events:
    date_span = event.find("span", class_="EventListItem_root__date__UUgtf")
    event_span = event.find("span", class_="EventListItem_root__event__XrjoV")
    extra_span = event.find("span", class_="EventListItem_root__otherBase__8Sksv")

    is_holiday = False
    if date_span and 'holiday' in ' '.join(date_span.get('class', [])):
        is_holiday = True
    if event_span and 'holiday' in ' '.join(event_span.get('class', [])):
        is_holiday = True

    date = date_span.get_text(strip=True) if date_span else ""
    event_text = event_span.get_text(strip=True) if event_span else ""
    extra = extra_span.get_text(strip=True) if extra_span else ""

    print(f"{date} - {event_text}" + (f" ({extra})" if extra else "") + (" [Holiday]" if is_holiday else ""))
