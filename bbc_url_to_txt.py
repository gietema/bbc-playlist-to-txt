"""Save playlist in BBC radio URL to txt"""
import json
import logging
from typing import List
import requests
from pathlib import Path
import click
from bs4 import BeautifulSoup


@click.command()
@click.option(
    "-url",
    "--url",
    required=True,
    type=click.STRING,
    help="The BBC playlist url, e.g. https://www.bbc.co.uk/sounds/play/m000jfcw",
)
@click.option(
    "-o",
    "--output-filepath",
    required=True,
    type=click.Path(exists=False, file_okay=True),
    help="The full path where the txt playlist will be saved, e.g., /home/username/playlist.txt",
)
def main(url: str, output_filepath: Path):
    playlist = get_playlist(url)
    save_playlist(playlist, output_filepath)


def get_playlist(url: str) -> List[str]:
    """
    Get list of artist + title song for each track in playlist

    Parameters
    ----------
    url: str
        The bbc playlist url

    Returns
    -------
    List[str]: A list of strings where each string is artist + title song
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for item in soup.find_all("script"):
        if "Tracklist" in str(item):
            data_script = item
    playlist = []
    for item in json.loads(str(data_script)[38:][:-11])["modules"]["data"][1]["data"]:
        item = item["titles"]
        title = item["primary"] + " - " + item["secondary"] if item["secondary"] is not None else item["primary"]
        if item["tertiary"] is not None:
            title += " " + item["tertiary"]
        playlist.append(title)
    return playlist

def save_playlist(playlist: List[str], output_filepath: Path):
    """
    Saves playlist to txt file

    Parameters
    ----------
    playlist: List[str]
        A list of strings where each string is artist + title song
    output_filepath: Path
        The full path where the txt playlist will be saved, e.g., /home/username/playlist.txt
    """
    with open(output_filepath, "w") as f:
        for song in playlist:
            f.write("%s\n" % song)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()  # pylint: disable=no-value-for-parameter
