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
MVP 1.4 Diálogos cinemáticos con imágenes completas

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



### Nuevas funcionalidades

En esta versión se incorporó una mejora importante al flujo del juego, agregando fases de combate más ordenadas y una escena inicial previa al gameplay.

### Intro cinemática de despegue

Al presionar `Start`, el juego ya no inicia directamente en combate. Ahora se muestra una escena inicial donde:

- La nave aparece en una bahía de despegue.
- Se visualiza la Tierra al fondo.
- La estación espacial permanece visible durante la preparación.
- Luego se ejecuta una animación de despegue.
- La estación y el planeta se desplazan hacia abajo para simular que la nave despega.
- Al finalizar la intro, el jugador toma el control de la nave.

### Diálogos temporales en la intro

Durante la escena inicial se agregaron cuadros de diálogo animados:

- Mensaje izquierdo: aparece desde fuera de la pantalla por la izquierda.
- Mensaje derecho: aparece desde fuera de la pantalla por la derecha.
- Cada mensaje permanece visible unos segundos y luego se retira.
- Se agregó un avatar temporal tipo anime placeholder.
- Los textos actuales son temporales: `Interaccion 1`, `Interaccion 2`, `Interaccion 3`.

Estos elementos quedan preparados para reemplazarse más adelante por arte final estilo anime/cyberpunk.

### Oleadas enemigas

Las naves enemigas pequeñas ahora aparecen en oleadas:

- Cantidad aleatoria de enemigos por oleada.
- Formación ordenada en fila.
- Aparición secuencial una nave tras otra.
- Trayectoria curva tipo parabólica.
- Aproximación peligrosa hacia la nave del jugador.
- Escape fuera de pantalla si no son destruidas.
- Las naves disparan durante su trayectoria.

### Ciclo de combate

Se agregó una estructura de fases:



```text
10 oleadas enemigas
↓
tormenta de meteoritos
↓
10 oleadas enemigas
↓
nueva tormenta de meteoritos

Durante la tormenta de meteoritos:

No aparecen nuevas oleadas enemigas.
Se generan aproximadamente 50 meteoritos.
Los meteoritos tienen distintos tamaños.
Al pasar o destruirse todos, vuelven las oleadas enemigas.
Entrada del Final Boss

Cuando se activa la condición del Final Boss:

Las naves enemigas activas desaparecen.
Cada nave enemiga visible explota antes de ser retirada.
Se refuerza visualmente la entrada del Final Boss como una amenaza dominante.
Derrota del Final Boss

Al destruir al Final Boss:

El sprite del Boss permanece visible.
Se generan múltiples explosiones sobre él durante varios segundos.
La transición hacia la pantalla YOU WIN es más cinematográfica que en versiones anteriores.
Control y jugabilidad

Se mejoró la interacción del jugador:

El juego inicia en modo mouse por defecto.
La tecla M alterna entre control con mouse y teclado.
En modo mouse, el clic izquierdo dispara.
Mantener clic izquierdo presionado activa disparo automático.
Mantener Spacebar presionado activa disparo automático.
La cadencia de disparo respeta el tipo de arma activa.
El juego puede ejecutarse en pantalla completa.
Controles principales
Acción	Control
Iniciar partida	Enter
Mover nave con mouse	Mouse
Alternar mouse/teclado	M
Disparar	Clic izquierdo o Spacebar
Activar Scanner	1
Activar / desactivar arma poderosa	2
Llamar aliados	3
Pausar	P
Salir	ESC
Archivos modificados principales
main.py
settings.py
enemy.py
enemy_wave.py
final_boss.py
Estado


### Mejora incorporada

Se reemplazó el sistema inicial de diálogos tipo tarjeta por un sistema de paneles cinemáticos basados en imágenes completas.

Ahora cada diálogo puede ser diseñado como una imagen independiente que incluye:

- Fondo visual propio.
- Personaje, escena o elemento narrativo.
- Frase integrada dentro de la imagen.
- Estilo visual libre, como anime, cyberpunk, sci-fi o panel narrativo.

Esto permite que los diálogos no dependan de texto renderizado por Pygame, sino de arte diseñado previamente.

### Diálogos de la intro

Durante la escena inicial de despegue se muestran tres paneles de diálogo:

```text
dialog_intro_1.png
dialog_intro_2.png
dialog_intro_3.png

Versión en desarrollo validada manualmente en rama:

feature/enemy-waves



Comportamiento visual

Los paneles mantienen la lógica animada de entrada y salida:

El primer diálogo aparece desde la izquierda.
El segundo diálogo aparece desde la derecha.
El tercer diálogo aparece nuevamente desde la izquierda.
Cada panel permanece visible durante unos segundos.
Luego se retira por el mismo lado desde donde apareció.
Sistema reutilizable

Se agregó el archivo:

dialog_sequence.py

Este componente permite definir secuencias de diálogos reutilizables, por lo que más adelante se podrán agregar nuevos diálogos durante:

La intro.
Aparición del Final Boss.
Tormentas de meteoritos.
Momentos críticos de baja energía.
Victoria o derrota.
Eventos narrativos especiales durante el gameplay.
Tamaño recomendado de imágenes

Para buena calidad visual, se recomienda crear las imágenes fuente en alta resolución y dejar que el juego las escale.

Recomendación actual:

Imagen fuente recomendada: 1840 x 960 px
Formato: PNG
Ubicación: assets/images/dialogs/

El juego las muestra visualmente como paneles cinemáticos dentro de la intro.

Archivos principales modificados
main.py
settings.py
dialog_sequence.py
README.md
assets/images/dialogs/
Estado

Sistema de diálogos por imágenes completas validado manualmente en la intro del juego.


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