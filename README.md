Overview
This project automates the process of sending emails to multiple recipients listed in a CSV file. You provide your Gmail credentials and upload a CSV file containing the email addresses. The bot will send the same email to all recipients in the file.

Installation
To run this project, install the required libraries by executing the following command in your terminal:

bash
Copy code
pip install flask pandas smtplib email-validator
Features
Upload a CSV file with recipient email addresses.
Automate sending emails to all listed recipients with a single message.
How It Works
Input your Gmail credentials securely.
Upload the CSV file containing recipient email addresses.
The bot sends the specified email to all recipients in the file.
