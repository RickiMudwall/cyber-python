# Cyber Python

**Cyber Python** es un juego arcade retro desarrollado en Python con Pygame.  
El jugador controla la nave **CyberHack**, encargada de defender la Tierra frente a una invasión de naves alienígenas y amenazas digitales.

El proyecto forma parte de mi portafolio técnico para demostrar habilidades prácticas en Python, organización de código, lógica de videojuegos, Git y GitHub.

---

## Objetivo del juego

Controlar la nave CyberHack, esquivar enemigos, disparar, sumar puntos y sobrevivir el mayor tiempo posible.

En futuras versiones, el jugador deberá recolectar herramientas de ciberseguridad como escáner, arma avanzada y apoyo de naves aliadas para derrotar al Final Boss.

---

## Estado actual del proyecto

Versión actual:

```text
MVP 1.2
```
Funcionalidades implementadas:

Ventana principal del juego.
Nave controlable con teclado.
Movimiento horizontal, vertical y diagonal.
Fondo espacial animado.
Disparo con barra espaciadora.
Enemigos que aparecen desde la parte superior.
- Enemigos que disparan proyectiles hacia el jugador.
- Proyectiles enemigos con temática de amenazas digitales: malware, bug y alert.
- Daño al jugador por impacto de proyectiles enemigos.
Colisiones entre balas y enemigos.
Sistema de puntaje.
Sistema de energía.
Sistema de 3 vidas.
Pantalla de Game Over.
Reinicio de partida con tecla R.
Salida del juego con tecla ESC.
Controles
Acción	Tecla
Mover izquierda	Flecha izquierda
Mover derecha	Flecha derecha
Mover adelante	Flecha arriba
Mover atrás	Flecha abajo
Movimiento diagonal	Combinación de flechas
Disparar	Spacebar
Reiniciar en Game Over	R
Salir en Game Over	ESC

| Acción | Tecla |
|---|---|
| Mover nave con teclado | Flechas direccionales |
| Activar/desactivar control con mouse | M |
| Disparar | Spacebar |
| Pausar / continuar | P |
| Seleccionar opción de menú | Enter |
| Mover selección de menú | Flecha arriba / Flecha abajo |
| Reiniciar en Game Over | R |
| Salir | ESC |

| Activar Scanner | 1 |
| Activar/desactivar arma poderosa | 2 |
| Llamar naves aliadas | 3 |


> Los enemigos disparan automáticamente amenazas digitales que reducen la energía del jugador.
- Meteoritos que aparecen desde la parte superior.
- Meteoritos con resistencia de 3 impactos.
- Meteoritos destructibles con disparos del jugador.
- Daño al jugador por colisión con meteoritos.
- Puntaje adicional al destruir meteoritos.

- Explosiones simples por partículas.
- Efectos visuales al destruir enemigos.
- Efectos visuales al destruir meteoritos.
- Explosiones al impactar enemigos o meteoritos contra el jugador.

- Sprites básicos para la nave del jugador.
- Sprites básicos para naves enemigas.
- Sprites básicos para balas del jugador.
- Sprites básicos para proyectiles enemigos.
- Sprites básicos para meteoritos.
- Assets generados localmente en `assets/images/`.
- Feedback visual de daño sobre la nave del jugador.





- Sonidos básicos generados localmente.
- Sonido de disparo del jugador.
- Sonido de impacto de bala.
- Sonido de explosión.
- Sonido de daño recibido por el jugador.
- Sonido de Game Over.
- Administrador de sonidos separado en `sound_manager.py`.


- Menú inicial con opciones Start y Salir.
- Sistema de pausa con la tecla P.
- Menú de pausa con opciones Continuar, Reiniciar y Salir.
- Retorno al menú inicial desde Game Over.
- Control alternativo con mouse.
- Cambio de modo de control con la tecla M.
- Visualización del modo de control actual en pantalla.



