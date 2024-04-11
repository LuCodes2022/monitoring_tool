#!/usr/bin/env python3
import psutil
import curses
import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Constants for email configuration
SENDER_EMAIL = "enter_your_sender_email_here"
RECIPIENT_EMAIL = "enter_your_recipient_email_here"
EMAIL_PASSWORD = "enter_your_password_here"

# Function to write system metrics to CSV file
def write_metrics_to_csv():
    cpu_percent = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('weekly_system_metrics.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu_percent, mem.percent])

    # Check if it's the end of the week (Sunday) to send the weekly report
    if datetime.datetime.today().weekday() == 6:  # 6 represents Sunday
        send_email_alert("Weekly System Report", "Please find attached the weekly system metrics report.", "weekly_system_metrics.csv")

# Function to send email alert or report
def send_email_alert(subject, body, attachment_file=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_file:
        # Attach the file
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {attachment_file}")
            msg.attach(part)

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)

        # Send the email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email sent successfully!")
        return True  # Email sent successfully
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False  # Failed to send email
    finally:
        server.quit()

# Function to display system metrics using curses
def display_metrics(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # Hide cursor

    while True:
        stdscr.addstr(0, 0, "Weekly System Metrics (Press q to quit)")
        stdscr.addstr(2, 0, "Timestamp                CPU Usage (%)    Memory Usage (%)")
        stdscr.addstr(3, 0, "-" * curses.COLS)  # Horizontal line

        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Display metrics
        stdscr.addstr(4, 0, f"{timestamp}")
        stdscr.addstr(4, 24, f"{cpu_percent:^15.2f}")
        stdscr.addstr(4, 42, f"{mem.percent:^17.2f}")

        stdscr.refresh()

        # Write metrics to CSV every minute
        write_metrics_to_csv()

        # Check for critical memory usage and send email alert
        if mem.percent > 90:
            send_email_alert("Memory Usage Alert", "Memory usage is critical!")

        # Check for user input to quit
        key = stdscr.getch()
        if key == ord('q'):
            break

# Function to test email sending functionality
def test_email_alert():
    email_sent = send_email_alert("Test Email", "This is a test email sent from the system monitoring script.")

    if email_sent:
        print("Test email sent successfully!")
    else:
        print("Failed to send test email. Check the console for details.")

# Main function
def main():
    # Initialize curses
    curses.wrapper(display_metrics)

if __name__ == "__main__":
     main()
