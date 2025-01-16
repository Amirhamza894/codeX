from moviepy.video.fx.all import fadein, fadeout

class Transitions:
    def __init__(self, clip):
        self.clip = clip

    def fade_in(self, duration=1):
        return self.clip.fx(fadein, duration)

    def fade_out(self, duration=1):
        return self.clip.fx(fadeout, duration)
