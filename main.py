# main.py

import pygame
import sys
import random
import os
import math
from powerup import PowerUp
from ally_ship import AllyShip
from final_boss import FinalBoss
from boss_missile import BossMissile
from dialog_sequence import DialogSequence

from scanner_effect import ScannerEffect

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    FPS,
    TITULO_JUEGO,
    NEGRO,
    VERDE_CYBER,
    BLANCO,
    AZUL_CYBER,
    ROJO_ALERTA,
    PUNTOS_ENEMIGO_PEQUENO,
    VIDAS_INICIALES,
    ENERGIA_INICIAL,
    ESTADO_MENU,
    ESTADO_JUGANDO,
    ESTADO_PAUSA,
    ESTADO_GAME_OVER,
    ESTADO_VICTORIA,
    ESTADO_INTRO,
    DURACION_INTRO_ESPERA_MS,
    DURACION_INTRO_DESPEGUE_MS,
    MUNICION_ARMA_PODEROSA_POR_POWERUP,
    CADENCIA_ARMA_NORMAL_MS,
    CADENCIA_ARMA_PODEROSA_MS,
    DANIO_BALA_NORMAL,
    DANIO_BALA_PODEROSA,
    CANTIDAD_ALIADOS,
    INTERVALO_OLEADAS_MS,
    OLEADAS_ANTES_TORMENTA_METEORITOS,
    TOTAL_METEORITOS_TORMENTA,
    INTERVALO_METEORITOS_TORMENTA_MS,
    DURACION_TEMBLOR_ENTRADA_BOSS_MS,
    DURACION_REMOLINO_ENTRADA_BOSS_MS,
    INTENSIDAD_TEMBLOR_ENTRADA_BOSS,
    DURACION_EXPLOSIONES_FINAL_BOSS_MS,
    INTERVALO_EXPLOSIONES_FINAL_BOSS_MS,
    RETRASO_TRANSICION_VICTORIA_MS,
    INTRO_DIALOGO_SLIDE_MS,
    INTRO_DIALOGO_HOLD_MS,
    INTRO_DIALOGO_ANCHO,
    INTRO_DIALOGO_ALTO,
    INTRO_DIALOGO_MARGEN_LATERAL,
    INTRO_DIALOGO_MARGEN_SUPERIOR,
    INTRO_SPRITES_RUTA_BASE,
    INTRO_TIERRA_IMAGEN,
    INTRO_ESTACION_FONDO_IMAGEN,
    INTRO_ESTACION_FRENTE_IMAGEN,
    INTRO_TIERRA_ANCHO,
    INTRO_TIERRA_ALTO,
    INTRO_TIERRA_CENTRO_Y,
    INTRO_ESTACION_ANCHO,
    INTRO_ESTACION_ALTO,
    INTRO_ESTACION_FONDO_Y,
    INTRO_ESTACION_FRENTE_Y,
    INTRO_ESTACION_COMPLETA_EN_PROGRESO,
    INTRO_MARGEN_SALIDA_SPRITES,
    INTRO_JUGADOR_Y,
    INTRO_VELOCIDAD_LUZ_ALTO_EFECTO,
    INTRO_VELOCIDAD_LUZ_CANTIDAD_ESTRELLAS,
    INTRO_VELOCIDAD_LUZ_INICIO_FADE_PROGRESO,
    DURACION_VELOCIDAD_LUZ_JUGANDO_MS,
)

from player import Player
from bullet import Bullet
from enemy import Enemy
from enemy_wave import EnemyWave
from enemy_bullet import EnemyBullet
from meteor import Meteor
from explosion import Explosion
from starfield import StarField
from sound_manager import SoundManager
from ui import dibujar_menu_inicio, dibujar_menu_pausa
from power_bullet import PowerBullet


