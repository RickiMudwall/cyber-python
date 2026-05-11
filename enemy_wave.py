# enemy_wave.py

import random

from enemy import Enemy

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ENEMIGOS_POR_OLEADA_MIN,
    ENEMIGOS_POR_OLEADA_MAX,
    SEPARACION_ENEMIGOS_OLEADA,
    DISTANCIA_ATAQUE_CERCA_JUGADOR,
)


class EnemyWave:
    def __init__(self, jugador):
        self.jugador = jugador
        self.cantidad = random.randint(
            ENEMIGOS_POR_OLEADA_MIN,
            ENEMIGOS_POR_OLEADA_MAX
        )

        self.enemigos = []
        self.crear_oleada()

    def crear_oleada(self):
        """
        Crea una oleada en formación.

        La oleada usa una curva principal y cada enemigo conserva
        una separación ordenada respecto al centro de la formación.
        """

        lado_entrada = random.choice(["izquierda", "derecha", "centro"])

        if lado_entrada == "izquierda":
            base_start_x = random.randint(-180, -80)
            base_exit_x = random.randint(ANCHO_PANTALLA + 80, ANCHO_PANTALLA + 220)

        elif lado_entrada == "derecha":
            base_start_x = random.randint(ANCHO_PANTALLA + 80, ANCHO_PANTALLA + 220)
            base_exit_x = random.randint(-220, -80)

        else:
            base_start_x = random.randint(80, ANCHO_PANTALLA - 80)
            base_exit_x = random.choice([
                random.randint(-220, -80),
                random.randint(ANCHO_PANTALLA + 80, ANCHO_PANTALLA + 220)
            ])

        base_start_y = random.randint(-220, -100)

        # Punto de ataque cercano a la nave del jugador
        base_attack_x = self.jugador.x + random.randint(-80, 80)

        if base_attack_x < 80:
            base_attack_x = 80

        if base_attack_x > ANCHO_PANTALLA - 80:
            base_attack_x = ANCHO_PANTALLA - 80

        base_attack_y = self.jugador.y - DISTANCIA_ATAQUE_CERCA_JUGADOR

        if base_attack_y < 180:
            base_attack_y = 180

        if base_attack_y > ALTO_PANTALLA - 180:
            base_attack_y = ALTO_PANTALLA - 180

        base_exit_y = random.randint(ALTO_PANTALLA + 80, ALTO_PANTALLA + 220)

        # Puntos de control para dar curva parabólica común
        control_entrada_x = (base_start_x + base_attack_x) // 2 + random.randint(-120, 120)
        control_entrada_y = min(base_start_y, base_attack_y) - random.randint(80, 180)

        control_salida_x = (base_attack_x + base_exit_x) // 2 + random.randint(-120, 120)
        control_salida_y = min(base_attack_y, base_exit_y) - random.randint(80, 180)

        centro_formacion = (self.cantidad - 1) / 2

        for indice in range(self.cantidad):
            offset_x = int((indice - centro_formacion) * SEPARACION_ENEMIGOS_OLEADA)

            start_pos = (
                base_start_x + offset_x,
                base_start_y
            )

            attack_pos = (
                base_attack_x + offset_x,
                base_attack_y
            )

            exit_pos = (
                base_exit_x + offset_x,
                base_exit_y
            )

            control_entrada = (
                control_entrada_x + offset_x,
                control_entrada_y
            )

            control_salida = (
                control_salida_x + offset_x,
                control_salida_y
            )

            # Delay para que aparezcan una tras otra, pero manteniendo formación
            delay_ms = indice * 180

            enemigo = Enemy(
                start_pos=start_pos,
                attack_pos=attack_pos,
                exit_pos=exit_pos,
                control_entrada=control_entrada,
                control_salida=control_salida,
                delay_ms=delay_ms
            )

            self.enemigos.append(enemigo)

    def obtener_enemigos(self):
        return self.enemigos