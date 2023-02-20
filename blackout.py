import os
import toml
import json
import yt_dlp
import base64
import sqlite3
import requests

from utils import db

from models import playlist, config

from typing import List

from pathlib import Path

from pydantic import parse_obj_as

from mutagen.flac import Picture
from mutagen.oggopus import OggOpus

from ytmusicapi import YTMusic

BASE_URL = "https://music.youtube.com/watch?v="
YT_DLP_OPTS = {
    "outtmpl": "",
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
        }
    ],
    "audio-format": "opus",
}

# Will probably switch to musicbrainz for proper tagging
def add_metadata(input_file: str, thumbnail_url: str, album: str, artists: List[playlist.Artist], title: str, year: str, track_count: int):
    response = requests.get(thumbnail_url)

    audio = OggOpus(input_file)

    picture = Picture()
    picture.data = response.content
    picture.type = 3
    picture.desc = "Album cover"
    picture.mime = u"image/jpeg"
    picture_data = picture.write()
    encoded_data = base64.b64encode(picture_data)
    vcomment_value = encoded_data.decode("ascii")
    
    # Tagging. View vorbis comments to know what this is
    audio["metadata_block_picture"] = [vcomment_value]

    audio["TITLE"] = title
    
    artist_names = []
    for artist in artists:
        artist_names.append(artist.name)
        
    audio["ARTIST"] =  ";".join(artist_names)
    audio["ALBUM"] = album
    audio["DATE"] = year
    audio["TOTALTRACKS"] = str(track_count)
    audio["TRACKTOTAL"] = str(track_count)
    
    audio.save()    
    # File names are wreidly saved with Topic_ prefix at song titles. 
    clear_name = input_file.replace("Topic_", "")
    os.rename(input_file, clear_name)
    
    db.write_track(conn, title, ";".join(artist_names) ,album, int(year),track_count, clear_name)
    
    return clear_name
    


if __name__ == "__main__":
    
    local_dir = os.path.dirname(__file__)
    try:
        try:
            with open(f"{local_dir}/config.toml") as f:
                config = config.Config(**toml.load(f))

        except FileNotFoundError:
            print(
                "No config.toml found. Please make sure you have that file and pasted a valid youtube auth cookie in there!"
            )
            exit(1)

        try:
            ytm = YTMusic(f"{local_dir}/headers_auth.json")

        except Exception:
            with open(f"{local_dir}/headers_auth.json", "r+") as f:
                headers_auth = json.load(f)
                
            headers_auth["Cookie"] = config.cookie_string
            with open(f"{local_dir}/headers_auth.json", "w") as f:
                json.dump(headers_auth, f)

            ytm = YTMusic(f"{local_dir}/headers_auth.json")

        liked_playlist = playlist.Playlist(**ytm.get_liked_songs())
        
        conn = db.create_db_conn(config.db_path)
        downloaded_tracks = db.get_tracks(conn)
        
        for track in liked_playlist.tracks:
            
            if track.videoType != "MUSIC_VIDEO_TYPE_ATV":
                continue
            
            album = ytm.get_album(track.album.id)

        
            
            found = False
            for downloaded in downloaded_tracks:
                if downloaded_tracks:
                    artist_names = []
                    for artist in track.artists:
                            artist_names.append(artist.name)
                    if track.title == downloaded[1] and ";".join(artist_names) == downloaded[2] and track.album.name == downloaded[3]:
                        found = True
                        
            if found:
                continue

            download_path = Path(config.download_path)

            if config.create_artist_dir:
                download_path = download_path.joinpath(track.artists[0].name)
            
            if config.create_album_dir:
                download_path = download_path.joinpath(track.album.name)
                
            download_path.mkdir(parents=True, exist_ok=True)
            download_path = download_path.joinpath(config.file_name)

            YT_DLP_OPTS["outtmpl"] = download_path.__str__()

            with yt_dlp.YoutubeDL(YT_DLP_OPTS) as ydl:
                ydl.download([BASE_URL + track.videoId])
                
            # Kids never do this please... i am sure there is a better way out there but i did not find it
            with yt_dlp.YoutubeDL(YT_DLP_OPTS) as ydl:
                output = ydl.extract_info(BASE_URL + track.videoId)[
                    "requested_downloads"
                ][0]["filepath"]

            cover_art: playlist.Thumbnail = {}
            
            thumbnails = parse_obj_as(List[playlist.Thumbnail], album["thumbnails"])

            # This chooses the most high res thumbnail
            for thumbnail in thumbnails:
                if "width" in cover_art:
                    if thumbnail.height > cover_art.height:
                        cover_art = thumbnail
                else:
                    cover_art = thumbnail
            
            
            year = album["year"] if "year" in album else ytm.get_song(track.videoId)["microformat"]["microformatDataRenderer"]["uploadDate"].split("-")[0]
            file_path = add_metadata(
                output,
                cover_art.url,
                track.album.name,
                track.artists,
                track.title,
                year,
                album["trackCount"]
            )

    except KeyboardInterrupt:
        exit(0)
