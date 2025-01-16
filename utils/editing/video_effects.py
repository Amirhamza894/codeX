from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize, mirror_x, edge_detect, gaussian_blur

class VideoEffects:
    def __init__(self, clip):
        self.clip = clip

    def colorx(self, factor):
        def adjust_frame(frame):
            return (frame * factor).clip(0, 255).astype("uint8")
        return self.clip.fl_image(adjust_frame)

    def flip_video(self):
        return self.clip.fx(mirror_x)

    def zoom_video(self, zoom_factor=1.2):
        return self.clip.fx(resize, zoom_factor)

    def apply_hdr(self):
        return self.colorx(1.0)

    def edge_detection(self):
        return self.clip.fx(edge_detect)

    def gaussian_blur(self, sigma=2):
        return self.clip.fx(gaussian_blur, sigma)
