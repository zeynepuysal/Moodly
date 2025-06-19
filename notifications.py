import time
from plyer import notification
from mac_notifications import client
import sys
import schedule

def send_notification_windows():
    """Send notification"""
    notification.notify(
        title="Remainder",
        message="Please enter your mood",
        timeout=10 # display notification by 10 seconds
    )

def send_notification_mac():
    client.create_notification(
        title="Remainder",
        subtitle="Please enter your mood"
    )

def run_scheduler():
    print("Running...")
    if sys.platform == 'darwin':
        schedule.every().day.at("17:50").do(send_notification_mac)
        schedule.every().day.at("17:52").do(send_notification_mac)
    else:
        schedule.every().day.at("17:50").do(send_notification_windows)
        schedule.every().day.at("17:52").do(send_notification_windows)

    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    run_scheduler()

if __name__ == "__main__":
    main()