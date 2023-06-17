from dataclasses import dataclass
from datetime import datetime, timedelta

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
        line_name = KNOWN_LINES.get(line_id, "Unknown")
        return cls(
            destination=journey["DestinationName"][0]["value"],
            time=datetime.fromisoformat(call["ExpectedArrivalTime"]).astimezone(),
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

    def as_str(self, compact: bool = False, pretty: bool = True) -> str:
        """Returns a pretty string representation of the next pass."""

        if compact:
            destination = "".join(
                [i for i in self.destination if i.isnumeric() or i.isupper()]
            )
            time_str = self.time.astimezone().strftime("%H:%M")
        else:
            time_str = (
                f"{self.delta_time.seconds // 60:>2} ({self.time.strftime('%H:%M')})"
            )
            destination = self.destination

        if pretty:
            bus_pretty_name = "".join([NUM2EMOJI.get(i, "") for i in self.line_name])
            return f"⏰ {time_str} {bus_pretty_name: <10} 🚍▶ {destination}"

        return f"{time_str} {self.line_name} [{destination}]"

    def __le__(self, other):
        return self.time <= other.time
