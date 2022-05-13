import pytest


def test_room_service_client(client):
    client.room_service.create_room()