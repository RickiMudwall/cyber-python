# settings.py

# =========================
# CONFIGURACIÓN DE PANTALLA
# =========================

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

TITULO_JUEGO = "Cyber Python"


# =========================
# COLORES RGB
# =========================

NEGRO = (10, 10, 18)
BLANCO = (255, 255, 255)
VERDE_CYBER = (0, 255, 120)
AZUL_CYBER = (0, 180, 255)
ROJO_ALERTA = (255, 60, 60)
AMARILLO = (255, 220, 80)
GRIS_OSCURO = (35, 35, 45)
GRIS_CLARO = (160, 160, 170)
MORADO_CYBER = (180, 80, 255)


# =========================
# JUGADOR
# =========================

VELOCIDAD_JUGADOR = 5
ANCHO_JUGADOR = 50
ALTO_JUGADOR = 60

VIDAS_INICIALES = 3
ENERGIA_INICIAL = 100


# =========================
# DISPAROS
# =========================

VELOCIDAD_BALA = 8
ANCHO_BALA = 6
ALTO_BALA = 14


# =========================
# ENEMIGOS
# =========================

VELOCIDAD_ENEMIGO = 2
ANCHO_ENEMIGO = 45
ALTO_ENEMIGO = 45

PUNTOS_ENEMIGO_PEQUENO = 10
PUNTOS_ENEMIGO_MEDIANO = 50
PUNTOS_FINAL_BOSS = 500

# =========================
# ESTADOS DEL JUEGO
# =========================

ESTADO_MENU = "menu"
ESTADO_JUGANDO = "jugando"
ESTADO_PAUSA = "pausa"
ESTADO_GAME_OVER = "game_over"

# =========================
# POWER-UPS
# =========================

# Escáner
DURACION_SCANNER_MS = 1200
VELOCIDAD_EXPANSION_SCANNER = 18

# Arma poderosa
CADENCIA_ARMA_NORMAL_MS = 180
CADENCIA_ARMA_PODEROSA_MS = 50
MUNICION_ARMA_PODEROSA_POR_POWERUP = 100

ANCHO_BALA_PODEROSA = 18
ALTO_BALA_PODEROSA = 42
VELOCIDAD_BALA_PODEROSA = 7

DANIO_BALA_NORMAL = 1
DANIO_BALA_PODEROSA = 3

# Aliados
CANTIDAD_ALIADOS = 4
DURACION_ALIADOS_MS = 5000
CADENCIA_DISPARO_ALIADO_MS = 450