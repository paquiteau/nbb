"""Backend to contact the IDFM api."""

import datetime
import unicodedata

import requests

BASE_URL = "https://api-iv.iledefrance-mobilites.fr/lines/v2/"

# line:IDFM:C01561
# stop_area:IDFM:420704


NUM2EMOJI = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    "10": "🔟",
}


def request_data(line, stop_area):
    """Get the data from IDFM API."""
    endpoint = f"{BASE_URL}/line:IDFM:{line}/stops/stop_area:IDFM:{stop_area}/realTime"

    response = requests.get(endpoint).json()
    data = response["nextDepartures"].get("data")
    statusCode = response["nextDepartures"].get("statusCode")
    errorMessage = response["nextDepartures"].get("errorMessage")

    return data, statusCode, errorMessage


def extract_info(nextbus):
    """Extract information for the next bus."""
    short_name = nextbus["shortName"]
    direction = nextbus["lineDirection"]
    time = int(nextbus["time"])

    now = datetime.datetime.now()
    next_bus_time = now + datetime.timedelta(minutes=time)

    return short_name, direction, time, next_bus_time


def format_next_bus_simple(nextbus, compact=False):
    """Format a next bus departure."""
    short_name, direction, time, next_bus_time = extract_info(nextbus)

    ret_str = ""
    if compact:
        direction = "".join([i for i in direction if i.isnumeric() or i.isupper()])
        time_str = f"{next_bus_time.hour}:{next_bus_time.minute}"
    else:
        time_str = f"{time} min. ({next_bus_time.hour}:{next_bus_time.minute})"

    ret_str = " ".join([time_str, short_name, f"[{direction}]"])
    return ret_str


def format_next_bus_pretty(nextbus, compact=False):
    """Pretty format of next bus departure."""
    short_name, direction, nb_t, nb_h = extract_info(nextbus)

    bus_pretty_name = "".join([NUM2EMOJI[i] for i in short_name if i.isnumeric()])
    ret_str = ""
    if compact:
        direction = "".join([i for i in direction if i.isnumeric() or i.isupper()])
        time_str = f"{nb_h.hour}:{nb_h.minute}"
    else:
        time_str = f"{nb_t:>2} min. ({nb_h.hour:02}:{nb_h.minute:02}) "

    ret_str = " ".join([f"⏰ {time_str}", f"{bus_pretty_name} 🚍▶ {direction}"])
    return ret_str


def format_data(data, stop_area, compact=False, pretty=False):
    """Format the reply string in human readable format."""
    ret_str = f"Next Buses at {stop_area}: \n"

    if pretty:
        format_func = format_next_bus_pretty
    else:
        format_func = format_next_bus_simple
    formatted_bus = [format_func(nextbus, compact=compact) for nextbus in data]

    if compact:
        ret_str += " | ".join(formatted_bus)
    else:
        ret_str = "- " + "\n- ".join(formatted_bus)

    return ret_str


def get_codes(stop_name):
    """Find the line and area code matching stop_name."""
    return "C01561", 420704

def string_norm(string):
    """Normalize string."""
    return unicodedata.normalize("NFKD", string).lower()


def normalize(config):
    """Normalize all the aliases."""
    alias_table = {}
    for stop_name, aliases in config["stop"]["aliases"].items():
        for alias_name in aliases:
            alias_table[string_norm(alias_name)] = stop_name

        alias_table[string_norm(stop_name)] = stop_name
    return alias_table


def get_stop_infos(config, input_name):
    """Get the line code and stop area code."""
    alias_table = normalize(config)

    if input_name is not None:
        try:
            stop_name = alias_table[input_name]
        except KeyError:
            _exit_err_msg(
                "Provided stop name could not be map to a registered stop name."
            )

    else:
        stop_name = list(config["stop"]["places"])[0]
    line_code, stop_code = config["stop"]["places"][stop_name]
    filters = config["stop"]["direction_filter"].get(stop_name, [])
    return stop_name, line_code, stop_code, filters


def get_formatted_response(line_name, area_code, filters, pretty=False, compact=False):
    """Return the formatted waiting time for every bus."""
    # get stop_code matching stop_name as close as possible
    # get line on the stop area.
    data, status, error_message = request_data(line_name, area_code)

    if status > 400:
        return error_message

    return format_data(data, stop_name, compact=compact, pretty=pretty)
