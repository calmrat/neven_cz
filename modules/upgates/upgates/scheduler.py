import time

import schedule


def scheduled_sync():
    """Runs full API sync on a schedule."""
    print("🔄 Running scheduled sync...")


schedule.every(30).minutes.do(scheduled_sync)

print("🕒 Scheduled sync initialized.")
while True:
    schedule.run_pending()
    time.sleep(1)
