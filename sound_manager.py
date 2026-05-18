# sound_manager.py

import os
import sys
import pygame


class SonidoNulo:
    """Representa un sonido inactivo cuando el audio no está disponible."""

    def set_volume(self, _volumen):
        # No realiza acción: mantiene la misma interfaz que pygame.mixer.Sound.
        return None

    def play(self, *args, **kwargs):
        # No realiza acción: evita errores cuando el juego intenta reproducir un sonido no cargado.
        return None


class SoundManager:
    def __init__(self):
        self.ruta_sonidos = os.path.join("assets", "sounds")
        self.ruta_musica = os.path.join("assets", "sounds", "source", "music")
        self.audio_web = sys.platform == "emscripten"
        self.motores_constantes_habilitados = not self.audio_web
        self.audio_disponible = self.inicializar_audio()

        self.sonido_disparo = self.cargar_sonido("player_shoot.wav")
        self.sonido_impacto_bala = self.cargar_sonido("bullet_impact.wav")
        self.sonido_explosion = self.cargar_sonido("explosion.wav")
        self.sonido_danio = self.cargar_sonido("player_damage.wav")
        self.sonido_game_over = self.cargar_sonido("game_over.wav")
        self.sonido_motor_enemigo = self.cargar_sonido("sound_motor_enemy_ship.wav")
        self.sonido_misil_boss = self.cargar_sonido("boss_misil.wav")

        self.musica_actual = None
        self.canal_motor_jugador = self.crear_canal(8)
        self.canal_motor_boss = self.crear_canal(9)
        self.canales_motor_enemigos = [self.crear_canal(indice) for indice in range(10, 26)]
        self.motor_jugador = self.cargar_sonido_music_source("ship_engine_loop.mp3")
        self.motor_boss = self.cargar_sonido_music_source("final_boss_engine_loop.mp3")

        # Volúmenes
        self.sonido_disparo.set_volume(0.30)
        self.sonido_impacto_bala.set_volume(0.42)
        self.sonido_explosion.set_volume(0.35)
        self.sonido_danio.set_volume(0.35)
        self.sonido_game_over.set_volume(0.45)
        self.sonido_motor_enemigo.set_volume(0.12)
        self.sonido_misil_boss.set_volume(0.45)

        if self.motor_jugador is not None:
            self.motor_jugador.set_volume(0.18)

        if self.motor_boss is not None:
            self.motor_boss.set_volume(0.22)

    def inicializar_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.set_num_channels(32)
            return True
        except pygame.error:
            return False

    def crear_canal(self, indice):
        if not self.audio_disponible:
            return None

        try:
            return pygame.mixer.Channel(indice)
        except pygame.error:
            return None

    def cargar_sonido(self, nombre_archivo):
        if not self.audio_disponible:
            return SonidoNulo()

        if self.audio_web:
            nombre_archivo = self.obtener_nombre_audio_web(nombre_archivo)

        ruta = os.path.join(self.ruta_sonidos, nombre_archivo)

        try:
            return pygame.mixer.Sound(ruta)
        except pygame.error:
            return SonidoNulo()

    def cargar_sonido_music_source(self, nombre_archivo):
        if not self.audio_disponible:
            return None

        if self.audio_web:
            nombre_archivo = self.obtener_nombre_audio_web(nombre_archivo)

        ruta = os.path.join(self.ruta_musica, nombre_archivo)

        if not os.path.exists(ruta):
            return None

        try:
            return pygame.mixer.Sound(ruta)
        except pygame.error:
            return None

    def obtener_ruta_musica(self, nombre_archivo):
        if self.audio_web:
            nombre_archivo = self.obtener_nombre_audio_web(nombre_archivo)

        ruta = os.path.join(self.ruta_musica, nombre_archivo)

        if not os.path.exists(ruta):
            return None

        return ruta

    def obtener_nombre_audio_web(self, nombre_archivo):
        nombre_base, _ = os.path.splitext(nombre_archivo)
        return f"{nombre_base}.ogg"

    def reproducir_musica(self, nombre_archivo, volumen=0.45, repetir=-1):
        if not self.audio_disponible:
            return

        if self.musica_actual == nombre_archivo:
            return

        ruta = self.obtener_ruta_musica(nombre_archivo)

        if ruta is None:
            self.detener_musica()
            self.musica_actual = None
            return

        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(repetir)
            self.musica_actual = nombre_archivo
        except pygame.error:
            self.detener_musica()
            self.musica_actual = None

    def detener_musica(self):
        if self.audio_disponible:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass

        self.musica_actual = None

    def reproducir_motor_jugador(self):
        if not self.motores_constantes_habilitados:
            return

        if self.motor_jugador is None or self.canal_motor_jugador is None:
            return

        if not self.canal_motor_jugador.get_busy():
            self.canal_motor_jugador.play(self.motor_jugador, loops=-1)

    def detener_motor_jugador(self):
        if self.canal_motor_jugador is not None:
            self.canal_motor_jugador.stop()

    def reproducir_motor_boss(self):
        if not self.motores_constantes_habilitados:
            return

        if self.motor_boss is None or self.canal_motor_boss is None:
            return

        if not self.canal_motor_boss.get_busy():
            self.canal_motor_boss.play(self.motor_boss, loops=-1)

    def detener_motor_boss(self):
        if self.canal_motor_boss is not None:
            self.canal_motor_boss.stop()

    def actualizar_motores_enemigos(self, cantidad_enemigos):
        if not self.motores_constantes_habilitados:
            self.detener_motores_enemigos()
            return

        cantidad_activa = min(cantidad_enemigos, len(self.canales_motor_enemigos))

        for indice, canal in enumerate(self.canales_motor_enemigos):
            if canal is None:
                continue

            if indice < cantidad_activa:
                if not canal.get_busy():
                    canal.play(self.sonido_motor_enemigo, loops=-1)
            else:
                canal.stop()

    def detener_motores_enemigos(self):
        for canal in self.canales_motor_enemigos:
            if canal is not None:
                canal.stop()

    def actualizar_audio_estado(
        self,
        estado,
        fase_boss_activa=False,
        final_boss_activo=False,
        enemigos_activos=0
    ):
        if estado == "menu":
            self.reproducir_musica("menu_start.mp3", volumen=0.7)
            self.detener_motor_jugador()
            self.detener_motor_boss()
            self.detener_motores_enemigos()

        elif estado == "intro":
            self.reproducir_musica("intro.mp3", volumen=0.6, repetir=0)
            self.reproducir_motor_jugador()
            self.detener_motor_boss()
            self.detener_motores_enemigos()

        elif estado == "jugando":
            if fase_boss_activa:
                self.reproducir_musica("boss_appearance.mp3", volumen=0.8)
            else:
                self.reproducir_musica("gameplay.mp3", volumen=0.7)

            self.reproducir_motor_jugador()

            if final_boss_activo:
                self.reproducir_motor_boss()
            else:
                self.detener_motor_boss()

            self.actualizar_motores_enemigos(enemigos_activos)

        elif estado == "pausa":
            self.reproducir_musica("pause_menu.mp3", volumen=0.35)
            self.detener_motor_jugador()
            self.detener_motor_boss()
            self.detener_motores_enemigos()

        elif estado == "game_over":
            self.reproducir_musica("game_over.mp3", volumen=0.8, repetir=0)
            self.detener_motor_jugador()
            self.detener_motor_boss()
            self.detener_motores_enemigos()

        elif estado == "victoria":
            self.reproducir_musica("victory.mp3", volumen=0.9, repetir=0)
            self.detener_motor_jugador()
            self.detener_motor_boss()
            self.detener_motores_enemigos()

    def reproducir_disparo(self):
        self.sonido_disparo.play()

    def reproducir_impacto_bala(self):
        self.sonido_impacto_bala.play()

    def reproducir_explosion(self):
        self.sonido_explosion.play()

    def reproducir_danio(self):
        self.sonido_danio.play()

    def reproducir_game_over(self):
        self.sonido_game_over.play()

    def reproducir_misil_boss(self):
        self.sonido_misil_boss.play()
