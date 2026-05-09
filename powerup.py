# powerup.py

import os
import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
)


class PowerUp:
    def __init__(self, tipo):
        self.tipo = tipo

        self.ancho = 42
        self.alto = 42
        self.velocidad = 2

        self.x = random.randint(self.ancho, ANCHO_PANTALLA - self.ancho)
        self.y = -self.alto

        nombre_imagen = self.obtener_nombre_imagen()
        ruta_imagen = os.path.join("assets", "images", nombre_imagen)

        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def obtener_nombre_imagen(self):
        if self.tipo == "scanner":
            return "powerup_scanner.png"

        if self.tipo == "weapon":
            return "powerup_weapon.png"

        if self.tipo == "allies":
            return "powerup_allies.png"

        return "powerup_scanner.png"

    def actualizar(self):
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.alto