- Sistema base de power-ups.
- Power-up Scanner de un solo uso.
- Efecto visual de escáner con onda expansiva circular.
- Power-up Arma poderosa con munición acumulable.
- Cada power-up de arma poderosa entrega 100 unidades de munición.
- Disparo poderoso con proyectil más grande y menor cadencia.
- El arma poderosa permanece activa hasta desactivarla con la tecla 2 o agotar munición.
- Power-up de llamada a naves aliadas.
- Las naves aliadas aparecen con trayectorias parabólicas aleatorias.
- Las naves aliadas disparan durante 5 segundos.
- Las naves aliadas se retiran con trayectorias parabólicas.
- Las naves aliadas heredan el arma poderosa si está activa y hay más de 500 municiones.
- Scanner y Aliados son consumibles de un solo uso.


- Final Boss con sprite propio.
- Aparición del Final Boss al tener Scanner, Aliados y más de 700 municiones de arma poderosa.
- Al aparecer el Final Boss se detienen enemigos normales, meteoritos y power-ups.
- Final Boss con barra de vida.
- Final Boss con movimiento lateral.
- El Scanner marca al Final Boss como escaneado.
- El Final Boss recibe daño mínimo con disparos normales o poderosos.
- Secuencia especial de victoria: Scanner → Arma poderosa → Aliados.
- Ataque masivo que destruye al Final Boss después de 5 segundos.
- Pantalla de victoria `YOU WIN!`.
- Retorno al menú inicial desde la pantalla de victoria.

- Misiles teledirigidos del Final Boss.
- Los misiles persiguen la posición actual de la nave del jugador.
- Los misiles pueden ser destruidos con disparos.
- Los misiles reciben más daño con arma poderosa.
- Los misiles causan daño al jugador si impactan.
- Los misiles desaparecen al derrotar al Final Boss.


Tecnologías utilizadas
Python 3.9
Pygame CE
PyCharm
Git
GitHub
Estructura del proyecto
cyber-runner-pygame/
│
├── main.py          # Motor principal del juego
├── settings.py      # Configuración global
├── player.py        # Clase del jugador
├── bullet.py        # Clase de disparos
├── enemy.py         # Clase de enemigos
├── starfield.py     # Fondo animado de estrellas
├── README.md        # Documentación del proyecto
├── .gitignore       # Archivos excluidos del control de versiones
│
└── assets/
    ├── images/      # Imágenes futuras del juego
    └── sounds/      # Sonidos futuros del juego
Instalación y ejecución local

Clonar el repositorio:

git clone URL_DEL_REPOSITORIO
cd cyber-runner-pygame

Crear entorno virtual:

python3 -m venv .venv
source .venv/bin/activate


Instalar dependencias:


pip install -r requirements.txt

Ejecutar el juego:

python3 main.py


Roadmap

Próximas mejoras planificadas:
- Mejorar explosiones con sprites animados y sonido.
- Mejorar meteoritos con sprites y animaciones.
Agregar enemigos medianos.
Agregar disparos enemigos.
- Agregar música de fondo y mejorar efectos de sonido.
- Mejorar diseño visual del menú inicial.
Agregar pantalla de victoria.
- Mejorar balance de power-ups.
- Agregar efectos visuales avanzados para Scanner, Arma poderosa y Aliados.
- Balancear frecuencia, velocidad y daño de los misiles del Final Boss.
- Agregar nuevos patrones de ataque del Final Boss.
- Mejorar estética visual del Final Boss.
- Agregar música de victoria.
- Balancear dificultad del combate final.
Agregar Final Boss.
Empaquetar como ejecutable.
Publicar versión jugable en navegador con GitHub Pages.
Concepto narrativo

La Tierra está siendo invadida por naves alienígenas que atacan usando amenazas digitales como malware, bugs y falsas alertas.

CyberHack, líder de una unidad de defensa tecnológica, debe destruir oleadas enemigas, recolectar herramientas estratégicas y coordinar a su equipo de naves aliadas para vencer al enemigo principal.

Aprendizajes técnicos aplicados

Este proyecto permite practicar:

Programación orientada a objetos.
Separación de responsabilidades por archivos.
Manejo de eventos de teclado.
Renderizado gráfico con Pygame.
Detección de colisiones.
Control de estado del juego.
Uso de Git para control de versiones.
Documentación técnica para portafolio.
Autor

Proyecto desarrollado por Ricardo Nabor Tapia Poblete como parte de su portafolio técnico en Python, automatización, QA, IA y ciberseguridad.