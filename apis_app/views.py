import re
import requests
from django.shortcuts import render
from django.http import Http404
from .api_client import get_persons, get_person_by_id, resolve_professions


def _extract_id(person_url):
    """Pull the numeric ID out of a canonical API URL like .../sample_project.person/30/"""
    m = re.search(r'/(\d+)/?$', person_url or "")
    return m.group(1) if m else None


def _display_name(person):
    """Combine forename + surname into one name."""
    parts = [person.get("forename", ""), person.get("surname", "")]
    name = " ".join(p for p in parts if p and p.strip())
    return name if name.strip() else "-"


def person_list(request):
    error = None
    persons = []

    try:
        raw = get_persons()
    except requests.RequestException as e:
        error = f"Could not reach the API: {e}"
        raw = []

    # Enrich each person with derived fields used in the template
    for p in raw:
        p["api_id"] = _extract_id(p.get("url", ""))
        p["display_name"] = _display_name(p)
        p["profession_str"] = ", ".join(resolve_professions(p.get("profession", [])))

    persons = raw

    # Filters
    name_q = request.GET.get("name", "").strip()
    profession_q = request.GET.get("profession", "").strip()
    gender_q = request.GET.get("gender", "").strip()

    if name_q:
        persons = [p for p in persons
                   if name_q.lower() in p["display_name"].lower()]
    if profession_q:
        persons = [p for p in persons
                   if profession_q.lower() in p["profession_str"].lower()]
    if gender_q:
        persons = [p for p in persons
                   if gender_q.lower() == p.get("gender", "").lower()]

    # Collect unique genders for the filter dropdown
    genders = sorted({p.get("gender", "") for p in raw if p.get("gender")})

    return render(request, "persons/person_list.html", {
        "persons": persons,
        "name_q": name_q,
        "profession_q": profession_q,
        "gender_q": gender_q,
        "genders": genders,
        "total": len(persons),
        "error": error,
    })


def person_detail(request, person_id):
    error = None
    person = None
    display_name = ""
    profession_str = ""

    try:
        person = get_person_by_id(person_id)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            raise Http404("Person not found")
        error = f"API error: {e}"
    except requests.RequestException as e:
        error = f"Could not reach the API: {e}"

    if person:
        display_name = _display_name(person)
        profession_str = ", ".join(resolve_professions(person.get("profession", [])))

    return render(request, "persons/person_detail.html", {
        "person": person,
        "display_name": display_name,
        "profession_str": profession_str,
        "person_id": person_id,
        "error": error,
    })

