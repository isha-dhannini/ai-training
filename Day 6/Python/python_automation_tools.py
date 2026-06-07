import os, shutil, pathlib, time, csv
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

EXT_MAP = {
    ".py": "Python",
    ".txt": "Text",
    ".jpg": "Images",
    ".png": "Images",
    ".csv": "CSV"
}

def organise(folder: str):
    src = Path(folder)

    for f in src.iterdir():
        if f.is_file():
            dest = src / EXT_MAP.get(f.suffix, "Other")
            dest.mkdir(exist_ok=True)

            shutil.move(str(f), dest / f.name)
            print(f"Moved {f.name} → {dest.name}/")

organise(r"C:\Users\Administrator\Learnings\ai-training\Day 6")


#---------------- Web scraping ----------------

def scrape_quotes() -> list:
    url = "https://quotes.toscrape.com"
    r = requests.get(url, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")
    quotes = []

    for q in soup.select(".quote")[:5]:
        quotes.append({
            "text": q.find("span", class_="text").text,
            "author": q.find("small").text,
            "scraped_at": datetime.now().isoformat(),
        })

    return quotes


def save_to_csv(rows, path="quotes.csv"):
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["text", "author", "scraped_at"])

        if f.tell() == 0:
            w.writeheader()

        w.writerows(rows)


data = scrape_quotes()
save_to_csv(data)
print(f"Saved {len(data)} quotes")


# ---------------- SMTP EMAIL ----------------

def send_alert(subject: str, body: str, to: str, gmail_user: str, app_pw: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(gmail_user, app_pw)
        s.send_message(msg)

    print("Alert sent ✓")


# ---------------- SCHEDULE ----------------

def job_scrape():
    data = scrape_quotes()
    save_to_csv(data)
    print(f"[{datetime.now():%H:%M:%S}] Scraped {len(data)} rows")


def job_report():
    print(f"[{datetime.now():%H:%M:%S}] Daily report sent")


schedule.every(10).seconds.do(job_scrape)
schedule.every().day.at("08:00").do(job_report)

deadline = time.time() + 35

while time.time() < deadline:
    schedule.run_pending()
    time.sleep(1)


# ---------------- APSCHEDULER ----------------

scheduler = BackgroundScheduler()

scheduler.add_job(job_scrape, "interval", seconds=15, id="scraper")

scheduler.add_job(
    job_report,
    CronTrigger(day_of_week="mon-fri", hour=7, minute=30),
    id="daily_report"
)

scheduler.start()

print("Scheduler running. Jobs:")
for job in scheduler.get_jobs():
    print(f" • {job.id} — next: {job.next_run_time}")

time.sleep(40)
scheduler.shutdown()