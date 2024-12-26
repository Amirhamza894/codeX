import yt_dlp

def download_facebook_reel(url):
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',  # Use video ID as the file name to avoid long names
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Replace with the URL of the Facebook Reel you want to download
reel_url = 'https://www.facebook.com/reel/1246867169762547'
download_facebook_reel(reel_url)
