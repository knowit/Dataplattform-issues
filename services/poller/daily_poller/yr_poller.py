import os
import urllib.request

import xmltodict
from poller_util import PollerUtil
from datetime import datetime

YR_TYPE = "YrType"


def poll():
    last_inserted_doc = PollerUtil.fetch_last_inserted_doc(YR_TYPE)
    last_inserted_timestamp = 0
    if last_inserted_doc:
        last_inserted_timestamp = int(last_inserted_doc)
    location = os.getenv("DATAPLATTFORM_YR_LOCATION", "Norway/Oslo/Oslo/Lakkegata")

    data_points = get_yr_data(location, last_inserted_timestamp)

    for forecast in data_points:
        result = PollerUtil.post_to_ingest_api(forecast, YR_TYPE)
        if result is not None:
            last_inserted_timestamp = forecast["time_from"]

    PollerUtil.upload_last_inserted_doc(last_inserted_timestamp, YR_TYPE)

    return True


def get_yr_data(location, last_inserted_timestamp):
    url = f"https://www.yr.no/place/{location}/varsel_time_for_time.xml"
    response = send_request(url)
    data = xmltodict.parse(response)

    def timestring_to_posix(time):
        # utc_offset = int(data["weatherdata"]["location"]["timezone"]["@utcoffsetMinutes"])
        # utc_delta = timedelta(minutes=utc_offset)
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")  # + utc_delta
        return int(time.timestamp())

    location_name = data["weatherdata"]["location"]["name"]
    forecasts = data["weatherdata"]["forecast"]["tabular"]["time"]
    ret = []
    for i in range(0, min(len(forecasts), 25)):  # At most insert 25 hours of weather data
        forecast = forecasts[i]
        time_from = timestring_to_posix(forecast["@from"])
        if time_from <= last_inserted_timestamp:
            continue
        data_point = {
            "location": location,
            "location_name": location_name,
            "time_from": time_from,
            "time_to": timestring_to_posix(forecast["@to"]),
            "precipitation": float(forecast["precipitation"]["@value"]),
            "wind_speed": float(forecast["windSpeed"]["@mps"]),
            "temperature": int(forecast["temperature"]["@value"]),
            "air_pressure": float(forecast["pressure"]["@value"])
        }
        ret.append(data_point)
    return ret


def send_request(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return response.read().decode()
