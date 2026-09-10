from unittest.mock import patch, MagicMock
import requests

from api import get_tmdb_metadata, get_film_details


def _mock_response(json_data):
    response = MagicMock()
    response.json.return_value = json_data
    return response


def test_get_tmdb_metadata_combines_fields():
    search = {"results": [{"id": 42}]}
    details = {
        "tagline": "A dark tale.",
        "overview": "Something happens.",
        "genres": [{"name": "Drama"}, {"name": "Thriller"}],
    }
    keywords = {"keywords": [{"name": "rain"}, {"name": "noir"}]}

    with patch("api.requests.get", side_effect=[
        _mock_response(search),
        _mock_response(details),
        _mock_response(keywords),
    ]):
        result = get_tmdb_metadata("Some Movie")

    assert result == "A dark tale. Something happens. Drama Thriller rain noir"


def test_get_tmdb_metadata_no_results():
    with patch("api.requests.get", return_value=_mock_response({"results": []})):
        result = get_tmdb_metadata("Nonexistent Movie")

    assert result == ""


def test_get_film_details_returns_title_year_poster():
    search = {
        "results": [{
            "title": "Some Movie",
            "release_date": "2019-05-01",
            "poster_path": "/abc123.jpg",
        }]
    }

    with patch("api.requests.get", return_value=_mock_response(search)):
        result = get_film_details("Some Movie")

    assert result == {
        "title": "Some Movie",
        "year": "2019",
        "poster": "https://image.tmdb.org/t/p/w342/abc123.jpg",
    }


def test_get_film_details_no_results_returns_empty_dict():
    with patch("api.requests.get", return_value=_mock_response({"results": []})):
        result = get_film_details("Nonexistent Movie")

    assert result == {}


def test_get_film_details_request_failure_returns_empty_dict():
    with patch("api.requests.get", side_effect=requests.RequestException("timeout")):
        result = get_film_details("Some Movie")

    assert result == {}
