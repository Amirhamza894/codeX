from moviepy.editor import AudioFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout

class AudioEffects:
    def __init__(self, clip):
        self.clip = clip

    def add_background_music(self, music_path, volume=0.1):
        music = AudioFileClip(music_path).volumex(volume)
        return self.clip.set_audio(music)

    def audio_fade_in(self, duration=1):
        return self.clip.audio.fx(audio_fadein, duration)

    def audio_fade_out(self, duration=1):
        return self.clip.audio.fx(audio_fadeout, duration)
