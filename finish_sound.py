import pygame

def finish_sound():
    pygame.mixer.init()

    pygame.mixer.music.load('Hmm.mp3')

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)