from rest_framework.decorators import api_view
from rest_framework.response import Response
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import certifi


def send_mail(receiver_email, message_data):
    # Email information
    sender_email = 'UWEFlixCinema@gmail.com'
    # receiver_email = 'UWEFlixCinema@gmail.com'
    password = ''
    subject = f'Order Summary - {message_data["id"]}'
    body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Summary</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}

        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
        }}

        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .summary {{
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #dee2e6;
            margin-bottom: 20px;
        }}

        .summary h3 {{
            margin-top: 0;
        }}

        .summary table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .summary th, .summary td {{
            border: 1px solid #dee2e6;
            padding: 8px;
            text-align: left;
        }}

        .summary th {{
            background-color: #e9ecef;
        }}

        .footer {{
            text-align: center;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>UWEFlix Cinema</h1>
            <h2>Order Summary</h2>
        </div>
        <div class="summary">
            <h3>Booking Details</h3>
            <table>
                <tr>
                    <th>Booking ID</th>
                    <td>{message_data['id']}</td>
                </tr>
                <tr>
                    <th>Movie</th>
                    <td>{message_data['movie']}</td>
                </tr>
                <tr>
                    <th>Date</th>
                    <td>{message_data['date']}</td>
                </tr>
                <tr>
                    <th>Screen</th>
                    <td>{message_data['screen']}</td>
                </tr>
                <tr>
                    <th>Tickets</th>
                    <td>{message_data['total_tickets']}</td>
                </tr>
                <tr>
                    <th>Total Price</th>
                    <td>£{message_data['total_price']}</td>
                </tr>
            </table>
        </div>
        <div class="footer">
            <p>Thank you for booking with us!</p>
            <p>© 2023 UWEFlix. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

    # Create a multipart message and set the headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    

    # Add body to the message
    # message.attach(MIMEText(body, 'plain'))
    message.attach(MIMEText(body, 'html'))

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print('Email sent successfully')
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        server.quit()

@api_view(['POST'])
def my_view(request):
    data = request.data
    # Do something with the data
    print(data)
    send_mail(data['email'], data)
    return Response(data)