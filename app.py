from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def email_bot():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'csv_file' not in request.files:
            flash("No file uploaded!", "error")
            return redirect(url_for('email_bot'))

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash("No file selected!", "error")
            return redirect(url_for('email_bot'))

        # Save the file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
        csv_file.save(file_path)

        # Get email credentials and subject/body
        sender_email = request.form['sender_email']
        sender_password = request.form['sender_password']
        subject = request.form['subject']
        body = request.form['body']

        try:
            # Process the CSV file
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                recipient_email = row['email']  # Ensure the CSV file has an 'email' column
                personalized_body = body.format(name=row.get('name', ''))  # Optional personalization
                if not send_email(sender_email, sender_password, recipient_email, subject, personalized_body):
                    flash(f"Failed to send email to {recipient_email}", "error")
            
            flash("Emails sent successfully!", "success")
        except Exception as e:
            flash(f"Error processing the file: {e}", "error")
        finally:
            # Remove the uploaded file after processing
            os.remove(file_path)

    return render_template('email_bot.html')


if __name__ == "__main__":
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
