# player.py

import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ANCHO_JUGADOR,
    ALTO_JUGADOR,
    VELOCIDAD_JUGADOR,
    VERDE_CYBER,
    AZUL_CYBER,
    BLANCO,
)


class Player:
    def __init__(self):
        # Posición inicial: centro inferior de la pantalla
        self.x = ANCHO_PANTALLA // 2
        self.y = ALTO_PANTALLA - 90

        self.ancho = ANCHO_JUGADOR
        self.alto = ALTO_JUGADOR
        self.velocidad = VELOCIDAD_JUGADOR

        # Rectángulo de colisión
        self.rect = pygame.Rect(
            self.x - self.ancho // 2,
            self.y - self.alto // 2,
            self.ancho,
            self.alto
        )

    def mover(self, teclas):
        # Movimiento izquierda/derecha/arriba/abajo
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

        # Actualizar rectángulo de colisión
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        # Nave estilo arcade usando polígonos simples

        punta = (self.x, self.y - self.alto // 2)
        izquierda = (self.x - self.ancho // 2, self.y + self.alto // 2)
        derecha = (self.x + self.ancho // 2, self.y + self.alto // 2)

        # Cuerpo principal
        pygame.draw.polygon(
            pantalla,
            VERDE_CYBER,
            [punta, izquierda, derecha]
        )

        # Cabina
        pygame.draw.circle(
            pantalla,
            AZUL_CYBER,
            (self.x, self.y),
            8
        )

        # Detalle central
        pygame.draw.line(
            pantalla,
            BLANCO,
            (self.x, self.y - 20),
            (self.x, self.y + 20),
            2
        )