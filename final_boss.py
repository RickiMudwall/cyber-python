# final_boss.py

import os
import pygame

from settings import (
    ANCHO_PANTALLA,
    VERDE_CYBER,
    ROJO_ALERTA,
    BLANCO,
    AZUL_CYBER,
    MORADO_CYBER,
)


class FinalBoss:
    def __init__(self):
        self.ancho = 160
        self.alto = 120

        self.x = ANCHO_PANTALLA // 2
        self.y = 120

        self.velocidad = 2
        self.direccion = 1

        self.vida_maxima = 300
        self.vida = self.vida_maxima

        self.escaneado = False
        self.ataque_masivo_activo = False
        self.derrotado = False

        self.tiempo_inicio_ataque_masivo = None
        self.duracion_ataque_masivo_ms = 5000

        ruta_imagen = os.path.join("assets", "images", "final_boss.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        if self.derrotado:
            return

        # Movimiento lateral simple
        self.x += self.velocidad * self.direccion

        margen = self.ancho // 2

        if self.x <= margen:
            self.x = margen
            self.direccion = 1

        if self.x >= ANCHO_PANTALLA - margen:
            self.x = ANCHO_PANTALLA - margen
            self.direccion = -1

        self.rect.center = (self.x, self.y)

        self.actualizar_ataque_masivo()

    def marcar_escaneado(self):
        self.escaneado = True

    def recibir_danio_minimo(self, cantidad):
        """
        El Boss puede recibir daño, pero es mínimo.
        La derrota real se logra con la secuencia:
        Scanner + Arma poderosa + Aliados.
        """
        if self.derrotado:
            return True

        danio_reducido = max(1, cantidad // 10)
        self.vida -= danio_reducido

        if self.vida < 1:
            self.vida = 1

        return False

    def iniciar_ataque_masivo(self):
        if not self.escaneado or self.derrotado:
            return

        self.ataque_masivo_activo = True
        self.tiempo_inicio_ataque_masivo = pygame.time.get_ticks()

    def actualizar_ataque_masivo(self):
        if not self.ataque_masivo_activo:
            return

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_ataque_masivo

        progreso = min(1, tiempo_transcurrido / self.duracion_ataque_masivo_ms)

        self.vida = int(self.vida_maxima * (1 - progreso))

        if tiempo_transcurrido >= self.duracion_ataque_masivo_ms:
            self.vida = 0
            self.derrotado = True
            self.ataque_masivo_activo = False

    def dibujar(self, pantalla):
        if self.derrotado:
            return

        pantalla.blit(self.imagen, self.rect)

        if self.escaneado:
            self.dibujar_estado_escaneado(pantalla)

        if self.ataque_masivo_activo:
            self.dibujar_ataque_masivo(pantalla)

        self.dibujar_barra_vida(pantalla)

    def dibujar_estado_escaneado(self, pantalla):
        # Aura visual indicando que el Boss fue escaneado
        capa = pygame.Surface((self.ancho + 40, self.alto + 40), pygame.SRCALPHA)
        centro = (capa.get_width() // 2, capa.get_height() // 2)

        pygame.draw.ellipse(
            capa,
            (*AZUL_CYBER, 90),
            (8, 8, self.ancho + 24, self.alto + 24),
            4
        )

        pygame.draw.circle(
            capa,
            (*VERDE_CYBER, 80),
            centro,
            32,
            3
        )

        pantalla.blit(
            capa,
            (
                self.rect.x - 20,
                self.rect.y - 20
            )
        )

    def dibujar_ataque_masivo(self, pantalla):
        # Efecto visual de daño masivo
        capa = pygame.Surface((self.ancho + 80, self.alto + 80), pygame.SRCALPHA)

        pygame.draw.ellipse(
            capa,
            (*ROJO_ALERTA, 100),
            (10, 10, self.ancho + 60, self.alto + 60),
            6
        )

        pygame.draw.ellipse(
            capa,
            (*MORADO_CYBER, 80),
            (25, 25, self.ancho + 30, self.alto + 30),
            4
        )

        pantalla.blit(
            capa,
            (
                self.rect.x - 40,
                self.rect.y - 40
            )
        )

    def dibujar_barra_vida(self, pantalla):
        ancho_barra = 220
        alto_barra = 14

        x_barra = self.x - ancho_barra // 2
        y_barra = self.y - self.alto // 2 - 22

        porcentaje_vida = self.vida / self.vida_maxima
        ancho_vida = int(ancho_barra * porcentaje_vida)

        pygame.draw.rect(
            pantalla,
            ROJO_ALERTA,
            (x_barra, y_barra, ancho_barra, alto_barra),
            border_radius=4
        )

        pygame.draw.rect(
            pantalla,
            VERDE_CYBER,
            (x_barra, y_barra, ancho_vida, alto_barra),
            border_radius=4
        )

        pygame.draw.rect(
            pantalla,
            BLANCO,
            (x_barra, y_barra, ancho_barra, alto_barra),
            2,
            border_radius=4
        )

        fuente = pygame.font.SysFont(None, 22)

        if self.ataque_masivo_activo:
            texto = fuente.render("ATAQUE MASIVO", True, ROJO_ALERTA)
        elif self.escaneado:
            texto = fuente.render("BOSS ESCANEADO", True, AZUL_CYBER)
        else:
            texto = fuente.render("FINAL BOSS", True, BLANCO)

        pantalla.blit(texto, (x_barra + 42, y_barra - 22))

    def esta_destruido(self):
        return self.derrotado or self.vida <= 0