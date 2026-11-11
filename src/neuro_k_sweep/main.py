import logging
import os
import shutil
import sys
from pathlib import Path

from thefuzz import fuzz

from lib.karaoke_parser.analyze_version import match_best
from lib.metadata_utils.CF_Program import Song

# find out what songs are 'upgradable'

logger = logging.getLogger(__name__)

SCRIPT_FOLDER = Path(__file__).parent.parent.parent 

LOG_DIRECTORY = SCRIPT_FOLDER / "Logs"
CONFIG_FILE = SCRIPT_FOLDER / "config.txt"

def setup_logger():
    logger = logging.getLogger()

    log_path = SCRIPT_FOLDER / 'Neuro_K_Sweep.log'

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def move(song: Song, new_location_path: Path):

    filename = song.path.name
    parent = song.path.parent.name
    new_song_path = new_location_path / parent / filename

    print(f"moved {song} to {new_song_path}")

    os.makedirs(os.path.dirname(new_song_path), exist_ok=True) ## side-effect
    #shutil.copy2(src=song.path, dst=new_song_path) ## side-effect
    shutil.move(src=song.path, dst=new_song_path) ## side-effect

    try:
        song.save()
        print(song.path)

    except FileExistsError:
        logger.exception("Error")



if __name__ == "__main__":

    setup_logger()

    print(f"SCRIPT_DIR: {SCRIPT_FOLDER}")

    songs_path = None
    new_location_path = None
    with open(CONFIG_FILE) as f:
        try:
            songs_line = f.readline()
            new_location_line = f.readline()

            songs_path = Path(songs_line.strip()).expanduser()
            new_location_path = Path(new_location_line.strip()).expanduser()
            print(f"Songs Path: {songs_path}")
            print(f"New Path: {new_location_path}")

        except Exception:
            logger.exception("Unable to parse config file.")

    if songs_path is None or new_location_path is None:
        logger.error("Invalid path in config file.")
        sys.exit()

    archive = [
        (Song(f))
        for f in songs_path.rglob("*.mp3")
        if f.is_file()
    ]

    logger.debug(f"Songs Path: {songs_path}")
    logger.debug(f"New Path: {new_location_path}")

    original_count = len(archive)

    if original_count == 0:
        logger.error("No songs found in song path. Please verify if the path is correct.")
        sys.exit()

    for song in archive:

        existing = match_best(
            query=song,
            scorer=fuzz.UWRatio,  # type: ignore
            score_cutoff=90,
            songs=archive,
        )

        if existing is None:
            continue

        old_song = existing[0]
        logger.debug(f"{Song} matched against old: {old_song}.")
        move(old_song, new_location_path)
        archive.remove(old_song)
        break

    new_count = len(archive)

    if original_count == new_count:
        logger.info("No song was moved.")
    else:
        logger.info(f"{original_count - new_count} songs were moved.")

