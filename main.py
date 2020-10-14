
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import time
from keep_alive import keep_alive


sessionIdUrl = 'https://share2.dexcom.com/ShareWebServices/Services/General/LoginPublisherAccountByName'
glucoseUrl = 'https://share2.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues?sessionID='  # noqa:E501
glucoseGetParams = '&minutes=1440&maxCount=36'
handler = urllib.request.HTTPHandler()
opener = urllib.request.build_opener(handler)


def get_data(sessionID):
    method = "POST"
    getGlucoseUrl = glucoseUrl + sessionID + glucoseGetParams
    print(getGlucoseUrl)
    glucoseRequest = urllib.request.Request(getGlucoseUrl)
    glucoseRequest.get_method = lambda: method
    glucoseRequest.add_header("Accept", 'application/json')
    glucoseRequest.add_header("Content-Length", '0')
    emptyLoad = {"": ""}
    try:
        connection2 = opener.open(glucoseRequest, json.dumps(emptyLoad).encode("utf8"))
    except urllib.error.HTTPError as e:
        connection2 = e
    if connection2.code == 200:
        print("ALL GOOD")
        glucoseReading = connection2.read()
        print(glucoseReading)
        glucoseReading = json.loads(glucoseReading)
        print(glucoseReading)
        glucose = glucoseReading[0]["Value"]
        trend = glucoseReading[0]["Trend"]
        data = []
        for item in glucoseReading:
            print(item["Value"])
            data.append(int(item["Value"]))
        data.reverse()
    else:
        print((connection2.code))
    return (glucose, trend, data)


def get_session():
    method = "POST"
    username = os.getenv("username")
    print(username)
    password = os.getenv("password")
    payload = {"password": password, "applicationId": "d89443d2-327c-4a6f-89e5-496bbb0317db", "accountName": username}
    payload = json.dumps(payload).encode('utf8')
    seshRequest = urllib.request.Request(sessionIdUrl, payload)
    seshRequest.add_header("Content-Type", 'application/json')
    seshRequest.add_header("User-Agent", 'Dexcom Share/3.0.2.11 CFNetwork/672.0.2 Darwin/14.0.0')
    seshRequest.add_header("Accept", 'application/json')
    seshRequest.get_method = lambda: method
    try:
        connection = opener.open(seshRequest)
    except urllib.error.HTTPError as e:
        connection = e
    if connection.code == 200:
        sessionID = connection.read()
        sessionID = sessionID[1:-1]
        sessionID = sessionID.decode("utf8")
    else:
        print((connection.code))
    return sessionID


def replace_trend(trend):
    """
    Replace trend number with arrows

    Args:
        trend (int): trend number

    Returns:
        String: trend represented with arrows
    """
    trendtext = None
    if trend == 0:
        trendtext = ""
    if trend == 1:
        # trendtext = "rising quickly"
        trendtext = "↑↑"
    if trend == 2:
        # trendtext = "rising"
        trendtext = "↑"
    if trend == 3:
        # trendtext = "rising slightly"
        trendtext = "↗"
    if trend == 4:
        # trendtext = "steady"
        trendtext = "→"
    if trend == 5:
        # trendtext = "falling slightly"
        trendtext = "↘"
    if trend == 6:
        # trendtext = "falling"
        trendtext = "↓"
    if trend == 7:
        trendtext = "↓↓"
    if trend == 8:
        # trendtext = "unable to determine a trend"
        trendtext = " "
    if trend == 9:
        # trendtext = "trend unavailable"
        trendtext = " "
    return trendtext


sessionId = get_session()
glucose, trend, datalist = get_data(sessionId)
trend_str = replace_trend(trend)

final_string = f"{glucose}{trend_str}"
data = {"bg": final_string}
f = open("output.txt", "w")
json.dump(data, f)
f.close()
with open('datalist.txt', 'w') as f:
    for counter in range(len(datalist)):
        item = datalist[counter]
        if counter != len(datalist)-1:
            f.write(f"{item},")
        else:
            f.write(f"{item}")

keep_alive()

try:
    while 1:
        counter = 0
        while counter < 25:

            glucose, trend, datalist = get_data(sessionId)
            trend_str = replace_trend(trend)
            final_string = f"{glucose}{trend_str}"
            data = {"bg": final_string}
            f = open("output.txt", "w")
            json.dump(data, f)
            f.close()
            with open('datalist.txt', 'w') as f:
                for counter in range(len(datalist)):
                    item = datalist[counter]
                    if counter != len(datalist)-1:
                        f.write(f"{item},")
                    else:
                        f.write(f"{item}")
            time.sleep(30)
            counter += 1
        sessionId = get_session()
except KeyboardInterrupt:
    f.close()
