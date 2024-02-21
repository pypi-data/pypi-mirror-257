import os
import click

from video_ethz.downloader import download_lecture


@click.command()
@click.argument("lecture_url")
@click.option("--first", "--start", default=1, help="Number of lecture episode to download.")
@click.option("--n_lectures", "-n", default=1, help="Number of lecture episode to download.")
@click.option("--all", "a", is_flag=True, help="Download all episodes.")
@click.option("--quality", default="medium", help="Quality of episodes to download.")
@click.option("--output_dir", default="./", help="Directory to save the downloaded episodes.")
@click.option("--remove_silence", is_flag=True, help="Remove silence from the downloaded episodes.")
def download_latest_lecture(lecture_url, first, n_lectures, a, quality, output_dir, remove_silence):
    """CLI tool to download the latest episodes."""
    if a:
        n_lectures = 127
    username = os.environ.get("ETHZ_USERNAME") or click.prompt("ETHZ Username")
    password = os.environ.get("ETHZ_PASSWORD") or click.prompt("ETHZ Password", hide_input=True)
    download_lecture(
        lecture_url,
        output_dir=output_dir,
        username=username,
        password=password,
        quality=quality,
        first=first,
        n_lectures=n_lectures,
        remove_silence=remove_silence,
    )


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    download_latest_lecture()
