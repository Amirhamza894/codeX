from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize, mirror_x

# Define colorx manually
def colorx(clip, factor):
    """
    Modifies the color intensity of the video.
    :param clip: Input video clip
    :param factor: Intensity factor (e.g., 1.5 for brighter colors)
    :return: Modified video clip
    """
    def adjust_frame(frame):
        return (frame * factor).clip(0, 255).astype("uint8")
    return clip.fl_image(adjust_frame)

# Function to apply flip
def flip_video(clip):
    return clip.fx(mirror_x)

# Function to apply zoom
def zoom_video(clip, zoom_factor=1.2):
    return clip.fx(resize, zoom_factor)

# Function to apply HDR effect
def apply_hdr(clip):
    return colorx(clip, 1.0)

# Function for setting user options
def get_user_options():
    print("\nAvailable Effects:")
    print("1. Flip Video")
    print("2. Zoom In")
    print("3. HDR Effect")
    print("4. Exit")  # Removed rotation option
    choices = input("\nEnter the numbers of the effects you want to apply (comma-separated): ")
    return [int(choice.strip()) for choice in choices.split(',') if choice.strip().isdigit()]

# Main function to apply effects based on user input
def apply_effects(video_path, output_path):
    try:
        clip = VideoFileClip(video_path)  # Use VideoFileClip instead of VideoClip
        print(f"\nLoaded video: {video_path} (Duration: {clip.duration:.2f} seconds)")
        
        while True:
            user_choices = get_user_options()
            for choice in user_choices:
                if choice == 1:
                    clip = flip_video(clip)
                elif choice == 2:
                    clip = zoom_video(clip)
                elif choice == 3:
                    clip = apply_hdr(clip)
                elif choice == 4:
                    print("Exiting...")
                    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    print(f"\nEdited video saved to: {output_path}")
                    return
                else:
                    print(f"Invalid choice: {choice}. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point
if __name__ == "__main__":
    input_video = input("Enter the path to the input video file: ")
    output_video = input("Enter the path for the output video file: ")
    apply_effects(input_video, output_video)
