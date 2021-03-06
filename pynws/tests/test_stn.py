"""Test stations"""
import asyncio

import aiohttp
import pynws
from pynws.tests.station_response import STATION_RESPONSE
import pytest

LATLON = (0, 0)
USERID = "testing@test"


@pytest.fixture()
def station_url(monkeypatch):
    """Monkeypatch station url"""

    def mock_url(a, b):
        return "/stations"

    monkeypatch.setattr("pynws.urls.stn_url", mock_url)


async def stn(request):
    """Return station response"""
    return aiohttp.web.json_response(data=STATION_RESPONSE)


async def test_stn_url(aiohttp_client, loop):
    """Test station url is correct"""
    app = aiohttp.web.Application()
    client = await aiohttp_client(app)
    assert pynws.urls.stn_url(
        *LATLON
    ) == pynws.const.API_URL + pynws.const.API_STATIONS.format(*LATLON)


async def test_stn_response(aiohttp_client, loop, station_url):
    """Test response of stations"""
    app = aiohttp.web.Application()
    app.router.add_get("/stations", stn)
    client = await aiohttp_client(app)
    await pynws.stations(*LATLON, client, USERID)


async def test_stn_fail(aiohttp_client, loop, station_url):
    """Station fails with wrong url"""
    app = aiohttp.web.Application()
    client = await aiohttp_client(app)
    with pytest.raises(aiohttp.ClientResponseError):
        stations = await pynws.stations(*LATLON, client, USERID)
