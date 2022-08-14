from re import sub
import requests
import json
import time
import smtplib
import ssl
from dotenv import load_dotenv
import os


load_dotenv("keys.env")
IP = f"http://{os.getenv('IPV4')}:{os.getenv('PORT')}/updatewallpaper"
NUMBER = os.getenv("PHONENUM")
TOKEN = os.getenv("TOKEN")
def main():
    print("STARTED")
    payload = {"access_token": TOKEN}
    req = requests.get('https://pasco.instructure.com/api/v1/users/self/todo_item_count', params=payload)
    req = req.json()
    itemsneeded = req['assignments_needing_submitting']
    while True:
        time.sleep(10)
        payload = {"access_token": TOKEN}
        try:
            req = requests.get('https://pasco.instructure.com/api/v1/users/self/todo_item_count', params=payload)
            req = req.json()
        except:
            print("RATELIMITED")
            time.sleep(60)
            continue
        try:
            if req['assignments_needing_submitting'] < itemsneeded:
                itemsneeded = req['assignments_needing_submitting']
                send_message("Assignment Complete")
                try:
                    requests.get(IP)
                except:
                    print("Computer Offline")
            elif req['assignments_needing_submitting'] > itemsneeded:
                itemsneeded = req['assignments_needing_submitting']
                send_message("/ Assignment Created")
                try:
                    requests.get(IP)
                except:
                    print("Computer Offline")
        except:
            print(req)
            continue

def send_message(subj):
    print("SENDING MESSAGE")
    SMTP_SERVER, SMTP_PORT = "smtp.gmail.com", 587
    # sender_email, email_password = ("austinscodeautomated@outlook.com", "N98M28Pea52mD*d#")
    sender_email, email_password = (os.getenv("SMPTEMAIL"), os.getenv("SMPTPASS"))

    email_message = f"From:{os.getenv('SMPTEMAIL')}\nSubject:{subj}\nTo:{NUMBER}\nPlease update wallpaper"
    with smtplib.SMTP(
        SMTP_SERVER, SMTP_PORT
    ) as email:
        email.ehlo()
        email.starttls(context=ssl.create_default_context())
        email.ehlo()
        email.login(sender_email, email_password)
        email.sendmail(sender_email, NUMBER, email_message)
    print("SENT")






if __name__ == "__main__":
    main()