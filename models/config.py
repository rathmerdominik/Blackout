from pydantic import BaseModel


class Config(BaseModel):
    cookie_string: str
    download_path: str
    file_name: str
    create_album_dir: bool
    create_artist_dir: bool
    db_path: str