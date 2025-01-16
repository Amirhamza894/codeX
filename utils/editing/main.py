from video_effects import VideoEffects
from transitions import Transitions
from audio_effects import AudioEffects
from subtitles import Subtitles
from moviepy.editor import VideoFileClip

def apply_effects(video_path, output_path, music_path=None, subtitles_path=None):
    try:
        clip = VideoFileClip(video_path)
        print(f"\nLoaded video: {video_path} (Duration: {clip.duration:.2f} seconds)")

        video_effects = VideoEffects(clip)
        transitions = Transitions(clip)
        audio_effects = AudioEffects(clip)
        subtitle_effects = Subtitles(clip)

        while True:
            print("\nAvailable Effects:")
            print("1. Flip Video")
            print("2. Zoom In")
            print("3. HDR Effect")
            print("4. Edge Detection")
            print("5. Gaussian Blur")
            print("6. Fade In Transition")
            print("7. Fade Out Transition")
            print("8. Add Background Music")
            print("9. Audio Fade In")
            print("10. Audio Fade Out")
            print("11. Add Subtitles")
            print("12. Exit")
            choices = input("\nEnter the numbers of the effects you want to apply (comma-separated): ")
            user_choices = [int(choice.strip()) for choice in choices.split(',') if choice.strip().isdigit()]

            for choice in user_choices:
                if choice == 1:
                    clip = video_effects.flip_video()
                elif choice == 2:
                    clip = video_effects.zoom_video()
                elif choice == 3:
                    clip = video_effects.apply_hdr()
                elif choice == 4:
                    clip = video_effects.edge_detection()
                elif choice == 5:
                    clip = video_effects.gaussian_blur()
                elif choice == 6:
                    clip = transitions.fade_in()
                elif choice == 7:
                    clip = transitions.fade_out()
                elif choice == 8 and music_path:
                    clip = audio_effects.add_background_music(music_path)
                elif choice == 9:
                    clip = audio_effects.audio_fade_in()
                elif choice == 10:
                    clip = audio_effects.audio_fade_out()
                elif choice == 11 and subtitles_path:
                    clip = subtitle_effects.add_subtitles(subtitles_path)
                elif choice == 12:
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
    music_path = input("Enter the path to the background music (optional, press Enter to skip): ")
    subtitles_path = input("Enter the path to the subtitles file (optional, press Enter to skip): ")
    apply_effects(input_video, output_video, music_path, subtitles_path)
