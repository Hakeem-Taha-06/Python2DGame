import pygame

class SoundPlayer:
    def __init__(self):
        self.SFX = {
            'grass' : pygame.mixer.Sound('audio/grass.wav'),
        }

        self.music = {
            'main' : pygame.mixer.Sound('audio/main.wav')
        }

        for sound in self.SFX.values():
            sound.set_volume(0.4)
        for sound in self.music.values():
            sound.set_volume(0.4)

        self.SFX_channel = pygame.mixer.Channel(0)
        self.music_channel = pygame.mixer.Channel(1)
    
    def play_SFX(self, name):
        if name in self.SFX.keys():
            self.SFX[name].play()

    def play_music(self, name):
        if name in self.music.keys():
            if not self.music_channel.get_busy():
                self.music_channel.play(self.music[name])