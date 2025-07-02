import pygame
import random

# --- 1. Inicialización de Pygame ---
pygame.init()

# --- 2. Configuración de la Ventana del Juego ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Atrapa la Moneda")

# --- 3. Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Aquí puedes añadir tus nuevos colores, si los definiste antes.
# Por ejemplo:
# VERDE_OSCURO = (0, 100, 0)
# MORADO_BRILLANTE = (200, 0, 255)

# --- Cargar Imágenes (si las tienes) ---
imagen_moneda = None # Variable para la imagen, iniciada en None
try:
    imagen_moneda = pygame.image.load('moneda.png').convert_alpha()
    # tamano_moneda DEBE estar definido antes de usarlo aquí
    tamano_moneda_temp = 20 # Define un tamaño temporal o asegúrate de que tamano_moneda esté definido antes
    imagen_moneda = pygame.transform.scale(imagen_moneda, (tamano_moneda_temp, tamano_moneda_temp))
except pygame.error as e:
    print(f"Error cargando imagen: {e}")
    print("Asegúrate de que 'moneda.png' está en la misma carpeta que 'juego.py'")


# --- Cargar Sonidos (si los tienes) ---
sonido_moneda = None # Variable para el sonido, iniciada en None
try:
    sonido_moneda = pygame.mixer.Sound('moneda_recogida.mp3')
except pygame.error as e:
    print(f"Error cargando sonido: {e}")
    print("Asegúrate de que 'moneda_recogida.wav' está en la misma carpeta que 'juego.py'")


# --- Fuente de la puntuación (siempre la necesitamos) ---
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72) # Para mensajes más grandes


