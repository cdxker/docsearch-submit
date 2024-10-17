import os
from flask import Flask, request, jsonify, Response, redirect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# SMTP configuration
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)

@app.route('/health')
def health():
    return Response(status=200)

@app.route('/')
def home():
    return redirect("https://trieve.ai/sitesearch")
    

@app.route('/submit', methods=['POST'])
def submit_info():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    website = data.get('website')
    
    # Compose email body
    email_body = f"New Docsearch submission:\nName: {name}\nEmail: {email}\nWebsite: {website}"
    
    try:
        send_email("💚💚💚Docsearch submission💚💚💚", email_body)
        return Response(status=204)
    except Exception as e:
        return Response(status=204)

if __name__ == '__main__':
    app.run(debug=True)
