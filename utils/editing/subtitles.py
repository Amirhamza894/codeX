from moviepy.editor import TextClip, CompositeVideoClip

class Subtitles:
    def __init__(self, clip):
        self.clip = clip

    def add_subtitles(self, subtitles_path):
        subtitles = TextClip(subtitles_path, fontsize=24, color='white')
        subtitles = subtitles.set_position(('center', 'bottom')).set_duration(self.clip.duration)
        return CompositeVideoClip([self.clip, subtitles])
