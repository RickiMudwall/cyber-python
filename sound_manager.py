# sound_manager.py

import os
import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sonido_disparo = self.cargar_sonido("player_shoot.wav")
        self.sonido_impacto_bala = self.cargar_sonido("bullet_impact.wav")
        self.sonido_explosion = self.cargar_sonido("explosion.wav")
        self.sonido_danio = self.cargar_sonido("player_damage.wav")
        self.sonido_game_over = self.cargar_sonido("game_over.wav")

        # Volúmenes
        self.sonido_disparo.set_volume(0.25)
        self.sonido_impacto_bala.set_volume(0.35)
        self.sonido_explosion.set_volume(0.35)
        self.sonido_danio.set_volume(0.35)
        self.sonido_game_over.set_volume(0.45)

    def cargar_sonido(self, nombre_archivo):
        ruta = os.path.join("assets", "sounds", nombre_archivo)
        return pygame.mixer.Sound(ruta)

    def reproducir_disparo(self):
        self.sonido_disparo.play()

    def reproducir_impacto_bala(self):
        self.sonido_impacto_bala.play()

    def reproducir_explosion(self):
        self.sonido_explosion.play()

    def reproducir_danio(self):
        self.sonido_danio.play()

    def reproducir_game_over(self):
        self.sonido_game_over.play()