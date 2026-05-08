# enemy.py

import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ANCHO_ENEMIGO,
    ALTO_ENEMIGO,
    VELOCIDAD_ENEMIGO,
    ROJO_ALERTA,
    BLANCO,
)


class Enemy:
    def __init__(self):
        self.ancho = ANCHO_ENEMIGO
        self.alto = ALTO_ENEMIGO
        self.velocidad = VELOCIDAD_ENEMIGO

        # Aparece en una posición aleatoria arriba de la pantalla
        self.x = random.randint(self.ancho, ANCHO_PANTALLA - self.ancho)
        self.y = -self.alto

        self.rect = pygame.Rect(
            self.x - self.ancho // 2,
            self.y - self.alto // 2,
            self.ancho,
            self.alto
        )

    def actualizar(self):
        # El enemigo baja hacia el jugador
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        # Nave enemiga estilo arcade simple

        punta_abajo = (self.x, self.y + self.alto // 2)
        izquierda = (self.x - self.ancho // 2, self.y - self.alto // 2)
        derecha = (self.x + self.ancho // 2, self.y - self.alto // 2)

        pygame.draw.polygon(
            pantalla,
            ROJO_ALERTA,
            [punta_abajo, izquierda, derecha]
        )

        # Detalle visual central
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (self.x, self.y),
            5
        )

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.alto