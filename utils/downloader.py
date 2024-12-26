import os
import re
import yt_dlp
import shutil
import instaloader
import requests
from bs4 import BeautifulSoup



class VideoDownloader:
    def __init__(self, output_dir='data/videos/'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.check_ffmpeg()

    def check_ffmpeg(self):
        """Check if FFmpeg is installed."""
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg is not installed. Please install it to enable video and audio merging.")

    def detect_platform(self, input_text):
        """Detect the platform based on the input text."""
        platforms = {
            "youtube": r"(https?://)?(www\.)?(youtube\.com|youtu\.be)",
            "tiktok": r"(https?://)?(www\.)?tiktok\.com",
            "instagram": r"(https?://)?(www\.)?instagram\.com",
            "facebook": r"(https?://)?(www\.)?facebook\.com",
        }

        for platform, pattern in platforms.items():
            if re.search(pattern, input_text):
                return platform

        return None  # Ambiguous input
    
    def fetch_filtered_videos(self, url, platform, filter_condition=None):
        """Fetch and download videos that meet the filter condition."""
        output_dir_map = {
            "youtube": 'youtube/%(uploader)s/%(title)s.%(ext)s',
            "tiktok": 'tiktok/%(uploader)s/%(title)s.%(ext)s',
            "instagram": 'instagram/%(uploader)s/%(title)s.%(ext)s',
            "facebook": 'facebook/%(uploader)s/%(title)s.%(ext)s',
        }
        options = {
            'outtmpl': os.path.join(self.output_dir, output_dir_map[platform]),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
            'noplaylist': True,  # Avoid downloading playlists
        }
        if filter_condition:
            options['match_filter'] = filter_condition

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Fetching and downloading videos from {platform}: {url}")
                ydl.download([url])
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
    
    def fetch_facebook_reels(self, username):
        """Fetch all Reels from a Facebook user's profile."""
        base_url = f"https://www.facebook.com/{username}/reels"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            # Make a request to the Facebook page
            response = requests.get(base_url, headers=headers)
            if response.status_code != 200:
                print("Error fetching Facebook page")
                return []

            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all video links (reels)
            video_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/reel/' in href:
                    full_url = f"https://www.facebook.com{href}"
                    video_links.append(full_url)

            return video_links
        except Exception as e:
            print(f"Error fetching reels for {username}: {e}")
            return []
    
    def fetch_instagram_reels(self, username):
        """Fetch and download all Reels for an Instagram account into the project directory."""
        # Define the target directory
        target_dir = os.path.join(self.output_dir, f"instagram/{username}")
        os.makedirs(target_dir, exist_ok=True)

        loader = instaloader.Instaloader(save_metadata=False, download_videos=True)
        loader.download_video_thumbnails = False  # Skip downloading thumbnails

        try:
            print(f"Fetching reels from Instagram account: {username}")
        
            # Get profile data
            profile = instaloader.Profile.from_username(loader.context, username)
        
            # Loop through all posts and download only Reels
            for post in profile.get_posts():
                if post.is_video and post.typename == 'GraphVideo':
                    print(f"Downloading reel: {post.shortcode}")
                    video_filename = os.path.join(target_dir, f"{post.shortcode}.mp4")
                
                    # Custom download logic: Skip directory creation
                    with loader.context.get_anonymous_session() as session:
                        response = session.get(post.url)
                        if response.ok:
                            with open(video_filename, "wb") as video_file:
                                video_file.write(response.content)
        
            # Remove unwanted files (if any)
            for file in os.listdir(target_dir):
                if not file.endswith(".mp4"):
                    os.remove(os.path.join(target_dir, file))

            print(f"Download completed successfully! Reels saved in {target_dir}")
        except Exception as e:
            print(f"Error fetching reels for {username}: {e}")

    def fetch_tiktok_videos(self, username):
        """Fetch and download all TikTok videos for a user."""
        target_dir = os.path.join(self.output_dir, f"tiktok/{username}")
        os.makedirs(target_dir, exist_ok=True)

        tiktok_url = f"https://www.tiktok.com/@{username}"
        options = {
            'outtmpl': os.path.join(target_dir, '%(id)s.%(ext)s'),
            'format': 'best',  # Download the best available format
            'noplaylist': True,  # Avoid downloading playlists if there are any
            'merge_output_format': 'mp4',  # Ensure the output is in mp4 format
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Fetching and downloading videos from TikTok user: {username}")
                ydl.download([tiktok_url])

            print(f"Download completed successfully! Videos saved in {target_dir}")
        except Exception as e:
            print(f"Error fetching TikTok videos for {username}: {e}")
        # try:
        #     print(f"Fetching videos from TikTok user: {username}")
        #     loader.download([user_url])

        #     print(f"Download completed successfully! Videos saved in {target_dir}")
        # except Exception as e:
        #     print(f"Error fetching TikTok videos for {username}: {e}")


    def process_input(self, input_text):
        """Process user input to determine if it's a URL or username."""
        platform = self.detect_platform(input_text)

        if platform:
            # Direct video link or playlist
            print(f"Direct video link detected. Downloading from {platform}.")
            self.fetch_filtered_videos(input_text, platform)
        else:
            # Ambiguous input, treat it as a username
            print("Ambiguous input detected. Is this a username?")
            print("Select the platform for the username:")
            print("1. YouTube (Shorts Only)\n2. TikTok\n3. Instagram (Reels Only)\n4. Facebook")
            choice = input("Enter the number corresponding to the platform: ").strip()

        platform_map = {
            "1": "youtube",
            "2": "tiktok",
            "3": "instagram",
            "4": "facebook",
        }
        platform = platform_map.get(choice)

        if platform == "instagram":
            # Fetch and download all Instagram Reels
            self.fetch_instagram_reels(input_text)

        elif platform == "tiktok":
            # Fetch and download all TikTok videos
            self.fetch_tiktok_videos(input_text)

        elif platform:
            platform_urls = {
                "youtube": f"https://www.youtube.com/@{input_text}/shorts",  # Constructed URL for YouTube Shorts
                "tiktok": f"https://www.tiktok.com/@{input_text}",
                "facebook": f"https://www.facebook.com/{input_text}/reels",  # Constructed URL for Facebook Reels
            }

            # Fetch and download videos (no need for filter for YouTube Shorts)
            print(f"Downloading videos from {platform}: {platform_urls[platform]}")
            self.fetch_filtered_videos(platform_urls[platform], platform)
        else:
            print("Invalid choice. Unable to determine platform.")

if __name__ == "__main__":
    downloader = VideoDownloader()

    while True:
        user_input = input("Enter a video/playlist URL or username (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting the downloader. Goodbye!")
            break
        downloader.process_input(user_input)