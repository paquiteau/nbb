"""Handles API calls to IDFM servers."""


from nbb.models import NextPass

BASE_URLv1 = ""

BASE_URLv2 = ""


def get_next_buses(request_data) -> list[NextPass]:
    """Parse the Request and Create the NextPass List"""
    list_monitored = request_data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][
        0
    ]["MonitoredStopVisit"]

    nextpass_list = [None] * len(list_monitored)
    for i, obj in enumerate(list_monitored):
        nextpass_list[i] = NextPass.from_v2(obj)

    return nextpass_list
