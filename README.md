> [!WARNING] 
> No longer maintained. I use Spotify by now.  
> Music downloading is just not worth it anymore.

# Blackout

This program written in python is the over-complex solution to my problem.

It pulls Opus files through Youtube Music from tracks that you have liked and saves them in a directory of your choice. It also caches the already downloaded music in a database so that it wont just re-download everything.

From there you can use [Syncthing](https://syncthing.net/) or any other solution that grants you access to the files to pull it to your device for offline usage.

The program is extremely easy to use and even comes with an installer that installs a systemd service and a timer set to 5 minutes. It also copies the program to the `/opt` directory

## Installation

First clone this repository:

`git clone https://github.com/rathmerdominik/Blackout.git`

Switch to the project root:

`cd Blackout`

Then copy the `config.dist.toml` file to `config.toml`:

`cp config.dist.toml config.toml`

After that edit the values in there:

```toml
cookie_string = "" # view https://ytmusicapi.readthedocs.io/en/stable/setup.html
download_path = "" # where to download music to
file_name = "%(uploader)s_%(title)s.%(ext)s" # has to be Youtube DLP standard template https://github.com/yt-dlp/yt-dlp#output-template
db_path = "blackout.db" # where to write the database for caching
create_artist_dir = true 
create_album_dir = true
```

You also need to rename the `headers_auth.dist.json` file to `headers_auth.json`:

`mv headers_auth.dist.json headers_auth.json`

And at last just execute the installer as root. You can either use sudo or just run it as the root user:

`sudo bash installer.sh`

You can also edit the user and the group with which the systemd service will be run in the `installer.sh` file

The installer comes with an uninstaller if you want to remove **Blackout** from your system.

Run `sudo bash installer.sh uninstall` for that

## Contribution

I am fully aware that the script might not be optimal, yet.  
Every pull request can help carry this project further! So feel free to open one.









