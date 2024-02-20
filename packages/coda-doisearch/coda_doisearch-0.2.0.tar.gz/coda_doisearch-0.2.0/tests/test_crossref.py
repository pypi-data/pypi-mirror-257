import json
from pathlib import Path
from typing import Any, Iterable, cast

from coda.doisearch import crossref, __version__

DOI = "10.1371/journal.pcbi.1004668"
TITLE = "A Quick Introduction to Version Control with Git and GitHub"
WORK_RESPONSE = Path("tests/crossref_work_response.json")
WORK_QUERY_RESPONSE = Path("tests/crossref_work_query_response.json")


def test__crossref_self_identification__creates_identity_string() -> None:
    identity = crossref.SelfIdentification(
        app_name="test-app",
        app_version="0.0.1",
        app_url="https://example.com",
        mailto="john.doe@example.com",
    )

    assert (
        str(identity)
        == f"test-app/0.0.1 (https://example.com; mailto: john.doe@example.com) BasedOn: coda-doisearch/{__version__}"
    )


def test__querying_crossref_work__returns_work() -> None:
    crossref_response = crossref_response_reference()
    message = crossref_response["message"]

    work = crossref.work(DOI)

    assert work == crossref.Work(
        title=publication_title(message),
        publication_date=published_date(message),
        online_publication_date=online_published_date(message),
    )


def test__querying_crossref_works__returns_multiple_works() -> None:
    ref = worklist_response_reference()

    works = crossref.works(title=TITLE)

    # NOTE: we're not testing for the exact same works,
    # because new works may have been published since the reference
    assert_contains_all_expected(works, ref)


def publication_title(crossref_response: dict[str, Any]) -> str:
    return cast(str, crossref_response["title"][0])


def published_date(crossref_response: dict[str, Any]) -> crossref.DateParts | None:
    if "published-print" not in crossref_response:
        return None

    return crossref.DateParts(*crossref_response["published-print"]["date-parts"][0])


def online_published_date(
    crossref_response: dict[str, Any]
) -> crossref.DateParts | None:
    if "published-online" not in crossref_response:
        return None

    return crossref.DateParts(*crossref_response["published-online"]["date-parts"][0])


def crossref_response_reference() -> dict[str, Any]:
    with WORK_RESPONSE.open() as json_file:
        crossref_response = json.load(json_file)

    return cast(dict[str, Any], crossref_response)


def worklist_response_reference() -> list[crossref.Work]:
    with WORK_QUERY_RESPONSE.open() as json_file:
        worklist_response = json.load(json_file)

    works = [
        crossref.Work(
            title=publication_title(work),
            publication_date=published_date(work),
            online_publication_date=online_published_date(work),
        )
        for work in worklist_response["message"]["items"]
    ]
    return works


def assert_contains_all_expected(
    actual: Iterable[Any], expected: Iterable[Any]
) -> None:
    missing = [exp for exp in expected if exp not in actual]
    if not missing:
        return

    raise AssertionError(f"actual is missing the following items: \n{missing}")
