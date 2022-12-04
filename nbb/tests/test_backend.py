"""Test for backend module."""
import json
import os
from unittest import mock

import pytest

from nbb import backend


@pytest.fixture()
def request_mocker(request):
    """Mock the call to IDFM lines API."""

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), f"request_{request.param}.json"
    )
    with open(filename) as f:
        mock_json = json.load(f)

    with mock.patch("nbb.backend.requests.get") as requests_mock:
        requests_mock.return_value = MockResponse(
            mock_json, 200 if request.param == "sucess" else 404
        )
        yield requests_mock


@pytest.mark.parametrize("pretty", [True, False])
@pytest.mark.parametrize("compact", [True, False])
@pytest.mark.parametrize("request_mocker", ["success", "fail"], indirect=True)
def test_get_formatted_response(request_mocker, pretty, compact):
    """Test get formatted response."""
    print(backend.get_formatted_response("stop_name", pretty, compact))
