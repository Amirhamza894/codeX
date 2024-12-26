import os

def list_directories(path):
    """Lists all directories in the given path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def add_mp4_files_to_file(path, file):
    """Adds .mp4 files in the given path to the text file."""
    for file_name in os.listdir(path):
        if file_name.endswith('.mp4'):
            file.write(os.path.join(path, file_name) + '\n')

def main():
    base_path = os.path.join('data', 'videos')

    if not os.path.exists(base_path):
        print(f"The path {base_path} does not exist.")
        return

    # current_path = base_path
    videos_path = os.path.join(os.getcwd(), 'videos_path')  # Current directory + videos_path folder

    # video_file_path = "video_paths.txt"
    if not os.path.exists(videos_path):
        os.makedirs(videos_path)

    video_file_path = os.path.join(videos_path, "video_paths.txt")

    with open(video_file_path, "w") as file:
        current_path = base_path
        while True:
            directories = list_directories(current_path)

            if not directories:
                print(f"No subdirectories found in {current_path}.")
                break

            print(f"Current Path: {current_path}")
            print("Subdirectories:")
            for idx, directory in enumerate(directories, start=1):
                print(f"{idx}. {directory}")

            try:
                choice = int(input("Select a directory (enter number): ")) - 1
                if choice < 0 or choice >= len(directories):
                    print("Invalid choice. Try again.")
                    continue

                selected_dir = directories[choice]
                current_path = os.path.join(current_path, selected_dir)

                # Check for .mp4 files in the selected directory
                add_mp4_files_to_file(current_path, file)
                mp4_count = len([file_name for file_name in os.listdir(current_path) if file_name.endswith('.mp4')])
                if mp4_count > 0:
                    print(f"The folder '{current_path}' contains {mp4_count} .mp4 file(s).")
                    break

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

    print(f"\nAll video paths have been saved to {video_file_path}.")

if __name__ == "__main__":
    main()
