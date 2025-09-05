# src/reminder_system.py

import pandas as pd
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import schedule
import time

# Load environment variables
load_dotenv()

def send_reminder_email(recipient_email, subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not all([sender_email, sender_password, recipient_email]):
        print("🛑 Email credentials or recipient not found. Skipping email.")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"✉️ Reminder email sent to {recipient_email}")
    except Exception as e:
        print(f"🛑 Failed to send email: {e}")

def check_appointments_and_send_reminders():
    print(f"\n--- Running Daily Reminder Check at {datetime.now()} ---")
    script_dir = os.path.dirname(__file__)
    schedule_path = os.path.join(script_dir, '..', 'data', 'doctor_schedules.xlsx')
    patients_path = os.path.join(script_dir, '..', 'data', 'patients.csv')

    try:
        schedule_df = pd.read_excel(schedule_path)
        patients_df = pd.read_csv(patients_path)
    except FileNotFoundError:
        print("🛑 Schedule or patient file not found. Aborting reminder check.")
        return

    today = datetime.now().date()
    schedule_df['Date'] = pd.to_datetime(schedule_df['Date'], errors='coerce').dt.date
    upcoming_appointments = schedule_df[
        (schedule_df['Status'] == 'Booked') &
        (schedule_df['Date'] >= today)
    ].copy()

    if upcoming_appointments.empty:
        print("No upcoming appointments to send reminders for.")
        return

    date_series = pd.to_datetime(upcoming_appointments['Date'])
    today_datetime = pd.to_datetime(today)
    upcoming_appointments['DaysUntil'] = (date_series - today_datetime).dt.days

    # 1st Reminder - 7 days before
    first_reminder_appointments = upcoming_appointments[upcoming_appointments['DaysUntil'] == 7]
    for _, row in first_reminder_appointments.iterrows():
        subject = "Reminder: Your Upcoming Appointment"
        body = "This is a friendly reminder of your upcoming appointment. We look forward to seeing you!"
        recipient = os.getenv("RECEIVER_EMAIL")
        send_reminder_email(recipient, subject, body)

    # 2nd & 3rd Reminder - 3 and 1 day before
    interactive_reminder_appointments = upcoming_appointments[upcoming_appointments['DaysUntil'].isin([3, 1])]
    for _, row in interactive_reminder_appointments.iterrows():
        subject = "Action Required: Please Confirm Your Upcoming Appointment"
        body = (
            "This is a reminder for your upcoming appointment. Please take a moment to confirm your visit.\n\n"
            "1. Have you filled out the new patient forms?\n"
            "2. Please reply to this email with 'CONFIRMED' to confirm your attendance. "
            "If you need to cancel, please state the reason.\n\n"
            "Thank you!\nMediCare Allergy & Wellness Center"
        )
        recipient = os.getenv("RECEIVER_EMAIL")
        send_reminder_email(recipient, subject, body)

    print("--- Daily Reminder Check Complete ---")

if __name__ == "__main__":
    schedule.every(15).seconds.do(check_appointments_and_send_reminders)
    print("✅ Reminder system is running. It will check for appointments every 15 seconds for testing.")
    print("Press Ctrl+C to exit.")

    check_appointments_and_send_reminders()

    while True:
        schedule.run_pending()
        time.sleep(1)
