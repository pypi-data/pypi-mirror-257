from typing import Any, NamedTuple

import httpx

from coda.doisearch import _json

PRINT_PUB_PATH = ("published-print", "date-parts")
ONLINE_PUB_PATH = ("published-online", "date-parts")

WORKS_ENDPOINT = "https://api.crossref.org/works/"


class DateParts(NamedTuple):
    year: int
    month: int | None = None
    day: int | None = None


class Work(NamedTuple):
    title: str
    publication_date: DateParts | None = None
    online_publication_date: DateParts | None = None

    def __str__(self) -> str:
        return self.title


def work(doi: str) -> Work:
    res = httpx.get(f"{WORKS_ENDPOINT}{doi}")
    res.raise_for_status()
    message = res.json()["message"]
    return Work(
        title=_json.get_path(message, "title")[0],
        publication_date=_read_date_parts(message, PRINT_PUB_PATH),
        online_publication_date=_read_date_parts(message, ONLINE_PUB_PATH),
    )


def works(title: str | None = None, author: str | None = None) -> list[Work]:
    res = httpx.get(WORKS_ENDPOINT, params=_prepare_query(title, author))
    res.raise_for_status()
    return [
        Work(
            title=_json.get_path(work, "title")[0],
            publication_date=_read_date_parts(work, PRINT_PUB_PATH),
            online_publication_date=_read_date_parts(work, ONLINE_PUB_PATH),
        )
        for work in _json.get_path(res.json(), "message", "items", default=[])
    ]


def _prepare_query(title: str | None, author: str | None) -> dict[str, str]:
    params = {}
    if title:
        params["query.title"] = title

    if author:
        params["query.author"] = author

    return params


def _read_date_parts(d: dict[str, Any], path: tuple[str, ...]) -> DateParts | None:
    parts = _json.get_path(d, *path)
    if not parts:
        return None

    return DateParts(*parts[0])
