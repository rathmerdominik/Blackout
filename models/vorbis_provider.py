# https://www.xiph.org/vorbis/doc/v-comment.html
# https://picard-docs.musicbrainz.org/downloads/MusicBrainz_Picard_Tag_Map.html
import pydantic

from typing import List, Optional, Union

from pydantic import BaseModel


class Track(BaseModel):
    """When using multiple strings please use [u'str1', u'str2'] to make sure it is Unicode encoded"""

    # AcousticID_ID
    # Track/Work name
    TITLE: str
    # The collection name to which this track belongs
    ALBUM: Album
    # The version field may be used to differentiate multiple versions of the same track title in a single collection. (e.g. remix info)
    VERSION: Optional[str]
    # The track number of this piece if part of a specific larger collection or album
    TRACKNUMBER: Optional[int]
    # The artist generally considered responsible for the work. In popular music this is usually the performing band or singer. For classical music it would be the composer. For an audio book it would be the author of the original text.
    ARTIST: List[Artist]
    # Copyright attribution, e.g., '2001 Nobody's Band' or '1999 Jack Moffitt'
    COPYRIGHT: Optional[str]
    # License information, for example, 'All Rights Reserved', 'Any Use Permitted', a URL to a license such as a Creative Commons license (e.g. "creativecommons.org/licenses/by/4.0/"), or similar.
    LICENSE: Optional[str]
    # Name of the organization producing the track (i.e. the 'record label')
    ORGANIZATION: Optional[str]
    # A short text description of the contents
    DESCRIPTION: Optional[str]
    # A short text indication of music genre
    GENRE: Optional[List[str]]
    # Date the track was recorded
    DATE: Optional[str]
    # Location where track was recorded
    LOCATION: Optional[str]
    # Contact information for the creators or distributors of the track. This could be a URL, an email address, the physical address of the producing label.
    CONTACT: Optional[str]
    # ISRC number for the track; see the ISRC intro page (https://isrc.ifpi.org/) for more information on ISRC numbers.
    ISRC: Optional[str]
    # NOT STANDARD VORBIS! Used for embedding thumbnails
    METADATA_BLOCK_PICTURE: bytes


class Artist(BaseModel):
    """When using multiple strings please use [u'str1', u'str2'] to make sure it is Unicode encoded"""

    # The artist generally considered responsible for the work. In popular music this is usually the performing band or singer. For classical music it would be the composer. For an audio book it would be the author of the original text.
    name: List[str]
    albums: List[Album]


class Album(BaseModel):
    title: str
    artists: List[Artist]
    tracks: List[Track]
