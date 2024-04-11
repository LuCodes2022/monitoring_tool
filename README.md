# monitoring_tool
This is a simple tool keeping track of your CPU and Memory usage whilst keeping an eye out that memory usage does not exceed 90%, if that were to happen the script will sent a notification email to whomever will be put as the receiver email.
## In progress
- editing this github to get int depth about this script and the cron jobs to run to execute it.

## Gmail set up

if you run this script and want to use a gmail account you will need to make an app password, for some people that is under accountmanagement then security. In my case, I had to look into the search bar of accountmanagement.

![](/assets/app_search.png)

click on it then you may be prompted to log in.

![](/assets/log_in.png)

enter your Gmail password then click continue.

![](/assets/app_name.png)

Give your app a name and there you go! You can now copy paste this password and put it as the EMAIL_PASSWORD variable.

## Setting up your environment
Ensure that the necessary Python libraries are installed and accessible in the environment where the script will run.:
- psutil
- smtplib
- email
Make sure to replace placeholder values with actual email credentials and addresses before deploying the script:
- SENDER_EMAIL
- RECIPIENT_EMAIL
- EMAIL_PASSWORD

Test the script thoroughly in your environment to confirm that it behaves as expected and handles potential errors gracefully.

## But what does the script execute?

write_metrics_to_csv()
- This function collects system metrics including CPU usage and memory usage using the psutil library.
- It retrieves the current timestamp.
- The collected metrics (timestamp, CPU usage percentage, and memory usage percentage) are then appended to a CSV file named hourly_system_metrics.csv.

send_weekly_report()
- This function checks if the current day of the week is Sunday (datetime.datetime.today().weekday() == 6).
- If it's Sunday, it prepares to send a weekly system report.
- The report consists of a subject, body message, and an attached CSV file (hourly_system_metrics.csv).
- It calls the send_email_alert() function to send the email containing the weekly report.

send_email_alert(subject, body, attachment_file=None)
- This function constructs an email message using the email.mime modules.
- It prepares the email subject, sender, recipient, and body message.
- If an attachment_file is provided, it attaches the specified file to the email.
- It establishes a connection to Gmail's SMTP server (smtp.gmail.com on port 587), starts TLS encryption, and logs in using the sender's email credentials.
- The email is then sent using server.sendmail() with the constructed message.
- If successful, it prints a message indicating that the email was sent. If there's an error, it prints the exception message.

main()
- This function serves as the entry point of the script.
- It invokes the write_metrics_to_csv() function to save system metrics to the CSV file.
- It also invokes the send_weekly_report() function to potentially send a weekly report if it's Sunday.

## Test
If you are unsue if the script is able to send out an email you can uncomment the section with the test_email_alert() function and comment out the main() function being called back at the end to make sure you can successfully send emails out.

## What happens when the script is executed:
- The main() function is responsible for triggering the collection of system metrics and potential sending of the weekly report based on the current day of the week.
- When executed, this script will continuously collect system metrics and append them to hourly_system_metrics.csv.
- Additionally, on Sundays, it will attempt to send a weekly report email containing the collected metrics from the CSV file.
- Any errors encountered during the email sending process will be printed to the console for debugging purposes.
- It checks the memory usage does not exceeds 90%, and when it does sends out a warning by email.