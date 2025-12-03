# ytmad
YouTube Music Albums Downloader. 
Just open any playlist (PL) on youtube, copypaste link with any track on that PL, and every track will be automatically detected and downloaded in MP3.

# Setup:
Download yt-dlp. Open terminal, paste:
pip install yt-dlp

Or Python 3:
pip3 install yt-dlp


# How to use:
Open terminal in the folder, where you downloaded the script. (Open folder > right click > open in Terminal)
Download the music to the folder where you installed the script:
python ytmad.py "https://www.youtube.com/playlist?list=PLxxxxxx"

# Or choose new folder:
python ytmad.py "https://www.youtube.com/playlist?list=PLxxxxxx" "my_music"

If python ytmad.py "..." doesn't work, try "pip3 install yt-dlp" and python3 ytmad.py "..."
