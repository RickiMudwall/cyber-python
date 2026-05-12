# ally_ship.py

import os
import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    DURACION_ALIADOS_MS,
    CADENCIA_DISPARO_ALIADO_MS,
)


class AllyShip:
    def __init__(self, indice, total_aliados):
        self.indice = indice
        self.total_aliados = total_aliados

        self.ancho = 95
        self.alto = 95

        # Posición objetivo distribuida en la base de la ventana
        separacion = ANCHO_PANTALLA // (total_aliados + 1)
        self.target_x = separacion * (indice + 1)
        self.target_y = ALTO_PANTALLA - 85

        # Entrada aleatoria desde fuera de la pantalla
        self.start_x = random.choice([
            random.randint(-140, -60),
            random.randint(ANCHO_PANTALLA + 60, ANCHO_PANTALLA + 140),
            random.randint(40, ANCHO_PANTALLA - 40),
        ])
        self.start_y = ALTO_PANTALLA + random.randint(70, 180)

        # Salida aleatoria hacia fuera de la pantalla
        self.exit_x = random.choice([
            random.randint(-160, -70),
            random.randint(ANCHO_PANTALLA + 70, ANCHO_PANTALLA + 160),
            random.randint(40, ANCHO_PANTALLA - 40),
        ])
        self.exit_y = ALTO_PANTALLA + random.randint(80, 200)

        # Puntos de control para curvas distintas
        self.control_entrada_x = (self.start_x + self.target_x) // 2 + random.randint(-180, 180)
        self.control_entrada_y = min(self.start_y, self.target_y) - random.randint(100, 240)

        self.control_salida_x = (self.target_x + self.exit_x) // 2 + random.randint(-180, 180)
        self.control_salida_y = min(self.target_y, self.exit_y) - random.randint(100, 240)

        self.x = self.start_x
        self.y = self.start_y

        self.estado = "entrando"

        self.tiempo_inicio_estado = pygame.time.get_ticks()
        self.tiempo_inicio_disparo = None
        self.ultimo_disparo = 0

        # Cada nave tiene duración propia para que no se muevan iguales
        self.duracion_entrada_ms = random.randint(800, 1300)
        self.duracion_salida_ms = random.randint(800, 1300)

        # Usamos el sprite de la nave del jugador como base aliada
        ruta_imagen = os.path.join("assets", "images", "player_ship.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.rect = self.imagen.get_rect()
        self.rect.center = (int(self.x), int(self.y))

    def calcular_curva_parabolica(self, x_inicio, y_inicio, x_control, y_control, x_fin, y_fin, progreso):
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
        tiempo_estado = tiempo_actual - self.tiempo_inicio_estado

        if self.estado == "entrando":
            progreso = min(1, tiempo_estado / self.duracion_entrada_ms)

            self.x, self.y = self.calcular_curva_parabolica(
                self.start_x,
                self.start_y,
                self.control_entrada_x,
                self.control_entrada_y,
                self.target_x,
                self.target_y,
                progreso
            )

            if progreso >= 1:
                self.estado = "disparando"
                self.tiempo_inicio_estado = tiempo_actual
                self.tiempo_inicio_disparo = tiempo_actual
                self.ultimo_disparo = 0

        elif self.estado == "disparando":
            tiempo_disparando = tiempo_actual - self.tiempo_inicio_disparo

            if tiempo_disparando >= DURACION_ALIADOS_MS:
                self.estado = "saliendo"
                self.tiempo_inicio_estado = tiempo_actual

        elif self.estado == "saliendo":
            progreso = min(1, tiempo_estado / self.duracion_salida_ms)

            self.x, self.y = self.calcular_curva_parabolica(
                self.target_x,
                self.target_y,
                self.control_salida_x,
                self.control_salida_y,
                self.exit_x,
                self.exit_y,
                progreso
            )

            if progreso >= 1:
                self.estado = "finalizado"

        self.rect.center = (int(self.x), int(self.y))

    def puede_disparar(self):
        if self.estado != "disparando":
            return False

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_disparo >= CADENCIA_DISPARO_ALIADO_MS:
            self.ultimo_disparo = tiempo_actual
            return True

        return False

    def obtener_posicion_disparo(self):
        return self.x, self.y - self.alto // 2

    def dibujar(self, pantalla):
        if self.estado != "finalizado":
            pantalla.blit(self.imagen, self.rect)

    def finalizado(self):
        return self.estado == "finalizado"