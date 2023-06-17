import requests

from nbb.models import NextPass


# curl -X 'GET'
# 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopArea%3ASP%3A420704%3A'
# -H 'accept: application/json'
# -H  'apikey: HjdLNrITbnGeVPpXSoPrwA0n3gQ6K02W' | jq

BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace/"
DEFAULT_API_KEY = "HjdLNrITbnGeVPpXSoPrwA0n3gQ6K02W"


def get_raw_data(STOP_ID):
    """Get raw data from API and return it as a json object."""
    response = requests.get(
        BASE_URL
        + "stop-monitoring?MonitoringRef="
        + f"STIF:StopArea:SP:{STOP_ID}:".replace(":", "%3A"),
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
        next_passes.append(NextPass.from_v2(monitored))
    return next_passes
