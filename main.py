import requests
import datetime as dt
import smtplib
import time

MY_LAT = 42.460550
MY_LNG = 18.524932


def send_email():
    my_email = "severeff@gmail.com"
    to_email = "egorii@list.ru"
    password = "qgbucfjtkecefapc"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg="Subject:ISS fly above\n\nLook up!"
        )


def iss_above():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    if -5 < MY_LAT - iss_lat < 5 and -5 < MY_LNG - iss_lng < 5:
        return True
    else:
        return False


def is_dark():
    global MY_LAT, MY_LNG
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.datetime.now()

    if sunset <= time_now.hour <= sunrise:
        return True
    else:
        return False


def check_this_out():
    if is_dark():
        if iss_above():
            send_email()
            time.sleep(300)
            check_this_out()
    else:
        time.sleep(3)
        print('not now')
        check_this_out()


check_this_out()
