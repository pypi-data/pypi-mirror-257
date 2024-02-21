import os
from random import randint
import time
from typing import Optional
from requests import Session
from tqdm import trange

from video_ethz.utils import (
    download_mp4,
    get_authenticated_session,
    get_extended_lecture_metadata,
    sanitize_filename,
)
import unsilence


def unsilence_file(filepath: str):
    #
    u = unsilence.Unsilence(filepath, temp_dir=f".tmp.{randint(0, 999999)}")
    filename = ".".join(filepath.split(".")[:-1])
    extension = "." + filepath.split(".")[-1]
    u.detect_silence()
    trng = None

    def on_render_progress_update(x, y):
        nonlocal trng
        if trng is None:
            trng = trange(y, desc="Rendering")
        trng.update(1)

    estimated_time = u.estimate_time(audible_speed=1.05, silent_speed=8)  # Estimate time savings
    overall_time_saving = estimated_time.get("delta").get("all")
    print(
        f"Estimated time savings overall: {overall_time_saving[0]:.2f}s corresponding to {(overall_time_saving[1] * 100):.2f}%."
    )
    unsilenced_filename = filename + "_unsilenced" + extension
    duplicate_ctr = 1
    while os.path.exists(unsilenced_filename):
        unsilenced_filename = filename + "_unsilenced" + f"_{duplicate_ctr}" + extension
        duplicate_ctr += 1
    u.render_media(
        unsilenced_filename,
        audible_speed=1,
        silent_speed=8,
        threads=8,
        on_render_progress_update=on_render_progress_update,
    )


def download_latest_episodes(
    session: Session,
    lecture_url: str,
    output_dir: Optional[str] = None,
    first: int = 1,
    n_lectures: int = 1,
    quality: str = "medium",
    remove_silence: bool = False,
):
    assert quality in ["high", "medium", "low"], "quality must be one of 'high', 'medium', 'low'"
    # high -> 0, medium -> 1, low -> 2
    output_dir = output_dir or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)
    quality = {"high": 0, "medium": 1, "low": 2}[quality]
    episodes = get_extended_lecture_metadata(session, lecture_url)
    start = max(first - 1, 0)
    for i in trange(
        start, start + n_lectures, desc=f"Downloading from episode {first}-{first+n_lectures}."
    ):
        episode = episodes[i]
        # format '2022-12-07T16:13' date nicely into '2022-12-07'
        episode_date = episode["createdAt"].split("T")[0]
        episode_url = episode["media"][quality]["url"]
        episode_name = sanitize_filename(episode["title"].lower() + "_" + episode_date)
        episode_extension = "." + episode_url.split(".")[-1]
        episode_path = os.path.join(output_dir, episode_name) + episode_extension
        duplicate_ctr = 1
        while os.path.exists(episode_path):
            episode_path = (
                os.path.join(output_dir, episode_name + f"_{duplicate_ctr}") + episode_extension
            )
            duplicate_ctr += 1
        filepath = download_mp4(session, episode_url, episode_path)
        if remove_silence:
            print(f"Removing silence from {episode_name}")
            unsilence_file(filepath)
        print(f"Downloaded {episode_name}")


def download_lecture(
    lecture_url: str,
    output_dir: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    quality: str = "medium",
    first: int = 1,
    n_lectures: int = 1,
    remove_silence: bool = False,
):
    session = get_authenticated_session(username, password)
    output_dir = output_dir or os.getcwd()
    download_latest_episodes(
        session,
        lecture_url,
        output_dir,
        first=first,
        n_lectures=n_lectures,
        quality=quality,
        remove_silence=remove_silence,
    )
