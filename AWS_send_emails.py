import boto3
from botocore.exceptions import ClientError
import MySQLdb
import sched
import time
from datetime import datetime

# Checks for updates in database and sends email if necessry
def checkForUpdates():
    print(str(datetime.now()) + " - Checking for updates")
    
    # Schedule new check
    scheduler.enter(10, 1, checkForUpdates, ())
    
    # Connect to database
    conn = MySQLdb.connect("localhost", "phpmyadmin1", "internetoflaundry", "mqtt_data")
    conn.begin()
    
    # Check for new entries
    c = conn.cursor()
    c.execute("SELECT address, name, machine, id FROM email_notifications WHERE sent = 1 order by id desc limit 1;")
    res = c.fetchall()
    
    
    # If new entries found, send email
    if len(res) > 0:
        email = res[0][0]
        name = res[0][1]
        machine = res[0][2]
        id = res[0][3]

        print(str(datetime.now()) + " - Will send email to " + name + " at address " + email + " for machine " + str(machine) + " (id: " + str(id) + ").")
        
        # Email settings associated with AWS SES
        SENDER = "internetoflaundry@gmail.com"
        RECIPIENT = email
        AWS_REGION = "us-west-2"
        SUBJECT = "Your laundry in machine " + str(machine) + " is done!"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Internet of Laundry Notification")

        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>Internet of Laundry Notification</h1>    
        <p>Dear """ + name + """,<br><br>Please come pick up your laundry from machine """ + str(machine) + """.
        <br><br>Best,<Br>Internet of Laundry</p>
        </body>
        </html>
        """            

        CHARSET = "UTF-8"
        client = boto3.client('ses',region_name=AWS_REGION)

        try:
            #Provide the contents of the email.
            response = client.send_email(
            Destination={
            'ToAddresses': [
            RECIPIENT,
            ],
            },
            Message={
            'Body': {
            'Html': {
            'Charset': CHARSET,
            'Data': BODY_HTML,
            },
            'Text': {
            'Charset': CHARSET,
            'Data': BODY_TEXT,
            },
            },
            'Subject': {
            'Charset': CHARSET,
            'Data': SUBJECT,
            },
            },
            Source=SENDER,
            )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        
        print(str(datetime.now()) + " - Will update status.")
        
        try:
            c.execute("""UPDATE email_notifications SET sent = 2 WHERE id = %s""", (id,))
            conn.commit()
        except Error as error:
            print(error)
    try:    
        conn.close()
    except Error as error:
        print(error)
    
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(10, 1, checkForUpdates, ())
print(str(datetime.now()) + " - Start running...")
scheduler.run()

