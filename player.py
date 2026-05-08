# player.py

import os
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ANCHO_JUGADOR,
    ALTO_JUGADOR,
    VELOCIDAD_JUGADOR,
)


class Player:
    def __init__(self):
        # Posición inicial: centro inferior de la pantalla
        self.x = ANCHO_PANTALLA // 2
        self.y = ALTO_PANTALLA - 90

        self.ancho = ANCHO_JUGADOR
        self.alto = ALTO_JUGADOR
        self.velocidad = VELOCIDAD_JUGADOR

        # Cargar sprite de la nave
        ruta_imagen = os.path.join("assets", "images", "player_ship.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad

        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad

        if teclas[pygame.K_UP]:
            self.y -= self.velocidad

        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad

        # Limitar movimiento dentro de la pantalla
        mitad_ancho = self.ancho // 2
        mitad_alto = self.alto // 2

        if self.x < mitad_ancho:
            self.x = mitad_ancho

        if self.x > ANCHO_PANTALLA - mitad_ancho:
            self.x = ANCHO_PANTALLA - mitad_ancho

        if self.y < mitad_alto:
            self.y = mitad_alto

        if self.y > ALTO_PANTALLA - mitad_alto:
            self.y = ALTO_PANTALLA - mitad_alto

        self.rect.center = (self.x, self.y)

    def mover_con_mouse(self, posicion_mouse):
        self.x, self.y = posicion_mouse

        # Limitar movimiento dentro de la pantalla
        mitad_ancho = self.ancho // 2
        mitad_alto = self.alto // 2

        if self.x < mitad_ancho:
            self.x = mitad_ancho

        if self.x > ANCHO_PANTALLA - mitad_ancho:
            self.x = ANCHO_PANTALLA - mitad_ancho

        if self.y < mitad_alto:
            self.y = mitad_alto

        if self.y > ALTO_PANTALLA - mitad_alto:
            self.y = ALTO_PANTALLA - mitad_alto

        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)