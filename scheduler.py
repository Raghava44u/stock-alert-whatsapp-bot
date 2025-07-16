import schedule
import time
from send_whatsapp import send_whatsapp_message

def job():
    print("📡 Running stock alert bot...")
    send_whatsapp_message()
    print("✅ Message sent.")

schedule.every().day.at("07:30").do(job)
print("📅 Scheduler started. Waiting for the scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(60)
