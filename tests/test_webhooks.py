import pytest


def test_webhooks(client):
    client.api_key = 'abcdefg'
    client.api_secret = 'abababa'
    body = '{"event":"room_started", "room":{"sid":"RM_TkVjUvAqgzKz", "name":"mytestroom", "emptyTimeout":300, "creationTime":"1628545903", "turnPassword":"ICkSr2rEeslkN6e9bXL4Ji5zzMD5Z7zzr6ulOaxMj6N", "enabledCodecs":[{"mime":"audio/opus"}, {"mime":"video/VP8"}]}}';
    sha = 'CoEQz1chqJ9bnZRcORddjplkvpjmPujmLTR42DbefYI='

    t = client.generate_access_token()
    t.sha256 = sha

    token = t.to_jwt()
    
    event = client.receive(body, token)
    assert event is not None
    assert event["room"]["name"] == "mytestroom"
    assert event["event"] == "room_started"

    