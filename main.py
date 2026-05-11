# main.py

import pygame
import sys
import random
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
    VELOCIDAD_SCROLL_DESPEGUE,
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
    DURACION_EXPLOSIONES_FINAL_BOSS_MS,
    INTERVALO_EXPLOSIONES_FINAL_BOSS_MS,
    RETRASO_TRANSICION_VICTORIA_MS,
    INTRO_DIALOGO_SLIDE_MS,
    INTRO_DIALOGO_HOLD_MS,
    INTRO_DIALOGO_ANCHO,
    INTRO_DIALOGO_ALTO,
    INTRO_DIALOGO_MARGEN_LATERAL,
    INTRO_DIALOGO_MARGEN_SUPERIOR,
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

    # Estado inicial
    estado = ESTADO_MENU
    opcion_menu_inicio = 0
    opcion_menu_pausa = 0
    tiempo_inicio_intro = 0
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
        nonlocal boss_missiles
        nonlocal oleadas_generadas_ciclo
        nonlocal tormenta_meteoritos_activa
        nonlocal meteoritos_tormenta_generados
        nonlocal derrota_boss_en_proceso
        nonlocal tiempo_inicio_derrota_boss
        nonlocal ultimo_explosion_boss
        nonlocal posicion_boss_derrotado

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

        oleadas_generadas_ciclo = 0
        tormenta_meteoritos_activa = False
        meteoritos_tormenta_generados = 0

        derrota_boss_en_proceso = False
        tiempo_inicio_derrota_boss = 0
        ultimo_explosion_boss = 0
        posicion_boss_derrotado = (0, 0)

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

        desplazamiento = int(
            progreso_despegue
            * VELOCIDAD_SCROLL_DESPEGUE
            * 120
        )

        # =========================
        # Tierra al fondo
        # =========================
        tierra_x = ANCHO_PANTALLA // 2
        tierra_y = 130 + desplazamiento
        radio_tierra = 210

        pygame.draw.circle(
            pantalla,
            (0, 90, 190),
            (tierra_x, tierra_y),
            radio_tierra
        )

        pygame.draw.circle(
            pantalla,
            (0, 180, 255),
            (tierra_x, tierra_y),
            radio_tierra,
            4
        )

        # Continentes simples
        pygame.draw.ellipse(
            pantalla,
            (30, 180, 90),
            (tierra_x - 120, tierra_y - 70, 120, 55)
        )

        pygame.draw.ellipse(
            pantalla,
            (30, 180, 90),
            (tierra_x + 20, tierra_y + 20, 130, 60)
        )

        pygame.draw.ellipse(
            pantalla,
            (30, 150, 80),
            (tierra_x - 40, tierra_y + 80, 90, 45)
        )

        # =========================
        # Estación / bahía de despegue
        # =========================
        estacion_y = 260 + desplazamiento

        # Plataforma principal
        pygame.draw.rect(
            pantalla,
            (35, 35, 45),
            (ANCHO_PANTALLA // 2 - 210, estacion_y, 420, 420),
            border_radius=18
        )

        pygame.draw.rect(
            pantalla,
            AZUL_CYBER,
            (ANCHO_PANTALLA // 2 - 210, estacion_y, 420, 420),
            3,
            border_radius=18
        )

        # Pista central
        pygame.draw.rect(
            pantalla,
            (15, 15, 22),
            (ANCHO_PANTALLA // 2 - 55, estacion_y + 20, 110, 390),
            border_radius=12
        )

        pygame.draw.rect(
            pantalla,
            VERDE_CYBER,
            (ANCHO_PANTALLA // 2 - 55, estacion_y + 20, 110, 390),
            2,
            border_radius=12
        )

        # Líneas de pista
        for i in range(8):
            y_linea = estacion_y + 50 + i * 42
            pygame.draw.line(
                pantalla,
                VERDE_CYBER,
                (ANCHO_PANTALLA // 2, y_linea),
                (ANCHO_PANTALLA // 2, y_linea + 20),
                3
            )

        # Laterales de la estación
        pygame.draw.rect(
            pantalla,
            (60, 60, 75),
            (ANCHO_PANTALLA // 2 - 300, estacion_y + 80, 90, 220),
            border_radius=12
        )

        pygame.draw.rect(
            pantalla,
            (60, 60, 75),
            (ANCHO_PANTALLA // 2 + 210, estacion_y + 80, 90, 220),
            border_radius=12
        )

        # =========================
        # Nave del jugador fija
        # =========================
        jugador.x = ANCHO_PANTALLA // 2
        jugador.y = ALTO_PANTALLA - 170
        jugador.rect.center = (jugador.x, jugador.y)
        jugador.dibujar(pantalla)

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

        if final_boss is not None:
            final_boss.dibujar(
                pantalla,
                mostrar_destruido=derrota_boss_en_proceso
            )

        for explosion in explosiones:
            explosion.dibujar(pantalla)

        for misil in boss_missiles:
            misil.dibujar(pantalla)

        jugador.dibujar(pantalla)

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

                if evento.type == EVENTO_CREAR_POWERUP:
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
                pygame.mouse.set_visible(not control_mouse)

                if control_mouse:
                    pygame.mouse.set_pos((int(jugador.x), int(jugador.y)))

        if estado == ESTADO_JUGANDO:
            teclas = pygame.key.get_pressed()

            # Activar fase Final Boss cuando se cumplen los requisitos
            if (
                    not fase_boss_activa
                    and tiene_scanner
                    and tiene_allies
                    and municion_weapon > 700
            ):
                fase_boss_activa = True
                final_boss = FinalBoss()

                # El Final Boss destruye a las naves enemigas activas al aparecer
                enemigos_visibles = [
                    enemigo for enemigo in enemigos
                    if enemigo.estado != "esperando" and not enemigo.finalizado
                ]

                for enemigo in enemigos_visibles:
                    explosiones.append(
                        Explosion(
                            enemigo.x,
                            enemigo.y,
                            cantidad_particulas=24
                        )
                    )

                if len(enemigos_visibles) > 0:
                    sonidos.reproducir_explosion()

                # Limpiar campo para iniciar fase Boss
                enemigos = []
                meteoritos = []
                balas_enemigas = []
                powerups = []

                # Cancelar tormenta si estaba activa
                tormenta_meteoritos_activa = False
                meteoritos_tormenta_generados = 0

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



            if control_mouse:
                posicion_mouse = pygame.mouse.get_pos()
                jugador.mover_con_mouse(posicion_mouse)
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
            texto_mensaje = fuente.render("Has derrotado al Final Boss", True, BLANCO)
            texto_menu = fuente.render("Presiona ENTER para volver al menu inicial", True, BLANCO)
            texto_salir = fuente.render("Presiona ESC para salir", True, BLANCO)

            pantalla.blit(texto_victoria, (250, 220))
            pantalla.blit(texto_mensaje, (250, 300))
            pantalla.blit(texto_menu, (190, 340))
            pantalla.blit(texto_salir, (290, 380))

        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()