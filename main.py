# main.py

import pygame
import sys
import random

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    FPS,
    TITULO_JUEGO,
    NEGRO,
    VERDE_CYBER,
    BLANCO,
    ROJO_ALERTA,
    PUNTOS_ENEMIGO_PEQUENO,
    VIDAS_INICIALES,
    ENERGIA_INICIAL,
    ESTADO_MENU,
    ESTADO_JUGANDO,
    ESTADO_PAUSA,
    ESTADO_GAME_OVER,
)

from player import Player
from bullet import Bullet
from enemy import Enemy
from enemy_bullet import EnemyBullet
from meteor import Meteor
from explosion import Explosion
from starfield import StarField
from sound_manager import SoundManager
from ui import dibujar_menu_inicio, dibujar_menu_pausa


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
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
    control_mouse = False

    # Variables de partida
    jugador = Player()
    balas = []
    enemigos = []
    balas_enemigas = []
    meteoritos = []
    explosiones = []

    puntaje = 0
    vidas = VIDAS_INICIALES
    energia = ENERGIA_INICIAL

    EVENTO_CREAR_ENEMIGO = pygame.USEREVENT + 1
    EVENTO_DISPARO_ENEMIGO = pygame.USEREVENT + 2
    EVENTO_CREAR_METEORITO = pygame.USEREVENT + 3

    pygame.time.set_timer(EVENTO_CREAR_ENEMIGO, 1200)
    pygame.time.set_timer(EVENTO_DISPARO_ENEMIGO, 900)
    pygame.time.set_timer(EVENTO_CREAR_METEORITO, 1800)

    def reiniciar_partida():
        nonlocal jugador, balas, enemigos, balas_enemigas, meteoritos
        nonlocal explosiones, puntaje, vidas, energia

        jugador = Player()
        balas = []
        enemigos = []
        balas_enemigas = []
        meteoritos = []
        explosiones = []

        puntaje = 0
        vidas = VIDAS_INICIALES
        energia = ENERGIA_INICIAL

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

        pantalla.blit(texto_titulo, (20, 20))
        pantalla.blit(texto_puntaje, (20, 50))
        pantalla.blit(texto_vidas, (20, 80))
        pantalla.blit(texto_energia, (20, 110))
        pantalla.blit(texto_pausa, (ANCHO_PANTALLA - 120, 20))
        pantalla.blit(texto_control, (ANCHO_PANTALLA - 210, 50))


        for bala in balas:
            bala.dibujar(pantalla)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        for bala_enemiga in balas_enemigas:
            bala_enemiga.dibujar(pantalla)

        for meteorito in meteoritos:
            meteorito.dibujar(pantalla)

        for explosion in explosiones:
            explosion.dibujar(pantalla)

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
                            estado = ESTADO_JUGANDO

                        elif opcion_menu_inicio == 1:
                            pygame.quit()
                            sys.exit()

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # =========================
                # JUEGO ACTIVO
                # =========================
                elif estado == ESTADO_JUGANDO:
                    if evento.key == pygame.K_SPACE:
                        nueva_bala = Bullet(jugador.x, jugador.y - jugador.alto // 2)
                        balas.append(nueva_bala)
                        sonidos.reproducir_disparo()

                    elif evento.key == pygame.K_m:
                        control_mouse = not control_mouse

                        if control_mouse:
                            pygame.mouse.set_visible(False)
                        else:
                            pygame.mouse.set_visible(True)

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

            # Eventos automáticos solo mientras se juega
            if estado == ESTADO_JUGANDO:
                if evento.type == EVENTO_CREAR_ENEMIGO:
                    nuevo_enemigo = Enemy()
                    enemigos.append(nuevo_enemigo)

                if evento.type == EVENTO_DISPARO_ENEMIGO:
                    if len(enemigos) > 0:
                        enemigo_que_dispara = random.choice(enemigos)
                        tipo_amenaza = random.choice(["malware", "bug", "alert"])

                        nueva_bala_enemiga = EnemyBullet(
                            enemigo_que_dispara.x,
                            enemigo_que_dispara.y + enemigo_que_dispara.alto // 2,
                            tipo_amenaza
                        )

                        balas_enemigas.append(nueva_bala_enemiga)

                if evento.type == EVENTO_CREAR_METEORITO:
                    nuevo_meteorito = Meteor()
                    meteoritos.append(nuevo_meteorito)

        # =========================
        # ACTUALIZACIÓN DEL JUEGO
        # =========================

        if estado == ESTADO_JUGANDO:
            teclas = pygame.key.get_pressed()

            if control_mouse:
                posicion_mouse = pygame.mouse.get_pos()
                jugador.mover_con_mouse(posicion_mouse)
            else:
                jugador.mover(teclas)

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

            for explosion in explosiones[:]:
                explosion.actualizar()

                if explosion.finalizada():
                    explosiones.remove(explosion)

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

                        meteorito_destruido = meteorito.recibir_impacto()

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

        # =========================
        # DIBUJO EN PANTALLA
        # =========================

        if estado == ESTADO_MENU:
            dibujar_menu_inicio(pantalla, opcion_menu_inicio)

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

        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()