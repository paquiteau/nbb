"""Core models for the nbb package."""
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta

from nbb.config import get_stop_infos

# TODO use ratp dataset
KNOWN_LINES = {"C01561": "9", "C01567": "91.06"}

NUM2EMOJI = {
    "0": "0️⃣ ",
    "1": "1️⃣ ",
    "2": "2️⃣ ",
    "3": "3️⃣ ",
    "4": "4️⃣ ",
    "5": "5️⃣ ",
    "6": "6️⃣ ",
    "7": "7️⃣ ",
    "8": "8️⃣ ",
    "9": "9️⃣ ",
    "10": "🔟 ",
}


def _get_value_id(obj, name) -> tuple:  # TODO Use namedtuple
    val = obj[name]
    if isinstance(val, list):
        val = val[0]
    val = val["value"]

    t, q, id = val.split(":")[1:-1]
    return t, q, id


@dataclass
class NextPass:
    """Description of the next pass of a bus at a stop area."""

    line_name: str
    """Name of the line."""
    destination: str
    """Destination of the bus."""
    time: datetime
    """Time of the next pass."""
    arrival_status: str
    """Arrival status of the bus. eg: onTime"""
    stop_area_name: str
    """Name of the stop area."""
    stop_area_id: int
    """ID of the stop area."""
    line_id: int
    """ID of the line."""
    is_valid: bool = True

    @classmethod
    def from_v1(cls, data):
        pass

    @classmethod
    def from_v2(cls, data: dict):
        """Create a NextPass object from the v2 data."""
        journey = data["MonitoredVehicleJourney"]
        call = journey["MonitoredCall"]

        stop_area_id = _get_value_id(data, "MonitoringRef")
        stop_area_name = call["StopPointName"][0]["value"]
        # TODO Save the mapping stop_area_id -> stop_area_name
        # Or dowload the full dataset from IDFM.
        line_id = _get_value_id(journey, "LineRef")[-1]
        line_name = KNOWN_LINES.get(line_id, line_id)

        # Find the time string and parse it.
        time_str = None
        for k in ["ExpectedArrivalTime", "ExpectedDepartureTime", "AimedDepartureTime"]:
            try:
                time_str = call[k]
            except KeyError:
                continue
            else:
                break
        if time_str is None:
            raise KeyError("No time found in the data.")
        try:
            time = datetime.fromisoformat(time_str)
        except ValueError as e:
            # The Z at the end of the time string is not supported by fromisoformat
            # until 3.11
            if time_str[-1] == "Z":
                time = datetime.fromisoformat(time_str[:-1])
            else:
                raise e

        return cls(
            destination=journey["DestinationName"][0]["value"],
            time=time.astimezone(),
            arrival_status=call["ArrivalStatus"],
            stop_area_name=stop_area_name,
            stop_area_id=stop_area_id,
            line_id=line_id,
            line_name=line_name,
        )

    @property
    def delta_time(self) -> timedelta:
        """Returns the time difference between now and the next pass."""

        return self.time - datetime.now(tz=self.time.tzinfo)

    def as_str(self, compact: bool = False, pretty: bool = True, padding=4) -> str:
        """Returns a pretty string representation of the next pass."""

        if compact:
            destination = "".join(
                [i for i in self.destination if i.isnumeric() or i.isupper()]
            )
            time_str = self.time.astimezone().strftime("%H:%M")
        else:
            time_str = (
                f"{self.delta_time.seconds // 60:>2}min."
                f"({self.time.strftime('%H:%M')})"
            )
            destination = self.destination

        if pretty:
            # bus_pretty_name = "".join([NUM2EMOJI.get(i, "") for i in self.line_name])
            # return f"⏰ {time_str} {bus_pretty_name: <{padding}} 🚍▶ {destination}"
            return f"{time_str} 🚍 ▶ {destination} [{self.line_name}]"

        return f"{time_str} {self.line_name} [{destination}]"

    def __le__(self, other):
        return self.time <= other.time


# curl -X 'GET'
# 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopArea%3ASP%3A420704%3A'
# -H 'accept: application/json'
# -H  'apikey: HjdLNrITbnGeVPpXSoPrwA0n3gQ6K02W' | jq

BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace/"
DEFAULT_API_KEY = "HjdLNrITbnGeVPpXSoPrwA0n3gQ6K02W"


def get_raw_data(stop_id):
    """Get raw data from API and return it as a json object."""
    response = requests.get(
        BASE_URL
        + "stop-monitoring?MonitoringRef="
        + f"STIF:StopArea:SP:{stop_id}:".replace(":", "%3A"),
        headers={"apikey": DEFAULT_API_KEY, "accept": "application/json"},
    )
    return response.json()


def get_next_passes(stop_id):
    """Get next passes from API and return it as a list of NextPass objects."""
    raw_data = get_raw_data(stop_id)
    next_passes = []
    monit_list = raw_data
    for f in [
        "Siri",
        "ServiceDelivery",
        "StopMonitoringDelivery",
        0,
        "MonitoredStopVisit",
    ]:
        monit_list = monit_list[f]

    for monitored in monit_list:
        try:
            next_passes.append(NextPass.from_v2(monitored))
        except KeyError:
            print(monitored)
    return next_passes


def get_message(conf, stop_name, simple=False, compact=False, padding=5):
    """Returns a message from a list of NextPass objects."""

    stop_full_name, stop_code, filters = get_stop_infos(conf, stop_name)
    next_passes = get_next_passes(stop_code)
    if not next_passes:
        return "No bus found"

    # Remove past buses
    for i, n in enumerate(next_passes):
        if n.time < datetime.now().astimezone():
            n.is_valid = False
    # Filter by direction
    if filters:
        for i, n in enumerate(next_passes):
            if n.destination not in filters:
                n.is_valid = False

    message = (
        f"Next buses at {stop_full_name} "
        f"({datetime.now().astimezone().strftime('%H:%M')})\n"
    )
    message += "\n".join(
        n.as_str(compact, pretty=not simple, padding=padding)
        for n in next_passes
        if n.is_valid
    )
    return message
