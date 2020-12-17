from datetime import datetime
from notify_run import Notify

import requests
import sys


BASE_URL = "https://www.ah.nl/service/rest/delegate?url=%2Fkies-moment%2Fbezorgen%2F$"


def find_slots(zipcode: str):
    result = requests.get(BASE_URL + zipcode)
    data = result.json()

    cur_week = datetime.now().isocalendar()[1]

    data = data.get("_embedded").get("lanes")[3].get("_embedded").get("items")[0].get("_embedded")
    total_slots = 1
    for day in data.get("deliveryDates"):
        date = datetime.strptime(day['date'], "%Y-%m-%d")
        if date.isocalendar()[1] == cur_week:
            r = 0
            for slot in day['deliveryTimeSlots']:
                if slot['state'] != "full":
                    r += 1
            total_slots += r
            # print(day["date"] + ": " + str(r) + " slots")

    if total_slots > 0:
        notify = Notify()
        if notify.config_file_exists:
            notify.read_config()
        else:
            print(notify.register())
            notify.write_config()
        notify.send("AH Bezorg slots beschikbaar", "https://www.ah.nl")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "info":
        notify = Notify()
        notify.read_config()
        print(notify.info())
    else:
        find_slots("7513DB")
