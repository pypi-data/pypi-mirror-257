import os
from typing import Optional
from requests import Session
import string


from video_ethz.config import SECURITY_CHECK_URL
import unicodedata


def sanitize_filename(filename: str) -> str:
    safe_chars = bytearray(("_-." + string.digits + string.ascii_letters).encode())
    all_chars = bytearray(range(0x100))
    delete_chars = bytearray(set(all_chars) - set(safe_chars))
    safe_filename = filename.encode("ascii", "ignore").translate(None, delete_chars).decode()
    return safe_filename


def lecture_security_check_url(lecture_url: str):
    return lecture_url.rsplit("/", 1)[0] + "/j_security_check"


def _headers(headers=None):
    headers = headers or {}
    headers_ = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    headers_.update(headers.copy())
    return headers_


def login(
    session: Session,
    username: Optional[str] = os.environ.get("ETHZ_USERNAME"),
    password: Optional[str] = os.environ.get("ETHZ_PASSWORD"),
):
    res = session.post(
        SECURITY_CHECK_URL,
        data=dict(
            j_username=username,
            j_password=password,
            j_validate=True,
        ),
    )
    res.raise_for_status()
    return res


def get_authenticated_session(
    username: Optional[str] = os.environ.get("ETHZ_USERNAME"),
    password: Optional[str] = os.environ.get("ETHZ_PASSWORD"),
):
    session = Session()
    session.headers = _headers()
    login(session, username, password)
    return session


def get_metadata_url(lecture_url: str, id: str = ""):
    base = lecture_url.rstrip(".html")
    if id != "":
        base += f"/{id}"
    return base + ".series-metadata.json"


def get_lecture_metadata(session: Session, lecture_url: str, id: str = ""):
    res = session.get(get_metadata_url(lecture_url, id))
    res.raise_for_status()
    return res.json()


def get_extended_lecture_metadata(session: Session, lecture_url: str):
    res = session.get(get_metadata_url(lecture_url))
    res.raise_for_status()
    res = res.json()
    res = res["episodes"]
    for episode in res:
        episode["media"] = (
            get_lecture_metadata(session, lecture_url, episode["id"])
            .get("selectedEpisode")
            .get("media")
            .get("presentations")
        )
    res.sort(key=lambda x: x.get("createdAt"), reverse=True)
    return res


def download_mp4(session: Session, url: str, filepath: str):
    assert url.endswith(".mp4"), "url must end with .mp4"
    res = session.get(url)
    res.raise_for_status()
    assert res.headers.get("Content-Type") == "video/mp4", "url must point to a mp4 file"
    with open(filepath, "wb") as f:
        f.write(res.content)
    return filepath
