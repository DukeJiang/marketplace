import os, datetime, json
import requests
import logging 
from flask import Flask

app = Flask(__name__)


#------------------------------------------------------------------------
#------------------------------------------------------------------------


@app.route("/tasks/health")
def health():
  response = requests.get('https://finalproject-351111.uc.r.appspot.com/market/all_listings')
  if response.status_code == 200:
    print('success')
    domain = 'sandbox710fe2f63bce4b799d2b86489b8c1831.mailgun.org'
    target_email = 'yuxuanjiang@uchicago.edu'
    api_key = '228ed7defc0cbfc1ef40a293701590e4-fe066263-341225ea'
    requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": f"Duke Jiang <dukejiang@{domain}>",
              "to": [f"{target_email}"],
              "subject": "👍 Health Check - https://finalproject-351111.uc.r.appspot.com/market/all_listings ",
              "text": "market endpoints healthy!"})
    logging.log(1, f"health check task performed")
    return "market endpoints healthy", 200
  else:
    print('fail')
    domain = 'sandbox710fe2f63bce4b799d2b86489b8c1831.mailgun.org'
    target_email = 'yuxuanjiang@uchicago.edu'
    api_key = '228ed7defc0cbfc1ef40a293701590e4-fe066263-341225ea'
    requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": f"Duke Jiang <dukejiang@{domain}>",
              "to": [f"{target_email}"],
              "subject": "🙅 Health Check - https://finalproject-351111.uc.r.appspot.com/market/all_listings ",
              "text": "Market endpoints down🙅!"})
    return "market endpoints failed", 400


if __name__ == '__main__':
  app.run(debug=True)
