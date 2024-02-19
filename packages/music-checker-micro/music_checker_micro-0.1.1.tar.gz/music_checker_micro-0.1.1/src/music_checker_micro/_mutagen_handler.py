"""
Handles tag retrieval functions
"""
from decimal import Decimal

import io

from mutagen.mp3 import MP3
from PIL import Image


def get_mp3_tag_ids(file: str) -> list:
    """Returns all the tags in the given file

    Args:
        file (str): file path and name

    Returns:
        list: tags on the mp3 file
    """
    rv = []
    tags = MP3(file).tags.values()
    for frame in tags:
        id3_id = frame.FrameID
        rv.append(id3_id)
    return rv


def get_filter_mp3_id3_tags(file: str, tags: list) -> dict:
    """Given an MP3 file returns the id3 tags and values for the list of tags

    Args:
        file (str): full path and file name
        tag_list (list): tag names

    Returns:
        dict: key value pairs of the given tags, otherwise empty string
    """
    tags = get_all_mp3_id3_tags(file)
    rv = {k: (tags[k] if k in tags else '') for k in tags}
    return rv


def load_image_from_bytes(bytes_str: str) -> Image:
    im = Image.open(io.BytesIO(bytes_str))
    return im


def get_apic_size(apic_bytes: str) -> str:
    t = load_image_from_bytes(apic_bytes).size
    return str(Decimal((t[0] * t[1]) / 1_000_000))


def get_all_mp3_id3_tags(file: str) -> list:
    """Returns all the ID3 tags in a given file"""
    rv = {}
    tags = MP3(file).tags.values()
    for frame in tags:
        id3_id = frame.FrameID
        # print(f'{id3_id} {frame.HashKey}')
        # T = text
        if id3_id.startswith("T"):
            if id3_id.startswith("TXXX"):
                value = "\n".join(map(str, getattr(frame, 'text', [])))
                rv[frame.HashKey] = value
            else:
                value = "\n".join(map(str, getattr(frame, 'text', [])))
                rv[id3_id] = value
                pass
        if id3_id == 'APIC':
            rv['APIC'] = get_apic_size(frame.data)
    return rv
