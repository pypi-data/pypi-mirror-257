"""
Tests for the gitlab_sdk.client Client class.
"""
import pytest
from snowplow_tracker import SelfDescribingJson, Snowplow

from gitlab_sdk import Client
from gitlab_sdk.client import SCHEMAS

app_id = "app_id"
host = "host-foobar123"
event_name = "event_name"
event_payload = {"pay": "load"}
user_id = "12"
user_attributes = {"user_name": "Matthew"}


@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Reset Snowplow after each test."""
    yield
    Snowplow.reset()


def test_initializes_snowplow_tracker_correctly(mocker):
    """Test if Snowplow initializes correctly when Client is instantiated."""
    mocked_emitter_creation = mocker.patch("snowplow_tracker.AsyncEmitter")

    tracker = Client(app_id=app_id, host=host).tracker
    emitter = tracker.emitters[0]

    mocked_emitter_creation.assert_called
    assert tracker.standard_nv_pairs["aid"] == app_id
    assert tracker.get_namespace() == "gitlab"
    assert host in emitter.endpoint
    assert emitter.batch_size == 1

def test_initializes_tracker_correctly_with_optional_args(mocker):
    """Test if Snowplow initializes correctly when Client is instantiated with optional arguments."""
    mocked_tracker_creation = mocker.patch("snowplow_tracker.Snowplow.create_tracker")

    Client(app_id=app_id, host=host, batch_size=10, async_emitter=False)

    creation_args = mocked_tracker_creation.call_args[1]
    assert creation_args["app_id"] == app_id
    assert creation_args["namespace"] == "gitlab"
    assert creation_args["endpoint"] == host
    assert creation_args["emitter_config"].batch_size == 10

def test_track(mocker):
    """Test if tracking works correctly."""
    mocked_track = mocker.patch("snowplow_tracker.Tracker.track_self_describing_event")

    Client(app_id=app_id, host=host).track(event_name, event_payload)

    track_args = mocked_track.call_args[1]
    assert list(track_args.keys()) == ["event_json"]
    assert track_args["event_json"].schema == SCHEMAS["custom_event"]
    assert track_args["event_json"].data == {"name": event_name, "props": event_payload}


def test_identify_without_user_attributes(mocker):
    """Test identifying user without user attributes."""
    mocked_set_subject = mocker.patch("snowplow_tracker.Tracker.set_subject")

    client = Client(app_id=app_id, host=host)
    client.identify(user_id)
    client.track(event_name, event_payload)

    subject = mocked_set_subject.call_args[0][0]
    assert subject.standard_nv_pairs["uid"] == user_id


def test_identify_with_user_attributes(mocker):
    """Test identifying user with user attributes."""
    mocked_set_subject = mocker.patch("snowplow_tracker.Tracker.set_subject")
    mocked_track = mocker.patch("snowplow_tracker.Tracker.track_self_describing_event")

    client = Client(app_id=app_id, host=host)
    client.identify(user_id, user_attributes)
    client.track(event_name, event_payload)

    subject = mocked_set_subject.call_args[0][0]
    assert subject.standard_nv_pairs["uid"] == user_id

    track_args = mocked_track.call_args[1]
    assert list(track_args.keys()) == ["event_json", "context"]
    assert isinstance(track_args["event_json"], SelfDescribingJson)
    assert len(track_args["context"]) == 1
    assert track_args["context"][0].schema == SCHEMAS["user_context"]
    assert track_args["context"][0].data == user_attributes

def test_track_without_event_payload(mocker):
    """Test if tracking works correctly without an event payload."""
    mocked_track = mocker.patch("snowplow_tracker.Tracker.track_self_describing_event")

    Client(app_id=app_id, host=host).track(event_name)

    track_args = mocked_track.call_args[1]
    assert list(track_args.keys()) == ["event_json"]
    assert track_args["event_json"].schema == SCHEMAS["custom_event"]
    assert track_args["event_json"].data == {"name": event_name, "props": {}}, "Expected event payload to default to an empty dictionary"

def test_identify_without_user_attributes_defaults_empty(mocker):
    """Test identifying user without specifying user attributes defaults to empty attributes."""
    mocked_set_subject = mocker.patch("snowplow_tracker.Tracker.set_subject")
    mocked_track = mocker.patch("snowplow_tracker.Tracker.track_self_describing_event")

    client = Client(app_id=app_id, host=host)
    client.identify(user_id)
    client.track(event_name)

    subject = mocked_set_subject.call_args[0][0]
    assert subject.standard_nv_pairs["uid"] == user_id

    track_args = mocked_track.call_args[1]
    assert "context" not in track_args, "Expected no user context when user_attributes not provided"
