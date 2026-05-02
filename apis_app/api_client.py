"""
API client responsible for fetching data from the external API. 

It provides functions to get a list of persons and to get details of a single person by ID or URL.

Base URL is configured in settings.py.
"""

import requests
from django.conf import settings


def _headers():
    # authentication is not needed
    h = {"Accept": "application/json"}
    return h


def _base():
    return settings.API_BASE_URL.rstrip("/")


def get_persons():
    """
    Fetches ALL persons from the paginated list endpoint, following "next" links.

    API response shape:
        {
            "count": 24,
            "next": "http://.../api/sample_project.person/?limit=20&offset=20",
            "previous": null,
            "results": [
                {
                    "url": "http://.../api/sample_project.person/30/",
                    "forename": "Death",
                    "surname": "",
                    "gender": "",
                    "date_of_birth": null,
                    "date_of_death": null,
                    "profession": []
                },
                ...
            ]
        }
    """
    url = f"{_base()}/api/sample_project.person/"
    all_results = []

    while url:
        resp = requests.get(url, headers=_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        all_results.extend(data.get("results", []))
        url = data.get("next")  # None stops the loop

    return all_results


def get_person_by_url(person_url):
    """
    Fetches a single person using their API URL
    (that is, from the the <url> field returned in the list, e.g. api/sample_project.person/31/).
    """
    resp = requests.get(person_url, headers=_headers(), timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_person_by_id(person_id):
    """
    Fetches a single person by their ID.
    Constructs: {API_BASE_URL}/api/sample_project.person/{person_id}/
    """
    url = f"{_base()}/api/sample_project.person/{person_id}/"
    resp = requests.get(url, headers=_headers(), timeout=10)
    resp.raise_for_status()
    return resp.json()


_profession_cache = {}
def _resolve_profession(value):
    """
    The profession field can be:
      - a dict with or "name"
      - a URL string like "http://.../api/sample_project.profession/6/"
    Returns a human-readable string.
    """
    if isinstance(value, dict):
        return value.get("name") or str(value)

    if isinstance(value, str) and value.startswith("http"):
        if value in _profession_cache:
            return _profession_cache[value]
        try:
            resp = requests.get(value, headers=_headers(), timeout=5)
            resp.raise_for_status()
            data = resp.json()
            name = data.get("name") or str(data)
            _profession_cache[value] = name
            return name
        except Exception:
            # Fall back to extracting the ID from the URL
            return value.rstrip("/").split("/")[-1]

    return str(value)

def resolve_professions(profession_list):
    """Resolve a list of profession values to display strings."""
    return [_resolve_profession(p) for p in (profession_list or [])]
