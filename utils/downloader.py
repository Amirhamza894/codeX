import os
import re
import yt_dlp
import shutil
import instaloader
from pathlib import Path

class VideoDownloader:
    def __init__(self, output_dir='data/videos/'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.check_ffmpeg()

    def check_ffmpeg(self):
        """Check if FFmpeg is installed."""
        if not shutil.which("ffmpeg"):
            raise EnvironmentError("FFmpeg is not installed. Please install it to enable video and audio merging.")

    def cleanup_temp_files(self, target_dir):
        """Remove any temporary .part files."""
        for file_name in os.listdir(target_dir):
            if file_name.endswith(".part"):
                part_file_path = os.path.join(target_dir, file_name)
                print(f"Removing temporary file: {part_file_path}")
                os.remove(part_file_path)

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

    def rename_files_and_folder(self, target_dir):
        """Rename the folder and files inside it by removing spaces."""
        if not os.path.exists(target_dir):
            print(f"Error: The directory {target_dir} does not exist.")
            return

        parent_dir = os.path.dirname(target_dir)
        folder_name = os.path.basename(target_dir)
        new_folder_name = folder_name.replace(" ", "_")  # Replace spaces with underscores
        new_target_dir = os.path.join(parent_dir, new_folder_name)

        if target_dir != new_target_dir:
            os.rename(target_dir, new_target_dir)
            print(f"Renamed folder: {target_dir} -> {new_target_dir}")
            target_dir = new_target_dir

        for file_name in os.listdir(target_dir):
            old_file_path = os.path.join(target_dir, file_name)
            if os.path.isfile(old_file_path):
                new_file_name = file_name.replace(" ", "_")
                new_file_path = os.path.join(target_dir, new_file_name)

                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed file: {old_file_path} -> {new_file_path}")

    def fetch_filtered_videos(self, url, platform):
        """Fetch and download videos from a given platform."""
        platform_folder = os.path.join(self.output_dir, platform)
        os.makedirs(platform_folder, exist_ok=True)

        output_dir_map = {
            "youtube": '%(uploader)s/%(title)s.%(ext)s',
            "tiktok": '%(uploader)s/%(title)s.%(ext)s',
            "instagram": '%(uploader)s/%(title)s.%(ext)s',
            "facebook": '%(uploader)s/%(title)s.%(ext)s',
        }

        uploader_name = None  # Initialize variable to store uploader name

        def hook(d):
            """Hook to capture metadata during download."""
            nonlocal uploader_name
            if d['status'] == 'finished':
                # Extract uploader name from metadata
                uploader_name = d.get('info_dict', {}).get('uploader', None)
                print(f"Download finished. Uploader: {uploader_name}")

        options = {
            'outtmpl': os.path.join(platform_folder, output_dir_map[platform]),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'progress_hooks': [hook],  # Attach the hook
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Downloading videos from {platform}: {url}")
                ydl.download([url])

            if uploader_name:
                # Construct the uploader folder path
                uploader_folder = os.path.join(platform_folder, uploader_name)
                print(f"Cleaning and renaming files in folder: {uploader_folder}")
                self.cleanup_temp_files(uploader_folder)
                self.rename_files_and_folder(uploader_folder)
            else:
                print("Unable to determine uploader name.")

        except Exception as e:
            print(f"Error downloading from {url}: {e}")

    def process_input(self, input_text):
        """Process user input to determine platform and action."""
        platform = self.detect_platform(input_text)

        if platform:
            if platform == "youtube" and 'youtube.com/shorts/' in input_text:
                print(f"Downloading video from YouTube Shorts: {input_text}")
                self.fetch_filtered_videos(input_text, platform)
                return

            print(f"Direct video link detected. Downloading from {platform}.")
            self.fetch_filtered_videos(input_text, platform)
        else:
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
            if not platform:
                print("Invalid choice. Unable to determine platform.")
                return

            if platform == "youtube":
                constructed_url = f"https://www.youtube.com/@{input_text}/shorts"
                print(f"Downloading videos from YouTube Shorts: {constructed_url}")
                self.fetch_filtered_videos(constructed_url, platform)
            elif platform == "instagram":
                self.fetch_instagram_reels(input_text)
            elif platform == "tiktok":
                self.fetch_tiktok_videos(input_text)
            elif platform == "facebook":
                self.fetch_facebook_videos(input_text)

    def fetch_instagram_reels(self, username):
        """Fetch and download all Reels for an Instagram account."""
        target_dir = os.path.join(self.output_dir, f"instagram")  # Specify the folder path
        print(f"Target directory for Instagram reels: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)

        # Check if the folder exists before downloading
        if not os.path.exists(target_dir):
            print(f"Directory {target_dir} does not exist. Please create it manually.")
            return

           # Change the current working directory to the target directory
        os.chdir(target_dir)
        print(f"Changed working directory to: {os.getcwd()}")

        loader = instaloader.Instaloader(save_metadata=False, download_videos=True)  # Allow download of videos
        loader.download_video_thumbnails = False  # Disable thumbnail downloads

        try:
            print(f"Fetching reels from Instagram account: {username}")
            profile = instaloader.Profile.from_username(loader.context, username)

            # Iterate through posts and download videos
            for post in profile.get_posts():
                if post.is_video and post.typename == 'GraphVideo':
                    print(f"Downloading reel: {post.shortcode}")
                    # Download the post directly to the existing target directory
                    loader.download_post(post, username)

            self.rename_files_and_folder(target_dir)  # Optional: renaming to clean up files
        except Exception as e:
            print(f"Error fetching reels for {username}: {e}")



    def fetch_tiktok_videos(self, username):
        """Fetch and download all TikTok videos for a user."""
        target_dir = os.path.join(self.output_dir, f"tiktok/{username}")
        os.makedirs(target_dir, exist_ok=True)

        tiktok_url = f"https://www.tiktok.com/@{username}"
        options = {
            'outtmpl': os.path.join(target_dir, '%(id)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Fetching and downloading videos from TikTok user: {username}")
                ydl.download([tiktok_url])

            self.rename_files_and_folder(target_dir)
        except Exception as e:
            print(f"Error fetching TikTok videos for {username}: {e}")

    def fetch_facebook_videos(self, username):
        """Fetch and download all Facebook videos for a user."""
        target_dir = os.path.join(self.output_dir, f"facebook/{username}")
        os.makedirs(target_dir, exist_ok=True)

        facebook_url = f"https://www.facebook.com/{username}/videos"
        options = {
            'outtmpl': os.path.join(target_dir, '%(id)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Fetching and downloading videos from Facebook user: {username}")
                ydl.download([facebook_url])

            self.rename_files_and_folder(target_dir)
        except Exception as e:
            print(f"Error fetching Facebook videos for {username}: {e}")


if __name__ == "__main__":
    downloader = VideoDownloader()

    while True:
        user_input = input("Enter a video/playlist URL or username (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting the downloader. Goodbye!")
            break
        downloader.process_input(user_input)
