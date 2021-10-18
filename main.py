import requests
from datetime import datetime
import smtplib
import time

# enter your latitude and longitude into below fields
MY_LATITUDE = 0
MY_LONGITUDE = 0

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

lat = float(data["iss_position"]["latitude"])
lng = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LATITUDE,
    "lng": MY_LONGITUDE,
    "formatted": 0
}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data_sunrise_sunset = response.json()["results"]
sunrise = int(data_sunrise_sunset["sunrise"].split("T")[1].split(":")[0])
sunset = int(data_sunrise_sunset["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now().hour

while True:
    time.sleep(60)
    if parameters["lat"] >= lat - 5 and parameters["lat"] <= lat + 5 and parameters["lng"] >= lng - 5 and parameters["lng"] <= lng + 5:
        if time_now >= sunset or time_now <= sunrise:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                # fill in fields belong for user and from and to addresses
                connection.login(user="test@gmail.com", password="create_password()")
                connection.sendmail(fromadr="test@gmail.com",
                                    to_addrs="test2@gmail.com",
                                    msg="Subject: Look Up!\n\nThe ISS space station is near your location! can you spot it?")