# --- DEFINE LA FUNCIÓN PRINCIPAL DEL JUEGO AQUÍ ---
def jugar_partida():
    # --- 4. Configuración del Jugador ---
    tamano_jugador = 50
    x_jugador = ANCHO_PANTALLA // 2 - tamano_jugador // 2
    y_jugador = ALTO_PANTALLA - tamano_jugador - 10
    velocidad_jugador = 5

    # --- 5. Configuración de las Monedas ---
    monedas = []
    cantidad_monedas = 5 # <--- Aquí puedes cambiar a 10 o 20
    tamano_moneda = 20 # <--- Aquí puedes cambiar el tamaño
    velocidad_moneda = 3 # <--- Aquí puedes cambiar la velocidad

    # --- 6. Puntuación y Tiempo ---
    puntuacion = 0
    tiempo_limite = 30 # Segundos de juego (cambia si quieres)
    tiempo_inicio = pygame.time.get_ticks()

    # --- Función para crear una nueva moneda (DENTRO de jugar_partida) ---
    # Nota: Esta función debe ir después de que tamano_moneda esté definida
    def crear_moneda():
        x = random.randint(0, ANCHO_PANTALLA - tamano_moneda)
        y = random.randint(-ALTO_PANTALLA, -tamano_moneda)
        return pygame.Rect(x, y, tamano_moneda, tamano_moneda)

    # --- Crear las primeras monedas ---
    for _ in range(cantidad_monedas):
        monedas.append(crear_moneda())

    # --- 7. Bucle Principal del Juego (¡El corazón del juego!) ---
    juego_activo = True
    reloj = pygame.time.Clock()

    while juego_activo:
        # --- A. Eventos (¿Qué hizo el jugador?) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir" # Si el jugador cierra la ventana, indicamos que quiere salir
        # ... (el resto del código del juego principal, hasta antes del pygame.quit())
        # --- B. Movimiento del Jugador ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            x_jugador -= velocidad_jugador
        if teclas[pygame.K_RIGHT]:
            x_jugador += velocidad_jugador

        # Asegurarse de que el jugador no salga de la pantalla
        if x_jugador < 0:
            x_jugador = 0
        if x_jugador > ANCHO_PANTALLA - tamano_jugador:
            x_jugador = ANCHO_PANTALLA - tamano_jugador

        # --- C. Movimiento de las Monedas y Colisiones ---
        for i, moneda in enumerate(monedas):
            moneda.y += velocidad_moneda

            # Si la moneda sale por abajo de la pantalla, la creamos de nuevo y restamos punto
            if moneda.y > ALTO_PANTALLA:
                monedas[i] = crear_moneda()
                puntuacion -= 1
                if puntuacion < 0:
                    puntuacion = 0

            # Si el jugador y la moneda se tocan (colisión)
            jugador_rect = pygame.Rect(x_jugador, y_jugador, tamano_jugador, tamano_jugador)
            if jugador_rect.colliderect(moneda):
                puntuacion += 1
                monedas[i] = crear_moneda()
                if sonido_moneda: # Si el sonido se cargó correctamente
                    sonido_moneda.play() # ¡Reproduce el sonido!

        # --- D. Dibujar en la Pantalla ---
        PANTALLA.fill(NEGRO) # <--- Aquí puedes cambiar el fondo a VERDE_OSCURO o el que quieras

        # Dibujar al jugador (un rectángulo azul)
        pygame.draw.rect(PANTALLA, AZUL, (x_jugador, y_jugador, tamano_jugador, tamano_jugador))

        # Dibujar las monedas (círculos amarillos o imágenes)
        for moneda in monedas:
            if imagen_moneda: # Si la imagen se cargó correctamente
                PANTALLA.blit(imagen_moneda, moneda)
            else: # Si hubo un error cargando la imagen, dibuja un círculo como respaldo
                pygame.draw.circle(PANTALLA, AMARILLO, moneda.center, tamano_moneda // 2) # <--- Aquí puedes cambiar el color a MORADO_BRILLANTE

        # Calcular el tiempo restante
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio) // 1000
        tiempo_restante = tiempo_limite - tiempo_transcurrido

        # Si el tiempo se acabó, termina el juego
        if tiempo_restante <= 0:
            tiempo_restante = 0
            juego_activo = False

        # Dibujar la puntuación y el tiempo
        texto_puntuacion = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        PANTALLA.blit(texto_puntuacion, (10, 10))

        texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}", True, BLANCO)
        PANTALLA.blit(texto_tiempo, (ANCHO_PANTALLA - texto_tiempo.get_width() - 10, 10))

        # --- E. Actualizar la Pantalla ---
        pygame.display.flip()

        # --- F. Controlar la Velocidad del Juego ---
        reloj.tick(60)

    # --- Fuera del bucle de juego activo: Muestra el mensaje final y pregunta ---
    PANTALLA.fill(NEGRO)
    mensaje_final_puntos = fuente_grande.render(f"¡Juego Terminado! Puntos: {puntuacion}", True, BLANCO)
    rect_mensaje_puntos = mensaje_final_puntos.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50))
    PANTALLA.blit(mensaje_final_puntos, rect_mensaje_puntos)

    mensaje_opciones = fuente.render("Presiona 'R' para Jugar de Nuevo o 'Q' para Salir", True, BLANCO)
    rect_opciones = mensaje_opciones.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 50))
    PANTALLA.blit(mensaje_opciones, rect_opciones)
    pygame.display.flip()

    # Bucle para esperar la decisión del jugador
    esperando_decision = True
    while esperando_decision:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando_decision = False
                return "salir" # El jugador cierra la ventana
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r: # Si presiona 'R'
                    esperando_decision = False
                    return "jugar_de_nuevo" # Indicamos que quiere jugar de nuevo
                if evento.key == pygame.K_q: # Si presiona 'Q'
                    esperando_decision = False
                    return "salir" # Indicamos que quiere salir

    return "salir" # Por si acaso, si sale del bucle sin una decisión clara

    # --- Bucle principal de la aplicación ---
# Este bucle controla si se juega una partida nueva o se sale del juego
while True:
    resultado = jugar_partida() # Llama a la función que contiene todo el juego
    if resultado == "salir":
        break # Si la partida dice que hay que salir, rompe este bucle y termina el programa

pygame.quit() # Cierra Pygame cuando el bucle principal de la aplicación termina