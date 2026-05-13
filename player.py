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

        self.direccion_horizontal = "idle"
        self.tiempo_inicio_inclinacion = 0
        self.movimiento_x = 0
        self.movimiento_y = 0

        self.sprites_nave = self.cargar_sprites_nave()
        self.sprites_thrusters = self.cargar_sprites_thrusters()
        self.imagen = self.sprites_nave["idle"]

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def es_pixel_fondo_claro(self, color):
        r, g, b = color[:3]
        return (
            r >= 180
            and g >= 180
            and b >= 180
            and max(r, g, b) - min(r, g, b) <= 60
        )

    def remover_fondo_claro_conectado(self, superficie):
        ancho, alto = superficie.get_size()
        visitado = bytearray(ancho * alto)
        pila = []

        def agregar_si_fondo(x, y):
            indice = y * ancho + x

            if visitado[indice]:
                return

            visitado[indice] = 1

            if self.es_pixel_fondo_claro(superficie.get_at((x, y))):
                pila.append((x, y))

        for x in range(ancho):
            agregar_si_fondo(x, 0)
            agregar_si_fondo(x, alto - 1)

        for y in range(alto):
            agregar_si_fondo(0, y)
            agregar_si_fondo(ancho - 1, y)

        while pila:
            x, y = pila.pop()
            r, g, b, _ = superficie.get_at((x, y))
            superficie.set_at((x, y), (r, g, b, 0))

            for vecino_x, vecino_y in (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ):
                if 0 <= vecino_x < ancho and 0 <= vecino_y < alto:
                    agregar_si_fondo(vecino_x, vecino_y)

    def cargar_sprite(self, ruta, limpiar_fondo=False):
        imagen_original = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.smoothscale(
            imagen_original,
            (self.ancho, self.alto)
        )

        if limpiar_fondo:
            self.remover_fondo_claro_conectado(imagen)

        return imagen

    def cargar_sprites_nave(self):
        ruta_base = os.path.join("assets", "images", "player", "ship")
        ruta_fallback = os.path.join("assets", "images", "player_ship.png")

        nombres = {
            "idle": "player_idle.png",
            "left_1": "player_left_1.png",
            "left_2": "player_left_2.png",
            "right_1": "player_right_1.png",
            "right_2": "player_right_2.png",
        }

        sprites = {}

        for clave, nombre_archivo in nombres.items():
            ruta = os.path.join(ruta_base, nombre_archivo)

            if not os.path.exists(ruta):
                ruta = ruta_fallback

            sprites[clave] = self.cargar_sprite(ruta, limpiar_fondo=True)

        return sprites

    def cargar_sprites_thrusters(self):
        ruta_base = os.path.join("assets", "images", "player", "thrusters")
        sprites = {}

        for tipo in ("main", "reverse", "left", "right"):
            sprites[tipo] = []

            for frame in range(1, 4):
                ruta = os.path.join(
                    ruta_base,
                    f"thruster_{tipo}_{frame}.png"
                )

                if os.path.exists(ruta):
                    sprites[tipo].append(self.cargar_sprite(ruta))

        return sprites

    def actualizar_estado_movimiento(self, movimiento_x, movimiento_y):
        self.movimiento_x = movimiento_x
        self.movimiento_y = movimiento_y

        if movimiento_x < 0:
            nueva_direccion = "left"
        elif movimiento_x > 0:
            nueva_direccion = "right"
        else:
            nueva_direccion = "idle"

        if nueva_direccion != self.direccion_horizontal:
            self.direccion_horizontal = nueva_direccion
            self.tiempo_inicio_inclinacion = pygame.time.get_ticks()

    def obtener_clave_sprite_nave(self):
        if self.direccion_horizontal == "idle":
            return "idle"

        direccion_sprite = {
            "left": "right",
            "right": "left",
        }.get(self.direccion_horizontal, self.direccion_horizontal)

        tiempo_inclinacion = (
            pygame.time.get_ticks()
            - self.tiempo_inicio_inclinacion
        )

        nivel = 1 if tiempo_inclinacion < 120 else 2
        return f"{direccion_sprite}_{nivel}"

    def obtener_frame_thruster(self, tipo):
        frames = self.sprites_thrusters.get(tipo, [])

        if not frames:
            return None

        indice = (pygame.time.get_ticks() // 80) % len(frames)
        return frames[indice]

    def dibujar_thruster(self, pantalla, tipo):
        imagen = self.obtener_frame_thruster(tipo)

        if imagen is None:
            return

        rect = imagen.get_rect(center=self.rect.center)
        pantalla.blit(imagen, rect)

    def mover(self, teclas):
        movimiento_x = 0
        movimiento_y = 0

        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
            movimiento_x -= 1

        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
            movimiento_x += 1

        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
            movimiento_y -= 1

        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad
            movimiento_y += 1

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
        self.actualizar_estado_movimiento(movimiento_x, movimiento_y)

    def mover_con_mouse(self, posicion_mouse):
        x_anterior = self.x
        y_anterior = self.y

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
        delta_x = self.x - x_anterior
        delta_y = self.y - y_anterior

        movimiento_x = 0
        movimiento_y = 0

        if delta_x < -1:
            movimiento_x = -1
        elif delta_x > 1:
            movimiento_x = 1

        if delta_y < -1:
            movimiento_y = -1
        elif delta_y > 1:
            movimiento_y = 1

        self.actualizar_estado_movimiento(movimiento_x, movimiento_y)

    def dibujar(self, pantalla):
        if self.movimiento_y < 0:
            self.dibujar_thruster(pantalla, "main")

        if self.movimiento_y > 0:
            self.dibujar_thruster(pantalla, "reverse")

        if self.movimiento_x < 0:
            self.dibujar_thruster(pantalla, "left")

        if self.movimiento_x > 0:
            self.dibujar_thruster(pantalla, "right")

        clave_sprite = self.obtener_clave_sprite_nave()
        self.imagen = self.sprites_nave.get(
            clave_sprite,
            self.sprites_nave["idle"]
        )
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
        pantalla.blit(self.imagen, self.rect)
