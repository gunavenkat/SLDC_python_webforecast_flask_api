import requests
import pytest
import json

# run 'pytest -v' for detailed tests
# run 'pytest -m <marker> -v' to run specific tests refer markers in pytest.ini

# Global variables for the data checks
SAMPLE_JSON = json.dumps({"user": "admin", "api-key": "123", "place": "chennai"})
SAMPLE_JSON_DICT = {"user": "admin", "api-key": "123", "place": "chennai"}


def response_fetcher(json=None):
    if json:
        try:
            response = requests.get("http://127.0.0.1:45000/", json=json)
        except:
            raise Exception("Unable to connect to flask API")
        if response.ok:
            # get the json from response
            return response.json()
    else:
        try:
            response = requests.get("http://127.0.0.1:45000/")
        except:
            raise Exception("Unable to connect to flask API")
        if response.ok:
            # get the json from response
            return response.json()


@pytest.mark.flask_1
def test_1():
    response = response_fetcher()
    assert "false" == response["status"]
    assert "no json data found" == response["reason"]


@pytest.mark.flask_1
def test_2():
    response = response_fetcher(json.dumps({}))
    assert "false" == response["status"]

    response = response_fetcher(json.dumps({"user": "admin"}))
    assert "false" == response["status"]

    response = response_fetcher(json.dumps({"user": "admin", "api-key": "123"}))
    assert "false" == response["status"]


@pytest.mark.flask_1
def test_3():
    response = response_fetcher(json.dumps({"user": ""}))
    assert "false" == response["status"]


@pytest.mark.flask_1
def test_4():
    response = response_fetcher(json.dumps({"user": "admin", "api-key": ""}))
    assert "false" == response["status"]


@pytest.mark.flask_2
@pytest.mark.parametrize("place", ["@$$%^&*", "#$/hu"])
def test_5(place):
    response = response_fetcher(
        json.dumps({"user": "admin", "api-key": "123", "place": place})
    )
    if "false" == response["status"]:
        assert "Unable to find the given location weather" == response["reason"]
    else:
        assert isinstance(response["area_name"], str)


@pytest.mark.flask_2
@pytest.mark.parametrize("place", ["1.018800, 84.017022", "-81.164926, 128.222071"])
def test_6(place):
    response = response_fetcher(
        json.dumps({"user": "admin", "api-key": "123", "place": place})
    )
    if "false" == response["status"]:
        assert "Unable to find the given location weather" == response["reason"]
    else:
        assert isinstance(response["area_name"], str)


@pytest.mark.flask_2
@pytest.mark.parametrize("place", ["gandhinagar"])
def test_7(place):
    response = response_fetcher(
        json.dumps({"user": "admin", "api-key": "123", "place": place})
    )
    if "false" == response["status"]:
        assert "Unable to find the given location weather" == response["reason"]
    else:
        assert isinstance(response["area_name"], str)
