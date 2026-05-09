# boss_missile.py

import os
import math
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
)


class BossMissile:
    def __init__(self, x, y, objetivo):
        self.x = x
        self.y = y
        self.objetivo = objetivo

        self.ancho = 28
        self.alto = 48
        self.velocidad = 3.2
        self.vida = 2

        ruta_imagen = os.path.join("assets", "images", "boss_missile.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen_base = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.imagen = self.imagen_base
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        dx = self.objetivo.x - self.x
        dy = self.objetivo.y - self.y

        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        self.x += dx * self.velocidad
        self.y += dy * self.velocidad

        # Rotar visualmente el misil hacia la dirección de avance
        angulo = math.degrees(math.atan2(-dy, dx)) - 90
        self.imagen = pygame.transform.rotate(self.imagen_base, angulo)
        self.rect = self.imagen.get_rect(center=(self.x, self.y))

    def recibir_impacto(self, danio=1):
        self.vida -= danio
        return self.vida <= 0

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return (
            self.x < -80
            or self.x > ANCHO_PANTALLA + 80
            or self.y < -80
            or self.y > ALTO_PANTALLA + 80
        )