from moviepy.editor import VideoFileClip
from moviepy.video.fx import all as vfx
import os

def apply_effects_to_video(video_path, output_path):
    """Applies effects to a video and saves the edited video."""
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        
        # Apply effects (for example, invert colors and slow down the video)
        edited_clip = (video_clip
                       .fx(vfx.colorx, 1.5)  # Increase color saturation
                       .fx(vfx.time_mirror)  # Mirror the time (reverse the video)
                       .fx(vfx.fadein, 2)    # Add a fade-in effect
                       .fx(vfx.fadeout, 2)   # Add a fade-out effect
                       )
        
        # Save the edited video to the output path
        edited_clip.write_videofile(output_path, codec='libx264')
        
        print(f"Video saved to {output_path}")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def process_videos_from_file(txt_file_path, output_folder):
    """Reads video paths from the txt file and applies effects to them."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read video paths from the .txt file
    with open(txt_file_path, "r", encoding="utf-8") as file:
        video_paths = file.readlines()

    # Loop through the video paths and apply effects
    for video_path in video_paths:
        video_path = video_path.strip()  # Remove extra whitespace/newlines

        # Handle paths with spaces or special characters by ensuring proper file handling
        if os.path.exists(video_path):
            # Generate output path for the edited video
            output_path = os.path.join(output_folder, os.path.basename(video_path))
            apply_effects_to_video(video_path, output_path)
        else:
            print(f"Video file {video_path} does not exist.")

if __name__ == "__main__":
    txt_file_path = "videos_path/video_paths.txt"  # Path to your .txt file with video paths
    output_folder = "edited_videos"  # Folder to save the edited videos
    
    process_videos_from_file(txt_file_path, output_folder)
