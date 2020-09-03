"""
Module to play sounds in the game. 

class AudioDevice
    Audio device needs to be constructed to play sounds.
    Use free standing functions to play sounds.
    Only one audio device should be created.

Functions:
    play_destroy_brick(audio_device: AudioDevice)
    play_hit_brick(audio_device: AudioDevice)
    play_hit_platform(audio_device: AudioDevice)
    play_game_over(audio_device: AudioDevice)
    play_next_level(audio_device: AudioDevice)
    play_lost_ball(audio_device: AudioDevice)
    play_extra_life(audio_device: AudioDevice)
    play_win_game(audio_device: AudioDevice)
"""
import pygame

FILENAME_DESTROY_BRICK = "sounds/destroyBrick.wav"
FILENAME_HIT_BRICK = "sounds/hitBrick.wav"
FILENAME_HIT_PLATFORM = "sounds/hitPlatform.wav"
FILENAME_GAME_OVER = "sounds/gameOver.wav"
FILENAME_NEXT_LEVEL = "sounds/nextLevel.wav"
FILENAME_LOST_BALL = "sounds/lostBall.wav"
FILENAME_EXTRA_LIFE = "sounds/extraLife.wav"
FILENAME_WIN_GAME = "sounds/winGame.wav"


class AudioDevice:
    """AudioDevice to play sounds with freestanding functions."""

    def __init__(self):
        pygame.mixer.init()

    def _play_sound(self, filename: str):
        effect = pygame.mixer.Sound(filename)
        effect.play()


def play_destroy_brick(audio_device: AudioDevice):
    """Play destroy brick sound."""
    audio_device._play_sound(FILENAME_DESTROY_BRICK)


def play_hit_brick(audio_device: AudioDevice):
    """Play hit brick sound."""
    audio_device._play_sound(FILENAME_HIT_BRICK)


def play_hit_platform(audio_device: AudioDevice):
    """Play hit platform sound."""
    audio_device._play_sound(FILENAME_HIT_PLATFORM)


def play_game_over(audio_device: AudioDevice):
    """Play game over sound."""
    audio_device._play_sound(FILENAME_GAME_OVER)


def play_next_level(audio_device: AudioDevice):
    """Play next level sound."""
    audio_device._play_sound(FILENAME_NEXT_LEVEL)


def play_lost_ball(audio_device: AudioDevice):
    """Play lost ball sound."""
    audio_device._play_sound(FILENAME_LOST_BALL)


def play_extra_life(audio_device: AudioDevice):
    """Play extra life sound."""
    audio_device._play_sound(FILENAME_EXTRA_LIFE)


def play_win_game(audio_device: AudioDevice):
    """Play win game sound."""
    audio_device._play_sound(FILENAME_WIN_GAME)