def main():
    pygame.init()

    pantalla = pygame.display.set_mode(
        (ANCHO_PANTALLA, ALTO_PANTALLA),
        pygame.FULLSCREEN | pygame.SCALED
    )
    pygame.display.set_caption(TITULO_JUEGO)

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 32)
    fuente_grande = pygame.font.SysFont(None, 72)

    fondo_estrellas = StarField()
    sonidos = SoundManager()

    def es_pixel_fondo_claro(color):
        r, g, b = color[:3]
        return (
            r >= 215
            and g >= 215
            and b >= 215
            and max(r, g, b) - min(r, g, b) <= 24
        )

    def remover_fondo_claro_conectado(superficie, puntos_extra=None):
        """
        Limpia el tablero blanco/gris exportado como RGB en assets que
        deberían tener transparencia. Solo elimina zonas conectadas al borde
        o a puntos seguros, para no borrar luces internas del sprite.
        """
        ancho, alto = superficie.get_size()
        visitado = bytearray(ancho * alto)
        pila = []

        def agregar_si_fondo(x, y):
            indice = y * ancho + x

            if visitado[indice]:
                return

            visitado[indice] = 1

            if es_pixel_fondo_claro(superficie.get_at((x, y))):
                pila.append((x, y))

        for x in range(ancho):
            agregar_si_fondo(x, 0)
            agregar_si_fondo(x, alto - 1)

        for y in range(alto):
            agregar_si_fondo(0, y)
            agregar_si_fondo(ancho - 1, y)

        if puntos_extra:
            for x, y in puntos_extra:
                if 0 <= x < ancho and 0 <= y < alto:
                    agregar_si_fondo(x, y)

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

    def cargar_sprite_intro(nombre_archivo, tamano, limpiar_fondo=False, puntos_extra=None):
        ruta = os.path.join(INTRO_SPRITES_RUTA_BASE, nombre_archivo)
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.smoothscale(imagen, tamano)

        if limpiar_fondo:
            remover_fondo_claro_conectado(imagen, puntos_extra=puntos_extra)

        return imagen

    intro_tierra = cargar_sprite_intro(
        INTRO_TIERRA_IMAGEN,
        (INTRO_TIERRA_ANCHO, INTRO_TIERRA_ALTO),
        limpiar_fondo=True
    )

    intro_estacion_fondo = cargar_sprite_intro(
        INTRO_ESTACION_FONDO_IMAGEN,
        (INTRO_ESTACION_ANCHO, INTRO_ESTACION_ALTO)
    )

    intro_estacion_frente = cargar_sprite_intro(
        INTRO_ESTACION_FRENTE_IMAGEN,
        (INTRO_ESTACION_ANCHO, INTRO_ESTACION_ALTO),
        limpiar_fondo=True,
        puntos_extra=[
            (x, y)
            for x in range(0, INTRO_ESTACION_ANCHO, 40)
            for y in range(0, INTRO_ESTACION_ALTO, 40)
        ]
    )

    # Estado inicial
    estado = ESTADO_MENU
    opcion_menu_inicio = 0
    opcion_menu_pausa = 0
    tiempo_inicio_intro = 0
    tiempo_inicio_efecto_velocidad_luz_jugando = None
    sincronizar_mouse_con_jugador = False
    frames_sincronizacion_mouse = 0
    control_mouse = True

    duracion_dialogo_intro = (
            INTRO_DIALOGO_SLIDE_MS
            + INTRO_DIALOGO_HOLD_MS
            + INTRO_DIALOGO_SLIDE_MS
    )

    dialogos_intro = DialogSequence([
        {
            "lado": "izquierda",
            "imagen": "dialog_intro_1.png",
            "inicio_ms": 0
        },
        {
            "lado": "derecha",
            "imagen": "dialog_intro_2.png",
            "inicio_ms": duracion_dialogo_intro
        },
        {
            "lado": "izquierda",
            "imagen": "dialog_intro_3.png",
            "inicio_ms": duracion_dialogo_intro * 2
        },
    ])

    # Variables de partida
    jugador = Player()
    balas = []
    enemigos = []
    balas_enemigas = []
    meteoritos = []
    explosiones = []

    powerups = []
    scanner_effects = []
    aliados = []
    boss_missiles = []
    final_boss = None
    fase_boss_activa = False
    entrada_boss_en_proceso = False
    tiempo_inicio_entrada_boss = 0
    punto_aparicion_boss = (ANCHO_PANTALLA // 2, 120)
    boss_previsualizacion_entrada = None
    enemigos_boss_explotados = False
    derrota_boss_en_proceso = False
    tiempo_inicio_derrota_boss = 0
    ultimo_explosion_boss = 0
    posicion_boss_derrotado = (0, 0)

    aliados_usan_weapon = False
    oleadas_generadas_ciclo = 0
    tormenta_meteoritos_activa = False
    meteoritos_tormenta_generados = 0



    tiene_scanner = False
    tiene_weapon = False
    tiene_allies = False

    scanner_activo = False
    weapon_activo = False
    allies_activo = False
    municion_weapon = 0

    puntaje = 0
    vidas = VIDAS_INICIALES
    energia = ENERGIA_INICIAL
    ultimo_disparo_ms = 0

    EVENTO_CREAR_ENEMIGO = pygame.USEREVENT + 1
    EVENTO_DISPARO_ENEMIGO = pygame.USEREVENT + 2
    EVENTO_CREAR_METEORITO = pygame.USEREVENT + 3
    EVENTO_CREAR_POWERUP = pygame.USEREVENT + 4
    EVENTO_DISPARO_BOSS = pygame.USEREVENT + 5

    pygame.time.set_timer(EVENTO_CREAR_ENEMIGO, INTERVALO_OLEADAS_MS)
    pygame.time.set_timer(EVENTO_DISPARO_ENEMIGO, 900)
    pygame.time.set_timer(EVENTO_CREAR_METEORITO, INTERVALO_METEORITOS_TORMENTA_MS)
    pygame.time.set_timer(EVENTO_CREAR_POWERUP, 3000)
    pygame.time.set_timer(EVENTO_DISPARO_BOSS, 1700)




    def reiniciar_partida():
        nonlocal jugador, balas, enemigos, balas_enemigas, meteoritos
        nonlocal explosiones, puntaje, vidas, energia
        nonlocal powerups
        nonlocal tiene_scanner, tiene_allies, municion_weapon
        nonlocal scanner_activo, weapon_activo, allies_activo
        nonlocal scanner_effects
        nonlocal ultimo_disparo_ms
        nonlocal aliados
        nonlocal aliados_usan_weapon
        nonlocal final_boss, fase_boss_activa
        nonlocal entrada_boss_en_proceso
        nonlocal tiempo_inicio_entrada_boss
        nonlocal punto_aparicion_boss
        nonlocal boss_previsualizacion_entrada
        nonlocal enemigos_boss_explotados
        nonlocal boss_missiles
        nonlocal oleadas_generadas_ciclo
        nonlocal tormenta_meteoritos_activa
        nonlocal meteoritos_tormenta_generados
        nonlocal derrota_boss_en_proceso
        nonlocal tiempo_inicio_derrota_boss
        nonlocal ultimo_explosion_boss
        nonlocal posicion_boss_derrotado
        nonlocal tiempo_inicio_efecto_velocidad_luz_jugando
        nonlocal sincronizar_mouse_con_jugador
        nonlocal frames_sincronizacion_mouse

        jugador = Player()
        balas = []
        enemigos = []
        balas_enemigas = []
        meteoritos = []
        explosiones = []
        powerups = []
        scanner_effects = []
        aliados = []
        boss_missiles = []
        aliados_usan_weapon = False

        puntaje = 0
        vidas = VIDAS_INICIALES
        energia = ENERGIA_INICIAL
        ultimo_disparo_ms = 0

        tiene_scanner = False
        tiene_allies = False
        municion_weapon = 0

        scanner_activo = False
        weapon_activo = False
        allies_activo = False
        final_boss = None
        fase_boss_activa = False
        entrada_boss_en_proceso = False
        tiempo_inicio_entrada_boss = 0
        punto_aparicion_boss = (ANCHO_PANTALLA // 2, 120)
        boss_previsualizacion_entrada = None
        enemigos_boss_explotados = False

        oleadas_generadas_ciclo = 0
        tormenta_meteoritos_activa = False
        meteoritos_tormenta_generados = 0

        derrota_boss_en_proceso = False
        tiempo_inicio_derrota_boss = 0
        ultimo_explosion_boss = 0
        posicion_boss_derrotado = (0, 0)
        tiempo_inicio_efecto_velocidad_luz_jugando = None
        sincronizar_mouse_con_jugador = False
        frames_sincronizacion_mouse = 0

    def aplicar_danio_al_jugador(cantidad_danio, particulas_impacto=18):
        nonlocal energia, vidas, estado

        explosiones.append(
            Explosion(
                jugador.x,
                jugador.y,
                cantidad_particulas=particulas_impacto
            )
        )

        sonidos.reproducir_danio()

        energia -= cantidad_danio

        if energia <= 0:
            vidas -= 1

            explosiones.append(
                Explosion(
                    jugador.x,
                    jugador.y,
                    cantidad_particulas=45
                )
            )

            if vidas <= 0:
                vidas = 0
                energia = 0
                estado = ESTADO_GAME_OVER
                sonidos.reproducir_game_over()
            else:
                energia = ENERGIA_INICIAL

    def intentar_disparar():
        nonlocal municion_weapon, weapon_activo, ultimo_disparo_ms

        tiempo_actual = pygame.time.get_ticks()

        if weapon_activo:
            cadencia_actual = CADENCIA_ARMA_PODEROSA_MS
        else:
            cadencia_actual = CADENCIA_ARMA_NORMAL_MS

        puede_disparar = tiempo_actual - ultimo_disparo_ms >= cadencia_actual

        if not puede_disparar:
            return

        if weapon_activo and municion_weapon > 0:
            nueva_bala = PowerBullet(jugador.x, jugador.y - jugador.alto // 2)
            balas.append(nueva_bala)

            municion_weapon -= 1
            ultimo_disparo_ms = tiempo_actual
            sonidos.reproducir_disparo()

            if municion_weapon <= 0:
                municion_weapon = 0
                weapon_activo = False

        else:
            nueva_bala = Bullet(jugador.x, jugador.y - jugador.alto // 2)
            balas.append(nueva_bala)

            ultimo_disparo_ms = tiempo_actual
            sonidos.reproducir_disparo()

    def dibujar_dialogos_intro(tiempo_transcurrido):
        dialogos_intro.dibujar(pantalla, tiempo_transcurrido)

    def suavizar_progreso_intro(progreso):
        return progreso * progreso * (3 - 2 * progreso)

    def posicion_mouse_valida_para_jugador(posicion_mouse):
        mouse_x, mouse_y = posicion_mouse

        if mouse_x <= 2 and mouse_y <= 2:
            return (
                jugador.x <= jugador.ancho // 2 + 2
                and jugador.y <= jugador.alto // 2 + 2
            )

        return True

    def dibujar_efecto_velocidad_luz(y, intensidad=1.0, progreso=0.0):
        intensidad = max(0, min(1, intensidad))
        progreso = max(0, min(1, progreso))

        if intensidad <= 0:
            return

        capa = pygame.Surface(
            (ANCHO_PANTALLA, INTRO_VELOCIDAD_LUZ_ALTO_EFECTO),
            pygame.SRCALPHA
        )

        tiempo_actual = pygame.time.get_ticks()

        if progreso < 0.22:
            estiramiento = 0
        elif progreso < 0.55:
            estiramiento = (progreso - 0.22) / 0.33
        elif progreso < 0.78:
            estiramiento = 1 - ((progreso - 0.55) / 0.23)
        else:
            estiramiento = 0

        estiramiento = suavizar_progreso_intro(estiramiento)
        desplazamiento_estrellas = int(progreso * 95)
        pulso = 0.75 + 0.25 * ((tiempo_actual // 90) % 2)

        tonos_estrellas = [
            (255, 255, 255),
            (160, 220, 255),
            (90, 245, 255),
            (255, 235, 170),
            (190, 150, 255),
        ]

        for indice in range(INTRO_VELOCIDAD_LUZ_CANTIDAD_ESTRELLAS):
            base_x = (indice * 73 + (indice * indice * 17)) % ANCHO_PANTALLA
            base_y = (
                indice * 41
                + (indice % 7) * 13
            ) % INTRO_VELOCIDAD_LUZ_ALTO_EFECTO

            x = base_x
            y_estrella = (
                base_y
                + desplazamiento_estrellas
                + (tiempo_actual // 38 if estiramiento > 0 else 0)
            ) % INTRO_VELOCIDAD_LUZ_ALTO_EFECTO

            tono = tonos_estrellas[indice % len(tonos_estrellas)]
            brillo = 140 + (indice % 5) * 22
            alpha = int(min(255, brillo * intensidad * pulso))

            if estiramiento <= 0.02:
                radio = 1 + (indice % 3 == 0)
                pygame.draw.circle(
                    capa,
                    (*tono, alpha),
                    (int(x), int(y_estrella)),
                    radio
                )
            else:
                largo = int((28 + (indice % 6) * 12) * estiramiento)
                grosor = 1 + int(estiramiento * 2)
                alpha_linea = int(alpha * (0.7 + estiramiento * 0.3))

                pygame.draw.line(
                    capa,
                    (*tono, alpha_linea),
                    (int(x), int(y_estrella - largo // 2)),
                    (int(x), int(y_estrella + largo)),
                    grosor
                )

        pantalla.blit(capa, (0, int(y)))

    def dibujar_remolino_entrada_boss(tiempo_transcurrido):
        if boss_previsualizacion_entrada is None:
            return

        progreso = min(1, tiempo_transcurrido / DURACION_REMOLINO_ENTRADA_BOSS_MS)
        progreso_suave = suavizar_progreso_intro(progreso)

        x_boss, y_boss = punto_aparicion_boss
        imagen_base = boss_previsualizacion_entrada.imagen

        escala = 0.08 + (0.92 * progreso_suave)
        ancho = max(1, int(boss_previsualizacion_entrada.ancho * escala))
        alto = max(1, int(boss_previsualizacion_entrada.alto * escala))

        angulo = (1 - progreso_suave) * 540
        radio_orbita = int((1 - progreso_suave) * 190)
        fase = progreso * math.tau * 2.4
        centro_x = x_boss + int(math.cos(fase) * radio_orbita)
        centro_y = y_boss + int(math.sin(fase) * radio_orbita * 0.45)

        imagen_escalada = pygame.transform.smoothscale(
            imagen_base,
            (ancho, alto)
        )
        imagen_rotada = pygame.transform.rotate(imagen_escalada, angulo)
        imagen_rotada.set_alpha(int(255 * min(1, progreso * 1.35)))
        rect = imagen_rotada.get_rect(center=(centro_x, centro_y))

        capa = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)

        for indice in range(5):
            radio = int((45 + indice * 26) * progreso_suave)
            alpha = int((125 - indice * 18) * (1 - progreso * 0.45))

            if radio > 0 and alpha > 0:
                pygame.draw.circle(
                    capa,
                    (90, 220, 255, alpha),
                    (int(x_boss), int(y_boss)),
                    radio,
                    2
                )

        for indice in range(18):
            paso = indice / 18
            angulo_particula = fase + paso * math.tau
            radio_particula = int((1 - progreso_suave) * 210 + paso * 65)
            x_particula = x_boss + int(math.cos(angulo_particula) * radio_particula)
            y_particula = y_boss + int(math.sin(angulo_particula) * radio_particula * 0.45)

            pygame.draw.circle(
                capa,
                (180, 80, 255, int(150 * (1 - paso) * (1 - progreso * 0.35))),
                (x_particula, y_particula),
                3
            )

        pantalla.blit(capa, (0, 0))
        pantalla.blit(imagen_rotada, rect)

    def aplicar_temblor_boss_si_activo():
        if not entrada_boss_en_proceso:
            return

        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_entrada_boss

        if tiempo_transcurrido >= DURACION_TEMBLOR_ENTRADA_BOSS_MS:
            return

        progreso = tiempo_transcurrido / DURACION_TEMBLOR_ENTRADA_BOSS_MS
        intensidad = int(INTENSIDAD_TEMBLOR_ENTRADA_BOSS * (1 - progreso))

        if intensidad <= 0:
            return

        offset_x = random.randint(-intensidad, intensidad)
        offset_y = random.randint(-intensidad, intensidad)
        captura = pantalla.copy()

        pantalla.fill(NEGRO)
        pantalla.blit(captura, (offset_x, offset_y))

    def dibujar_intro_despegue():
        pantalla.fill(NEGRO)

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_intro

        tiempo_despegue = max(
            0,
            tiempo_transcurrido - DURACION_INTRO_ESPERA_MS
        )

        progreso_despegue = min(
            1,
            tiempo_despegue / DURACION_INTRO_DESPEGUE_MS
        )

        progreso_tierra = suavizar_progreso_intro(progreso_despegue)
        progreso_estacion = min(
            1,
            progreso_despegue / INTRO_ESTACION_COMPLETA_EN_PROGRESO
        )
        progreso_estacion = suavizar_progreso_intro(progreso_estacion)

        tierra_y_inicial = (
            INTRO_TIERRA_CENTRO_Y
            - INTRO_TIERRA_ALTO // 2
        )
        salida_tierra = (
            ALTO_PANTALLA
            - tierra_y_inicial
            + INTRO_MARGEN_SALIDA_SPRITES
        )
        salida_estacion_fondo = (
            ALTO_PANTALLA
            - INTRO_ESTACION_FONDO_Y
            + INTRO_MARGEN_SALIDA_SPRITES
        )
        salida_estacion_frente = (
            ALTO_PANTALLA
            - INTRO_ESTACION_FRENTE_Y
            + INTRO_MARGEN_SALIDA_SPRITES
        )

        desplazamiento_tierra = int(salida_tierra * progreso_tierra)
        desplazamiento_estacion_fondo = int(
            salida_estacion_fondo * progreso_estacion
        )
        desplazamiento_estacion_frente = int(
            salida_estacion_frente * progreso_estacion
        )

        tierra_x = (ANCHO_PANTALLA - INTRO_TIERRA_ANCHO) // 2
        tierra_y = tierra_y_inicial + desplazamiento_tierra

        pantalla.blit(intro_tierra, (tierra_x, tierra_y))

        estacion_fondo_y = (
            INTRO_ESTACION_FONDO_Y
            + desplazamiento_estacion_fondo
        )

        pantalla.blit(
            intro_estacion_fondo,
            (
                (ANCHO_PANTALLA - INTRO_ESTACION_ANCHO) // 2,
                estacion_fondo_y
            )
        )

        # =========================
        # Nave del jugador fija
        # =========================
        jugador.x = ANCHO_PANTALLA // 2
        jugador.y = INTRO_JUGADOR_Y
        jugador.rect.center = (jugador.x, jugador.y)

        if progreso_despegue > 0:
            jugador.actualizar_estado_movimiento(0, -1)
        else:
            jugador.actualizar_estado_movimiento(0, 0)

        jugador.dibujar(pantalla)

        estacion_frente_y = (
            INTRO_ESTACION_FRENTE_Y
            + desplazamiento_estacion_frente
        )

        pantalla.blit(
            intro_estacion_frente,
            (
                (ANCHO_PANTALLA - INTRO_ESTACION_ANCHO) // 2,
                estacion_frente_y
            )
        )

        if progreso_despegue > 0:
            intensidad_velocidad_luz = min(1, progreso_despegue / 0.18)

            if progreso_despegue > INTRO_VELOCIDAD_LUZ_INICIO_FADE_PROGRESO:
                progreso_fade = (
                    progreso_despegue
                    - INTRO_VELOCIDAD_LUZ_INICIO_FADE_PROGRESO
                ) / (1 - INTRO_VELOCIDAD_LUZ_INICIO_FADE_PROGRESO)
                intensidad_velocidad_luz *= 1 - progreso_fade

            dibujar_efecto_velocidad_luz(
                0,
                intensidad_velocidad_luz,
                progreso_despegue
            )

        # Texto de intro
        fuente_intro = pygame.font.SysFont(None, 30)

        if tiempo_transcurrido < DURACION_INTRO_ESPERA_MS:
            segundos_restantes = int(
                (DURACION_INTRO_ESPERA_MS - tiempo_transcurrido) / 1000
            ) + 1

            texto_intro = fuente_intro.render(
                f"Preparando despegue... {segundos_restantes}",
                True,
                BLANCO
            )
        else:
            texto_intro = fuente_intro.render(
                "Despegue iniciado",
                True,
                VERDE_CYBER
            )

        pantalla.blit(texto_intro, (20, ALTO_PANTALLA - 50))
        dibujar_dialogos_intro(tiempo_transcurrido)

    def dibujar_escena_juego():
        pantalla.fill(NEGRO)

        fondo_estrellas.actualizar()
        fondo_estrellas.dibujar(pantalla)

        texto_titulo = fuente.render("Cyber Python - MVP 0.9", True, VERDE_CYBER)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        texto_energia = fuente.render(f"Energia: {energia}", True, BLANCO)
        texto_pausa = fuente.render("P: Pausa", True, BLANCO)
        modo_control = "Mouse" if control_mouse else "Teclado"
        texto_control = fuente.render(f"M: Control {modo_control}", True, BLANCO)

        estado_scanner = "ON" if scanner_activo else ("OK" if tiene_scanner else "--")
        estado_weapon = f"ON {municion_weapon}" if weapon_activo else (
            f"AMMO {municion_weapon}" if municion_weapon > 0 else "--")
        estado_allies = "ON" if allies_activo else ("OK" if tiene_allies else "--")

        texto_powerups = fuente.render(
            f"1 Scanner: {estado_scanner} | 2 Arma: {estado_weapon} | 3 Aliados: {estado_allies}",
            True,
            BLANCO
        )

        if tormenta_meteoritos_activa:
            texto_fase = fuente.render(
                f"TORMENTA DE METEORITOS: {meteoritos_tormenta_generados}/{TOTAL_METEORITOS_TORMENTA}",
                True,
                ROJO_ALERTA
            )
        else:
            texto_fase = fuente.render(
                f"Oleadas: {oleadas_generadas_ciclo}/{OLEADAS_ANTES_TORMENTA_METEORITOS}",
                True,
                BLANCO
            )


        pantalla.blit(texto_titulo, (20, 20))
        pantalla.blit(texto_puntaje, (20, 50))
        pantalla.blit(texto_vidas, (20, 80))
        pantalla.blit(texto_energia, (20, 110))
        pantalla.blit(texto_pausa, (ANCHO_PANTALLA - 120, 20))
        pantalla.blit(texto_control, (ANCHO_PANTALLA - 210, 50))
        pantalla.blit(texto_powerups, (20, 140))
        pantalla.blit(texto_fase, (20, 170))


        for bala in balas:
            bala.dibujar(pantalla)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        for bala_enemiga in balas_enemigas:
            bala_enemiga.dibujar(pantalla)

        for meteorito in meteoritos:
            meteorito.dibujar(pantalla)

        for powerup in powerups:
            powerup.dibujar(pantalla)


        for scanner_effect in scanner_effects:
            scanner_effect.dibujar(pantalla)

        for aliado in aliados:
            aliado.dibujar(pantalla)

        if entrada_boss_en_proceso:
            tiempo_entrada_boss = (
                pygame.time.get_ticks()
                - tiempo_inicio_entrada_boss
            )

            if tiempo_entrada_boss >= DURACION_TEMBLOR_ENTRADA_BOSS_MS:
                dibujar_remolino_entrada_boss(
                    tiempo_entrada_boss - DURACION_TEMBLOR_ENTRADA_BOSS_MS
                )

        if final_boss is not None:
            final_boss.dibujar(
                pantalla,
                mostrar_destruido=derrota_boss_en_proceso,
                mostrar_barra=False
            )

        for explosion in explosiones:
            explosion.dibujar(pantalla)

        for misil in boss_missiles:
            misil.dibujar(pantalla)

        jugador.dibujar(pantalla)

        if (
                final_boss is not None
                and not final_boss.esta_destruido()
        ):
            final_boss.dibujar_barra_vida(pantalla)

        if tiempo_inicio_efecto_velocidad_luz_jugando is not None:
            tiempo_efecto = (
                pygame.time.get_ticks()
                - tiempo_inicio_efecto_velocidad_luz_jugando
            )
            progreso_efecto = min(
                1,
                tiempo_efecto / DURACION_VELOCIDAD_LUZ_JUGANDO_MS
            )
            progreso_salida = suavizar_progreso_intro(progreso_efecto)
            y_velocidad_luz = (
                ALTO_PANTALLA
                - INTRO_VELOCIDAD_LUZ_ALTO_EFECTO
                + int(
                    progreso_salida
                    * (INTRO_VELOCIDAD_LUZ_ALTO_EFECTO + 80)
                )
            )

            dibujar_efecto_velocidad_luz(
                y_velocidad_luz,
                1 - progreso_efecto,
                progreso_efecto
            )

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                # =========================
                # MENÚ INICIAL
                # =========================
                if estado == ESTADO_MENU:
                    if evento.key == pygame.K_UP:
                        opcion_menu_inicio = (opcion_menu_inicio - 1) % 2

                    elif evento.key == pygame.K_DOWN:
                        opcion_menu_inicio = (opcion_menu_inicio + 1) % 2

                    elif evento.key == pygame.K_RETURN:
                        if opcion_menu_inicio == 0:
                            reiniciar_partida()
                            tiempo_inicio_intro = pygame.time.get_ticks()
                            estado = ESTADO_INTRO
                            pygame.mouse.set_visible(False)

                        elif opcion_menu_inicio == 1:
                            pygame.quit()
                            sys.exit()

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif estado == ESTADO_INTRO:
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # =========================
                # JUEGO ACTIVO
                # =========================
                elif estado == ESTADO_JUGANDO:
                    if evento.key == pygame.K_m:
                        control_mouse = not control_mouse

                        if control_mouse:
                            pygame.mouse.set_visible(False)
                        else:
                            pygame.mouse.set_visible(True)

                    elif evento.key == pygame.K_1 and tiene_scanner:
                        # Scanner es de un solo uso: se consume al activarlo
                        tiene_scanner = False

                        scanner_activo = True

                        scanner_effects = [
                            ScannerEffect(jugador.x, jugador.y)
                        ]

                        # Si el Final Boss ya está activo, el scanner lo marca como escaneado
                        if fase_boss_activa and final_boss is not None:
                            final_boss.marcar_escaneado()

                    elif evento.key == pygame.K_2 and municion_weapon > 0:
                        # El arma poderosa se activa/desactiva solo por decisión del jugador
                        weapon_activo = not weapon_activo

                    elif evento.key == pygame.K_3 and tiene_allies:
                        # Aliados es de un solo uso: se consume al activarlo
                        tiene_allies = False

                        # Si el arma poderosa está activa y hay más de 500 municiones,
                        # las naves aliadas heredan el disparo poderoso.
                        aliados_usan_weapon = weapon_activo and municion_weapon > 500

                        allies_activo = True

                        aliados = [
                            AllyShip(indice, CANTIDAD_ALIADOS)
                            for indice in range(CANTIDAD_ALIADOS)
                        ]

                        # Secuencia especial contra el Final Boss:
                        # Scanner aplicado + arma poderosa activa + llamada a aliados.
                        if (
                                fase_boss_activa
                                and final_boss is not None
                                and final_boss.escaneado
                                and weapon_activo
                                and municion_weapon > 0
                        ):
                            final_boss.iniciar_ataque_masivo()

                    elif evento.key == pygame.K_p:
                        estado = ESTADO_PAUSA
                        opcion_menu_pausa = 0
                        pygame.mouse.set_visible(True)

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # =========================
                # PAUSA
                # =========================
                elif estado == ESTADO_PAUSA:
                    if evento.key == pygame.K_p:
                        estado = ESTADO_JUGANDO

                    elif evento.key == pygame.K_UP:
                        opcion_menu_pausa = (opcion_menu_pausa - 1) % 3

                    elif evento.key == pygame.K_DOWN:
                        opcion_menu_pausa = (opcion_menu_pausa + 1) % 3

                    elif evento.key == pygame.K_RETURN:
                        if opcion_menu_pausa == 0:
                            estado = ESTADO_JUGANDO

                        elif opcion_menu_pausa == 1:
                            reiniciar_partida()
                            estado = ESTADO_JUGANDO

                        elif opcion_menu_pausa == 2:
                            pygame.quit()
                            sys.exit()

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # =========================
                # GAME OVER
                # =========================
                elif estado == ESTADO_GAME_OVER:
                    if evento.key == pygame.K_r:
                        reiniciar_partida()
                        estado = ESTADO_JUGANDO

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    elif evento.key == pygame.K_p:
                        estado = ESTADO_MENU
                        pygame.mouse.set_visible(True)

                elif estado == ESTADO_VICTORIA:
                    if evento.key == pygame.K_RETURN:
                        reiniciar_partida()
                        estado = ESTADO_MENU

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Eventos automáticos solo mientras se juega
            if estado == ESTADO_JUGANDO:
                if (
                        evento.type == EVENTO_CREAR_ENEMIGO
                        and not fase_boss_activa
                        and not tormenta_meteoritos_activa
                        and oleadas_generadas_ciclo < OLEADAS_ANTES_TORMENTA_METEORITOS
                ):
                    nueva_oleada = EnemyWave(jugador)
                    enemigos.extend(nueva_oleada.obtener_enemigos())
                    oleadas_generadas_ciclo += 1

                if evento.type == EVENTO_DISPARO_ENEMIGO and not fase_boss_activa:
                    enemigos_visibles = [
                        enemigo for enemigo in enemigos
                        if enemigo.estado != "esperando" and not enemigo.finalizado
                    ]

                    if len(enemigos_visibles) > 0:
                        enemigo_que_dispara = random.choice(enemigos_visibles)
                        tipo_amenaza = random.choice(["malware", "bug", "alert"])

                        nueva_bala_enemiga = EnemyBullet(
                            enemigo_que_dispara.x,
                            enemigo_que_dispara.y + enemigo_que_dispara.alto // 2,
                            tipo_amenaza
                        )

                        balas_enemigas.append(nueva_bala_enemiga)

                if (
                        evento.type == EVENTO_CREAR_METEORITO
                        and not fase_boss_activa
                        and tormenta_meteoritos_activa
                        and meteoritos_tormenta_generados < TOTAL_METEORITOS_TORMENTA
                ):
                    nuevo_meteorito = Meteor()
                    meteoritos.append(nuevo_meteorito)
                    meteoritos_tormenta_generados += 1

                if evento.type == EVENTO_CREAR_POWERUP and not fase_boss_activa:
                    tipo_powerup = random.choice(["scanner", "weapon", "allies"])
                    nuevo_powerup = PowerUp(tipo_powerup)
                    powerups.append(nuevo_powerup)

                if (
                        evento.type == EVENTO_DISPARO_BOSS
                        and fase_boss_activa
                        and final_boss is not None
                        and not final_boss.esta_destruido()
                        and not derrota_boss_en_proceso
                ):
                    nuevo_misil = BossMissile(
                        final_boss.x,
                        final_boss.y + final_boss.alto // 2,
                        jugador
                    )
                    boss_missiles.append(nuevo_misil)

        # =========================
        # ACTUALIZACIÓN DEL JUEGO
        # =========================

        if estado == ESTADO_INTRO:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio_intro

            if tiempo_transcurrido >= (
                    DURACION_INTRO_ESPERA_MS + DURACION_INTRO_DESPEGUE_MS
            ):
                estado = ESTADO_JUGANDO
                tiempo_inicio_efecto_velocidad_luz_jugando = tiempo_actual
                jugador.x = ANCHO_PANTALLA // 2
                jugador.y = INTRO_JUGADOR_Y
                jugador.rect.center = (jugador.x, jugador.y)
                pygame.mouse.set_visible(not control_mouse)

                if control_mouse:
                    pygame.mouse.set_pos((int(jugador.x), int(jugador.y)))
                    sincronizar_mouse_con_jugador = True
                    frames_sincronizacion_mouse = 10

        if estado == ESTADO_JUGANDO:
            if tiempo_inicio_efecto_velocidad_luz_jugando is not None:
                tiempo_efecto_velocidad_luz = (
                    pygame.time.get_ticks()
                    - tiempo_inicio_efecto_velocidad_luz_jugando
                )

                if tiempo_efecto_velocidad_luz >= DURACION_VELOCIDAD_LUZ_JUGANDO_MS:
                    tiempo_inicio_efecto_velocidad_luz_jugando = None

            teclas = pygame.key.get_pressed()

            # Activar fase Final Boss cuando se cumplen los requisitos
            if (
                    not fase_boss_activa
                    and tiene_scanner
                    and tiene_allies
                    and municion_weapon > 700
            ):
                fase_boss_activa = True
                entrada_boss_en_proceso = True
                tiempo_inicio_entrada_boss = pygame.time.get_ticks()
                punto_aparicion_boss = (ANCHO_PANTALLA // 2, 120)
                boss_previsualizacion_entrada = FinalBoss()
                enemigos_boss_explotados = False

                # Limpiar objetos de apoyo; naves enemigas y meteoritos
                # permanecen visibles hasta que termina el temblor.
                balas_enemigas = []
                powerups = []

                # Cancelar tormenta si estaba activa
                tormenta_meteoritos_activa = False
                meteoritos_tormenta_generados = 0

            if entrada_boss_en_proceso:
                tiempo_entrada_boss = (
                    pygame.time.get_ticks()
                    - tiempo_inicio_entrada_boss
                )
                duracion_total_entrada_boss = (
                    DURACION_TEMBLOR_ENTRADA_BOSS_MS
                    + DURACION_REMOLINO_ENTRADA_BOSS_MS
                )

                if (
                        tiempo_entrada_boss >= DURACION_TEMBLOR_ENTRADA_BOSS_MS
                        and not enemigos_boss_explotados
                ):
                    enemigos_visibles = [
                        enemigo for enemigo in enemigos
                        if enemigo.estado != "esperando" and not enemigo.finalizado
                    ]
                    meteoritos_visibles = meteoritos[:]

                    for enemigo in enemigos_visibles:
                        explosiones.append(
                            Explosion(
                                enemigo.x,
                                enemigo.y,
                                cantidad_particulas=24
                            )
                        )

                    for meteorito in meteoritos_visibles:
                        explosiones.append(
                            Explosion(
                                meteorito.x,
                                meteorito.y,
                                cantidad_particulas=28
                            )
                        )

                    if len(enemigos_visibles) > 0 or len(meteoritos_visibles) > 0:
                        sonidos.reproducir_explosion()

                    enemigos = []
                    meteoritos = []
                    enemigos_boss_explotados = True

                if tiempo_entrada_boss >= duracion_total_entrada_boss:
                    final_boss = boss_previsualizacion_entrada or FinalBoss()
                    final_boss.x, final_boss.y = punto_aparicion_boss
                    final_boss.rect.center = (final_boss.x, final_boss.y)
                    boss_previsualizacion_entrada = None
                    entrada_boss_en_proceso = False

            # Actualizar Final Boss
            if final_boss is not None:
                final_boss.actualizar()

            for misil in boss_missiles[:]:
                misil.actualizar()

                if misil.esta_fuera_de_pantalla():
                    boss_missiles.remove(misil)

            # Activar tormenta de meteoritos después de 10 oleadas completadas
            if (
                    not fase_boss_activa
                    and not tormenta_meteoritos_activa
                    and oleadas_generadas_ciclo >= OLEADAS_ANTES_TORMENTA_METEORITOS
                    and len(enemigos) == 0
            ):
                tormenta_meteoritos_activa = True
                meteoritos_tormenta_generados = 0

            if (
                    final_boss is not None
                    and final_boss.esta_destruido()
                    and not derrota_boss_en_proceso
            ):
                derrota_boss_en_proceso = True
                tiempo_inicio_derrota_boss = pygame.time.get_ticks()
                ultimo_explosion_boss = 0
                posicion_boss_derrotado = (final_boss.x, final_boss.y)

                boss_missiles = []
                pygame.mouse.set_visible(True)

            if derrota_boss_en_proceso:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - tiempo_inicio_derrota_boss

                if tiempo_actual - ultimo_explosion_boss >= INTERVALO_EXPLOSIONES_FINAL_BOSS_MS:
                    ultimo_explosion_boss = tiempo_actual

                    offset_x = random.randint(-70, 70)
                    offset_y = random.randint(-45, 45)

                    explosiones.append(
                        Explosion(
                            posicion_boss_derrotado[0] + offset_x,
                            posicion_boss_derrotado[1] + offset_y,
                            cantidad_particulas=random.randint(20, 38)
                        )
                    )

                    sonidos.reproducir_explosion()

                if tiempo_transcurrido >= (
                        DURACION_EXPLOSIONES_FINAL_BOSS_MS + RETRASO_TRANSICION_VICTORIA_MS
                ):
                    derrota_boss_en_proceso = False
                    final_boss = None
                    estado = ESTADO_VICTORIA



            if control_mouse and sincronizar_mouse_con_jugador:
                jugador.x = ANCHO_PANTALLA // 2
                jugador.y = INTRO_JUGADOR_Y
                jugador.rect.center = (jugador.x, jugador.y)
                pygame.mouse.set_pos((int(jugador.x), int(jugador.y)))

                frames_sincronizacion_mouse -= 1

                if frames_sincronizacion_mouse <= 0:
                    sincronizar_mouse_con_jugador = False
            elif control_mouse:
                posicion_mouse = pygame.mouse.get_pos()

                if posicion_mouse_valida_para_jugador(posicion_mouse):
                    jugador.mover_con_mouse(posicion_mouse)
                else:
                    pygame.mouse.set_pos((int(jugador.x), int(jugador.y)))
            else:
                jugador.mover(teclas)
            botones_mouse = pygame.mouse.get_pressed()

            if teclas[pygame.K_SPACE] or (control_mouse and botones_mouse[0]):
                intentar_disparar()

            for bala in balas[:]:
                bala.actualizar()

                if bala.esta_fuera_de_pantalla():
                    balas.remove(bala)

            for enemigo in enemigos[:]:
                enemigo.actualizar()

                if enemigo.esta_fuera_de_pantalla():
                    enemigos.remove(enemigo)

            for bala_enemiga in balas_enemigas[:]:
                bala_enemiga.actualizar()

                if bala_enemiga.esta_fuera_de_pantalla():
                    balas_enemigas.remove(bala_enemiga)

            for meteorito in meteoritos[:]:
                meteorito.actualizar()

                if meteorito.esta_fuera_de_pantalla():
                    meteoritos.remove(meteorito)

            # Terminar tormenta cuando ya se generaron todos los meteoritos
            # y no queda ninguno en pantalla
            if (
                    tormenta_meteoritos_activa
                    and meteoritos_tormenta_generados >= TOTAL_METEORITOS_TORMENTA
                    and len(meteoritos) == 0
            ):
                tormenta_meteoritos_activa = False
                meteoritos_tormenta_generados = 0
                oleadas_generadas_ciclo = 0

            for powerup in powerups[:]:
                powerup.actualizar()

                if powerup.esta_fuera_de_pantalla():
                    powerups.remove(powerup)

            for explosion in explosiones[:]:
                explosion.actualizar()

                if explosion.finalizada():
                    explosiones.remove(explosion)

            for scanner_effect in scanner_effects[:]:
                scanner_effect.actualizar()

                if scanner_effect.finalizado():
                    scanner_effects.remove(scanner_effect)
                    scanner_activo = False

            for aliado in aliados[:]:
                aliado.actualizar()

                if aliado.puede_disparar():
                    x_disparo, y_disparo = aliado.obtener_posicion_disparo()

                    if aliados_usan_weapon and municion_weapon > 0:
                        nueva_bala = PowerBullet(x_disparo, y_disparo)
                        municion_weapon -= 1

                        if municion_weapon <= 0:
                            municion_weapon = 0
                            aliados_usan_weapon = False
                    else:
                        nueva_bala = Bullet(x_disparo, y_disparo)

                    balas.append(nueva_bala)

                if aliado.finalizado():
                    aliados.remove(aliado)

            if allies_activo and len(aliados) == 0:
                allies_activo = False
                aliados_usan_weapon = False

            # Colisión bala del jugador contra enemigo
            for bala in balas[:]:
                for enemigo in enemigos[:]:
                    if bala.rect.colliderect(enemigo.rect):
                        sonidos.reproducir_impacto_bala()

                        if bala in balas:
                            balas.remove(bala)

                        if enemigo in enemigos:
                            explosiones.append(Explosion(enemigo.x, enemigo.y))
                            sonidos.reproducir_explosion()
                            enemigos.remove(enemigo)

                        puntaje += PUNTOS_ENEMIGO_PEQUENO
                        break

            # Colisión bala del jugador contra meteorito
            for bala in balas[:]:
                for meteorito in meteoritos[:]:
                    if bala.rect.colliderect(meteorito.rect):
                        sonidos.reproducir_impacto_bala()

                        if bala in balas:
                            balas.remove(bala)

                        danio_bala = getattr(bala, "danio", DANIO_BALA_NORMAL)
                        meteorito_destruido = meteorito.recibir_impacto(danio_bala)

                        if meteorito_destruido and meteorito in meteoritos:
                            explosiones.append(
                                Explosion(
                                    meteorito.x,
                                    meteorito.y,
                                    cantidad_particulas=25
                                )
                            )
                            sonidos.reproducir_explosion()
                            meteoritos.remove(meteorito)
                            puntaje += 15

                        break

            # Colisión bala del jugador contra Final Boss
            if final_boss is not None and not final_boss.esta_destruido():
                for bala in balas[:]:
                    if bala.rect.colliderect(final_boss.rect):
                        sonidos.reproducir_impacto_bala()

                        danio_bala = getattr(bala, "danio", DANIO_BALA_NORMAL)
                        final_boss.recibir_danio_minimo(danio_bala)

                        if bala in balas:
                            balas.remove(bala)

            # Colisión bala del jugador contra misil del Boss
            for bala in balas[:]:
                for misil in boss_missiles[:]:
                    if bala.rect.colliderect(misil.rect):
                        sonidos.reproducir_impacto_bala()

                        danio_bala = getattr(bala, "danio", DANIO_BALA_NORMAL)
                        misil_destruido = misil.recibir_impacto(danio_bala)

                        if bala in balas:
                            balas.remove(bala)

                        if misil_destruido and misil in boss_missiles:
                            explosiones.append(
                                Explosion(
                                    misil.x,
                                    misil.y,
                                    cantidad_particulas=18
                                )
                            )
                            sonidos.reproducir_explosion()
                            boss_missiles.remove(misil)

                        break

            # Colisión misil del Boss contra jugador
            for misil in boss_missiles[:]:
                if misil.rect.colliderect(jugador.rect):
                    explosiones.append(
                        Explosion(
                            misil.x,
                            misil.y,
                            cantidad_particulas=24
                        )
                    )
                    sonidos.reproducir_explosion()

                    boss_missiles.remove(misil)
                    aplicar_danio_al_jugador(25, particulas_impacto=24)


            # Colisión enemigo contra jugador
            for enemigo in enemigos[:]:
                if enemigo.rect.colliderect(jugador.rect):
                    explosiones.append(Explosion(enemigo.x, enemigo.y))
                    sonidos.reproducir_explosion()
                    enemigos.remove(enemigo)
                    aplicar_danio_al_jugador(20, particulas_impacto=20)

            # Colisión bala enemiga contra jugador
            for bala_enemiga in balas_enemigas[:]:
                if bala_enemiga.rect.colliderect(jugador.rect):
                    balas_enemigas.remove(bala_enemiga)
                    aplicar_danio_al_jugador(10, particulas_impacto=14)

            # Colisión meteorito contra jugador
            for meteorito in meteoritos[:]:
                if meteorito.rect.colliderect(jugador.rect):
                    explosiones.append(
                        Explosion(
                            meteorito.x,
                            meteorito.y,
                            cantidad_particulas=25
                        )
                    )
                    sonidos.reproducir_explosion()
                    meteoritos.remove(meteorito)
                    aplicar_danio_al_jugador(30, particulas_impacto=30)

            # Colisión power-up contra jugador
            for powerup in powerups[:]:
                if powerup.rect.colliderect(jugador.rect):
                    if powerup.tipo == "scanner":
                        # Scanner no es acumulativo
                        if not tiene_scanner and not scanner_activo:
                            tiene_scanner = True

                    elif powerup.tipo == "weapon":
                        # Arma poderosa sí es acumulativa
                        municion_weapon += MUNICION_ARMA_PODEROSA_POR_POWERUP

                    elif powerup.tipo == "allies":
                        # Aliados no es acumulativo
                        if not tiene_allies and not allies_activo:
                            tiene_allies = True

                    powerups.remove(powerup)

        # =========================
        # DIBUJO EN PANTALLA
        # =========================

        if estado == ESTADO_MENU:
            dibujar_menu_inicio(pantalla, opcion_menu_inicio)

        elif estado == ESTADO_INTRO:
            dibujar_intro_despegue()

        elif estado == ESTADO_JUGANDO:
            dibujar_escena_juego()
            aplicar_temblor_boss_si_activo()

        elif estado == ESTADO_PAUSA:
            dibujar_escena_juego()
            dibujar_menu_pausa(pantalla, opcion_menu_pausa)

        elif estado == ESTADO_GAME_OVER:
            dibujar_escena_juego()

            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO_ALERTA)
            texto_reinicio = fuente.render("Presiona R para reiniciar", True, BLANCO)
            texto_menu = fuente.render("Presiona P para volver al menu inicial", True, BLANCO)
            texto_salir = fuente.render("Presiona ESC para salir", True, BLANCO)

            pantalla.blit(texto_game_over, (230, 230))
            pantalla.blit(texto_reinicio, (270, 310))
            pantalla.blit(texto_menu, (230, 345))
            pantalla.blit(texto_salir, (290, 380))

        elif estado == ESTADO_VICTORIA:
            pantalla.fill(NEGRO)

            texto_victoria = fuente_grande.render("YOU WIN!", True, VERDE_CYBER)
            pantalla.blit(
                texto_victoria,
                texto_victoria.get_rect(center=(ANCHO_PANTALLA // 2, 220))
            )

            lineas_victoria = [
                "Has derrotado al Final Boss",
                "La Tierra ha sido defendida con exito",
                "CyberHack vuelve a la base"
            ]

            y_inicial = 310
            separacion = 36

            for indice, linea in enumerate(lineas_victoria):
                texto_linea = fuente.render(linea, True, BLANCO)
                pantalla.blit(
                    texto_linea,
                    texto_linea.get_rect(
                        center=(ANCHO_PANTALLA // 2, y_inicial + indice * separacion)
                    )
                )

            texto_menu = fuente.render("Presiona ENTER para volver al menu inicial", True, BLANCO)
            texto_salir = fuente.render("Presiona ESC para salir", True, BLANCO)

            pantalla.blit(
                texto_menu,
                texto_menu.get_rect(center=(ANCHO_PANTALLA // 2, 450))
            )

            pantalla.blit(
                texto_salir,
                texto_salir.get_rect(center=(ANCHO_PANTALLA // 2, 490))
            )

        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()
