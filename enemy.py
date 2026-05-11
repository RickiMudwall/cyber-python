# enemy.py

import os
import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ANCHO_ENEMIGO,
    ALTO_ENEMIGO,
    VELOCIDAD_ENEMIGO,
    DURACION_ENTRADA_OLEADA_MS,
    DURACION_ESCAPE_OLEADA_MS,
)


class Enemy:
    def __init__(
        self,
        start_pos=None,
        attack_pos=None,
        exit_pos=None,
        control_entrada=None,
        control_salida=None,
        delay_ms=0
    ):
        self.ancho = ANCHO_ENEMIGO
        self.alto = ALTO_ENEMIGO
        self.velocidad = VELOCIDAD_ENEMIGO

        self.delay_ms = delay_ms
        self.tiempo_creacion = pygame.time.get_ticks()

        self.estado = "esperando"
        self.finalizado = False

        self.usa_trayectoria = (
            start_pos is not None
            and attack_pos is not None
            and exit_pos is not None
            and control_entrada is not None
            and control_salida is not None
        )

        if self.usa_trayectoria:
            self.start_x, self.start_y = start_pos
            self.attack_x, self.attack_y = attack_pos
            self.exit_x, self.exit_y = exit_pos

            self.control_entrada_x, self.control_entrada_y = control_entrada
            self.control_salida_x, self.control_salida_y = control_salida

            self.x = self.start_x
            self.y = self.start_y

        else:
            # Comportamiento antiguo: enemigo simple bajando recto
            self.x = random.randint(self.ancho, ANCHO_PANTALLA - self.ancho)
            self.y = -self.alto
            self.estado = "activo"

        ruta_imagen = os.path.join("assets", "images", "enemy_ship.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.rect = self.imagen.get_rect()
        self.rect.center = (int(self.x), int(self.y))

        self.tiempo_inicio_estado = pygame.time.get_ticks()

    def calcular_curva_parabolica(
        self,
        x_inicio,
        y_inicio,
        x_control,
        y_control,
        x_fin,
        y_fin,
        progreso
    ):
        """
        Curva cuadrática tipo Bézier.
        Visualmente funciona como una trayectoria parabólica suave.
        """
        t = progreso
        inv_t = 1 - t

        x = (inv_t ** 2 * x_inicio) + (2 * inv_t * t * x_control) + (t ** 2 * x_fin)
        y = (inv_t ** 2 * y_inicio) + (2 * inv_t * t * y_control) + (t ** 2 * y_fin)

        return x, y

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.finalizado:
            return

        # Si tiene trayectoria, primero espera su turno de entrada
        if self.usa_trayectoria and self.estado == "esperando":
            if tiempo_actual - self.tiempo_creacion >= self.delay_ms:
                self.estado = "entrando"
                self.tiempo_inicio_estado = tiempo_actual
            else:
                return

        if self.usa_trayectoria:
            tiempo_estado = tiempo_actual - self.tiempo_inicio_estado

            if self.estado == "entrando":
                progreso = min(1, tiempo_estado / DURACION_ENTRADA_OLEADA_MS)

                self.x, self.y = self.calcular_curva_parabolica(
                    self.start_x,
                    self.start_y,
                    self.control_entrada_x,
                    self.control_entrada_y,
                    self.attack_x,
                    self.attack_y,
                    progreso
                )

                if progreso >= 1:
                    self.estado = "escapando"
                    self.tiempo_inicio_estado = tiempo_actual

            elif self.estado == "escapando":
                progreso = min(1, tiempo_estado / DURACION_ESCAPE_OLEADA_MS)

                self.x, self.y = self.calcular_curva_parabolica(
                    self.attack_x,
                    self.attack_y,
                    self.control_salida_x,
                    self.control_salida_y,
                    self.exit_x,
                    self.exit_y,
                    progreso
                )

                if progreso >= 1:
                    self.finalizado = True

        else:
            # Comportamiento antiguo
            self.y += self.velocidad

        self.rect.center = (int(self.x), int(self.y))

    def dibujar(self, pantalla):
        if self.estado != "esperando" and not self.finalizado:
            pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        if self.usa_trayectoria:
            return self.finalizado

        return self.y > ALTO_PANTALLA + self.alto