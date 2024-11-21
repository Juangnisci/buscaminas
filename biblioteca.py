import pygame, random, sys, json
# Constantes

pygame.init()
pygame.mixer.init()

ANCHO = 1000
ALTO = 800
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NOMBRE_FUENTE = pygame.font.SysFont("Pixeled.ttf", 20, bold=True)
ARCHIVO_PUNTAJES = "puntajesbuscamina.json"

# Colores
COLOR_BOTON = (0, 200, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_CASILLA = (200, 200, 200)
COLOR_CASILLA_DESCUBIERTA = (150, 150, 150)
COLOR_BANDERA = (255, 0, 0)

# Variables del juego
puntos = 0
fin_juego = False
silencio = False  # Bandera de silencio para sonidos

# Cargar y configurar sonidos
sonido_fondo = pygame.mixer.Sound("ringtones-got-theme.mp3")
sonido_fondo.set_volume(0.2) # Configurar volumen set_volume es la cantidad de sonido que se reproduce, 0.2 es el porcentaje de volumen que se reproduce


# Cargar iconos
icono_sonido_encendido = pygame.image.load('unmute.png')
icono_sonido_apagado = pygame.image.load('mute.png')
tamano_icono = 50
posicion_icono = (ANCHO - tamano_icono - 10, 10)  # Esquina superior derecha

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('fondo4.jpg')
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Fuentes
fuente = pygame.font.Font("Pixeled.ttf", 20)  # Tamaño de la fuente de texto (36 pixeles) 
fuente_pequena = pygame.font.SysFont(None, 36)

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('BUSCAMINAS')

# Constantes de posición
POSICION_TITULO = (ANCHO / 2, 50) # Centrar el texto en la pantalla, 2 ,50 son las coordenadas
POSICION_PUNTOS = (ANCHO / 2, 250) # Centrar el texto en la pantalla, 2, 250 son las coordenadas
ANCHO_BOTON, ALTO_BOTON = 200, 50 # Tamaño de los botones
INICIO_BOTON_Y = ALTO / 2 - 100 # Posición inicial de los botones
ESPACIADO_BOTON = 70 # Espaciado entre botones

def crear_matriz_buscamina(filas, columnas, num_minas):
    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
    minas_colocadas = 0
    while minas_colocadas < num_minas:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)
        if matriz[fila][columna] != -1:
            matriz[fila][columna] = -1
            minas_colocadas += 1
    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] == -1:
                continue
            for i in range(max(0, fila - 1), min(filas, fila + 2)):
                for j in range(max(0, columna - 1), min(columnas, columna + 2)):
                    if matriz[i][j] == -1:
                        matriz[fila][columna] += 1
    return matriz

def modificar_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                contiguas = 0
                for k in range(max(0, i - 1), min(len(matriz), i + 2)):
                    for l in range(max(0, j - 1), min(len(matriz[0]), j + 2)):
                        if matriz[k][l] == -1:
                            contiguas += 1
                if contiguas > 0:
                    matriz[i][j] = contiguas
    return matriz

# Funciones de dibujo
def dibujar_texto(surf, texto, tamano, x, y, alineacion="center"): 
    """
        Una función que representa texto en una superficie en una posición y alineación específicas.

        Args:
        surf: La superficie sobre la que representar el texto.
        texto: El texto en el ultimo proceso.
        tamano: El tamaño de fuente del texto..
        x: La posición de la coordenada x.
        y: la posición de la coordenada y.
        alineacion: La alineación del texto, por defecto es "centro".

        Returns:
            None
    """
    fuente = pygame.font.Font("Pixeled.ttf", tamano) # Cargar fuente de texto en la superficie en el tamanio indicado 
    superficie_texto = fuente.render(texto, True, BLANCO) # Rerpesenta el texto en la superficie
    rectangulo_texto = superficie_texto.get_rect() # Crea un rectángulo que cubre el texto
    if alineacion == "center": # Si la alineación es "centro" 
        rectangulo_texto.midtop = (x, y) # El rectángulo se centra en la superficie, .midtop representa el punto medio superior del rectángulo 
    elif alineacion == "left": # Si la alineación es "izquierda"
        rectangulo_texto.topleft = (x, y) 
    elif alineacion == "right": # Si la alineación es "derecha"
        rectangulo_texto.topright = (x, y)
    surf.blit(superficie_texto, rectangulo_texto) # Rellena el rectángulo con el texto

def dibujar_boton(texto, x, y, ancho, alto, color_inactivo, color_activo, accion = None):
    """
    Dibuja un botón en la pantalla con el texto y las dimensiones especificadas.

    Parameters:
    - texto: El texto que se mostrará en el botón.
    - x: La coordenada x de la esquina superior izquierda del botón.
    - y: La coordenada y de la esquina superior izquierda del botón.
    - ancho: El ancho del botón.
    - alto: La altura del botón.
    - color_inactivo: El color del botón cuando está inactivo.
    - color_activo: El color del botón cuando está activo.
    - accion: La función que se ejecutará cuando se haga clic en el botón (el valor predeterminado es None).

    Returns:
    - pygame.Rect: El rectángulo que define el área del botón.
    """
    raton = pygame.mouse.get_pos()  # Obtener la posición del ratón
    clic = pygame.mouse.get_pressed()  # Obtener el estado del clic

    rect_boton = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo para el botón

    if rect_boton.collidepoint(raton):  # Determinar si el ratón está sobre el botón
        pygame.draw.rect(pantalla, color_activo, rect_boton)  # Botón activo
        if clic[0] == 1 and accion is not None :  # Si se hace clic y hay acción
            accion()
    else:
        pygame.draw.rect(pantalla, color_inactivo, rect_boton)  # Botón inactivo

    dibujar_texto(pantalla, texto, 16, rect_boton.centerx, rect_boton.centery - 18)

    return rect_boton  # Retornar el rectángulo del botón

#Configuracion de niveles

def seleccionar_nivel():
    while True: 
        pantalla.blit(imagen_fondo, (0, 0))
        boton_facil = dibujar_boton("Facil", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y - ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        boton_medio = dibujar_boton("Medio", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        boton_dificil = dibujar_boton("Difícil", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clic inicial
                if boton_facil.collidepoint(event.pos):
                    return (8, 8, 10)  # Fácil: 8x8 con 10 minas
                elif boton_medio.collidepoint(event.pos):
                    return (16, 16, 40)  # Medio: 16x16 con 40 minas
                elif boton_dificil.collidepoint(event.pos):
                    return (16, 30, 100)  # Difícil: 16x30 con 100 minas

        pygame.display.flip()
  
#configuracion de sonido

def alternar_sonido(silencio, sonido_fondo):
    nuevo_silencio = not silencio
    if nuevo_silencio:
        sonido_fondo.stop()
    else:
        sonido_fondo.play(-1)  # Reproducir el sonido indefinidamente
    return nuevo_silencio

#Dibujar tablero

def cargar_imagenes():
    imagenes_numeros = {
        
        1: pygame.image.load(r"1.png"),
        2: pygame.image.load(r"2.png"),
        3: pygame.image.load(r"3.png"),
        4: pygame.image.load(r"4.png"),
        5: pygame.image.load(r"5.png"),
        6: pygame.image.load(r"6.png"),
        7: pygame.image.load(r"7.png"),
        8: pygame.image.load(r"8.png"),
    }

    #mina_vacia = pygame.image.load(r"0.png")
    imagen_mina = pygame.image.load(r"unclicked-bomb.png")
    imagen_mina_explotada = pygame.image.load(r"bomb-at-clicked-block.png")
    imagen_bandera_mina = pygame.image.load(r"flag.png")
    imagen_vacia = pygame.image.load(r"empty-block.png")
    # -------------------------------------------------------------------------------------------------
    imagen_bandera_erronea = pygame.image.load(r"wrong-flag.png")
    # -------------------------------------------------------------------------------------------------

# AGREGUE EL imagen_bandera_erronea
    return imagenes_numeros, imagen_mina, imagen_mina_explotada, imagen_bandera_mina, imagen_vacia, imagen_bandera_erronea


def dibujar_celda(pantalla, x, y, tam_casilla, tipo, imagenes, numero=None):
    imagenes_numeros, imagen_mina, imagen_mina_explotada, imagen_bandera_mina, imagen_vacia, imagen_bandera_erronea = imagenes

    if tipo == "mina_explotada":
        imagen_mina_explotada = pygame.transform.scale(imagen_mina_explotada, (tam_casilla, tam_casilla))
        pantalla.blit(imagen_mina_explotada, (x, y))
    elif tipo == "mina":
        imagen_mina = pygame.transform.scale(imagen_mina, (tam_casilla, tam_casilla))
        pantalla.blit(imagen_mina, (x, y))
    elif tipo == "bandera":
        imagen_bandera = pygame.transform.scale(imagen_bandera_mina, (tam_casilla, tam_casilla))
        pantalla.blit(imagen_bandera, (x, y))
    elif tipo == "numero" and numero:
        imagen_numero = imagenes_numeros.get(numero)
        if imagen_numero:
            imagen_redimensionada = pygame.transform.scale(imagen_numero, (tam_casilla, tam_casilla))
            pantalla.blit(imagen_redimensionada, (x, y))
    elif tipo == "vacia":
        mina_vacia = pygame.image.load(r"0.png")
        mina_vacia = pygame.transform.scale(mina_vacia, (tam_casilla, tam_casilla))
        pantalla.blit(mina_vacia, (x, y))
    elif tipo == "oculta":
        imagen_vacia_redimensionada = pygame.transform.scale(imagen_vacia, (tam_casilla, tam_casilla))
        pantalla.blit(imagen_vacia_redimensionada, (x, y))

def manejar_celda_juego_normal(pantalla, fila, columna, x, y, tam_casilla, matriz, banderas, descubiertas, imagenes): 
    if descubiertas[fila][columna]:
        if matriz[fila][columna] == 0:
            dibujar_celda(pantalla, x, y, tam_casilla, "vacia", imagenes) 
        else:
            dibujar_celda(pantalla, x, y, tam_casilla, "numero", imagenes, matriz[fila][columna])
# --------- INICIO PRUEBA -------------------------------------------------------------
        if matriz[fila][columna] == -1:  # Mina
            # if banderas[fila][columna]:
            #     dibujar_celda(pantalla, x, y, tam_casilla, "bandera", imagenes)
            # else:
                dibujar_celda(pantalla, x, y, tam_casilla, "mina_explotada", imagenes)
# # --------- FIN PRUEBA -------------------------------------------------------------
    else:
        dibujar_celda(pantalla, x, y, tam_casilla, "oculta", imagenes)
        if banderas[fila][columna]:
            dibujar_celda(pantalla, x, y, tam_casilla, "bandera", imagenes)

def dibujar_tablero(matriz, descubiertas, banderas, pantalla, fuente, tam_casilla):
    imagenes = cargar_imagenes()
    filas, columnas = len(matriz), len(matriz[0])

    for fila in range(filas):
        for columna in range(columnas):
            x = columna * tam_casilla
            y = fila * tam_casilla + 100  # Ajustar para el área de puntaje
            manejar_celda_juego_normal(pantalla, fila, columna, x, y, tam_casilla, matriz, banderas, descubiertas, imagenes)

def crear_matriz(filas, columnas, valor_inicial):
    matriz = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(valor_inicial)
        matriz.append(fila)
    return matriz
                    
def descubrir_vacias(fila, columna, matriz, descubiertas, filas, columnas):
    # Usamos una pila para simular la recursión de inundación.
    celdas_por_descubrir = [(fila, columna)]

    while celdas_por_descubrir:
        f, c = celdas_por_descubrir.pop()

        # Si la celda ya ha sido descubierta, saltarla
        if descubiertas[f][c]:
            continue

        # Marcar la celda como descubierta
        descubiertas[f][c] = True

        # Si la celda es vacía, agregar todas sus celdas adyacentes no descubiertas
        if matriz[f][c] == 0:
            for i in range(f - 1, f + 2):  # Verifica las filas adyacentes
                for j in range(c - 1, c + 2):  # Verifica las columnas adyacentes
                    if 0 <= i < filas and 0 <= j < columnas and not descubiertas[i][j]:
                        celdas_por_descubrir.append((i, j))


def ajustar_tamano_casilla(filas, columnas):
    pantalla_ancho, pantalla_alto = pantalla.get_size()  # Obtener tamaño de la pantalla
    # Ajustar el tamaño de las celdas para que el tablero entre en la pantalla
    espacio_ancho = pantalla_ancho - 100  # 100px de margen
    espacio_alto = pantalla_alto - 200  # 200px de margen (ajusta según sea necesario)

    tam_casilla_ancho = espacio_ancho // columnas
    tam_casilla_alto = espacio_alto // filas

    # Elegir el tamaño mínimo entre ancho y alto para que encaje correctamente
    tam_casilla = min(tam_casilla_ancho, tam_casilla_alto)

    # Asegurarse de que el tamaño de la celda no sea demasiado pequeño
    tam_casilla = max(tam_casilla, 30)

    return tam_casilla

def iniciar_juego():
    """
    Inicia un nuevo juego de Buscaminas.

    Esta función reinicia las variables del juego y llama a la función `juego_principal()`.
    """
    # Crear un diccionario para almacenar las variables del estado del juego
    estado_juego = {
        'matriz': [],
        'descubiertas': [],
        'banderas': [],
        'puntaje': 0
    }

    # Reiniciar variables del juego
    filas = seleccionar_nivel()[0]
    columnas = seleccionar_nivel()[1]
    num_minas = seleccionar_nivel()[2]
    
    estado_juego['matriz'] = crear_matriz_buscamina(filas, columnas, num_minas)  # Generar una nueva matriz con minas distribuidas aleatoriamente
    estado_juego['descubiertas'] = crear_matriz(filas, columnas, False)  # Reiniciar el estado de las casillas descubiertas
    estado_juego['banderas'] = crear_matriz(filas, columnas, False)  # Reiniciar el estado de las banderas
    estado_juego['puntaje'] = 0  # Reiniciar el puntaje a 0000

    juego_principal()  # Llamar a la función que maneja el bucle principal del juego

    # Si necesitas acceder a las variables actualizadas después de llamar a juego_principal, puedes retornarlas
    return estado_juego


def menu_principal():
    """
    Muestra el menú principal del juego y permite al jugador seleccionar opciones como iniciar un nuevo juego, ver el marcador o salir del juego.

    Esta función inicializa las variables globales del juego e inicia el bucle del juego. Actualiza continuamente la pantalla con la imagen de fondo del juego y muestra el título del juego. También dibuja botones para iniciar un nuevo juego, ver el marcador y salir del juego. Además, dibuja un ícono para activar o desactivar el sonido del juego.

    Parameters:
    None

    Returns:
    None
    """

    # Reproducir música de fondo
    sonido_fondo.play(loops=-1)

    ejecutando = True
    silencio = False
    while ejecutando:  # Bucle principal del juego 
        pantalla.blit(imagen_fondo, (0, 0))  # Dibujar imagen de fondo
        dibujar_texto(pantalla, "BUSCAMINAS", 48, POSICION_TITULO[0], POSICION_TITULO[1])

        # Dibujar botones

        dibujar_boton("Jugar", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200), iniciar_juego)
        dibujar_boton("Ver Puntajes", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        dibujar_boton("Salir", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + 2 * ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200), salir)

        # Dibujar ícono de sonido
        if silencio:  # Si el sonido esta silenciado, mostrar el ícono de sonido apagado
            pantalla.blit(pygame.transform.scale(icono_sonido_apagado, (tamano_icono, tamano_icono)), posicion_icono)
        else:  # Si el sonido no esta silenciado, mostrar el ícono de sonido encendido
            pantalla.blit(pygame.transform.scale(icono_sonido_encendido, (tamano_icono, tamano_icono)), posicion_icono)
            

        pygame.display.flip()

        for event in pygame.event.get(): # Manejo de eventos del juego (Click, teclado, etc.)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Salir del programa cuando se cierra la ventana
            elif event.type == pygame.MOUSEBUTTONDOWN: # Manejo de eventos de click del ratón (Click, teclado, etc.)
                if posicion_icono[0] < event.pos[0] < posicion_icono[0] + tamano_icono and posicion_icono[1] < event.pos[1] < posicion_icono[1] + tamano_icono: # Verificar si el click se encuentra dentro del ícono de sonido (activado o desactivado) y cambiar el estado del silencio a su opuesto 
                    silencio = alternar_sonido(silencio, sonido_fondo)  # Alternar sonido cuando se hace clic en el ícono de sonido
                    
    
                                 
                    
def juego_principal():
    SONIDO_CELDA_DESCUBIERTA = pygame.mixer.Sound("coin_mario-[AudioTrimmer.com].mp3")
    SONIDO_FIN_JUEGO = pygame.mixer.Sound("game_over.mp3")
    """Inicia una nueva partida del Buscaminas."""
    filas = seleccionar_nivel()[0]
    columnas = seleccionar_nivel()[1]
    num_minas = seleccionar_nivel()[2]

    # Inicializar el estado del juego
    matriz = crear_matriz_buscamina(filas, columnas, num_minas)
    descubiertas = crear_matriz(filas, columnas, False)
    banderas = crear_matriz(filas, columnas, False) 
    puntaje = 0
    fin_juego = False
    tam_casilla = ajustar_tamano_casilla(filas, columnas)
    evento_contador = pygame.USEREVENT + 1 
    un_segundo = 1000 # 1000 milisegundos = 1 segundo
    pygame.time.set_timer(evento_contador, un_segundo)
    contador_segundos = 0
    contador_texto = fuente.render(f"Time: {contador_segundos}", True, "red")

    while not fin_juego:  # Bucle de la partida
        pantalla.blit(imagen_fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                columna = x // tam_casilla
                fila = (y - 100) // tam_casilla

                if 0 <= fila < filas and 0 <= columna < columnas:
                    if event.button == 1:  # Clic izquierdo
                        if not banderas[fila][columna]:  # No se puede descubrir si hay una bandera
                            if matriz[fila][columna] == -1:  # Si encuentra una mina
                                #--------------------------------------------
                                for i in range(len(matriz)):
                                    for j in range(len(matriz[0])):
                                        if matriz[i][j] == -1:
                                            descubiertas[i][j] = True
                                SONIDO_FIN_JUEGO.play()
                                #--------------------------------------------                          
                                print("¡Boom! Has encontrado una mina. Has perdido la partida.")
                                fin_juego = True
                            else:
                                if descubiertas[fila][columna] == False:
                                    SONIDO_CELDA_DESCUBIERTA.play()
                                    puntaje += 1
                                descubrir_vacias(fila, columna, matriz, descubiertas, filas, columnas)
                                
                    elif event.button == 3:  # Clic derecho
                        banderas[fila][columna] = not banderas[fila][columna]
            if event.type == evento_contador:
                contador_segundos += 1
                contador_texto = fuente.render(f"Time: {contador_segundos}", True, "red")
                    
        # Dibujar el tablero con imágenes y números
        dibujar_tablero(matriz, descubiertas, banderas, pantalla, fuente, tam_casilla)

        # Mostrar el puntaje
        texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (20, 20))
        pantalla.blit(contador_texto, (700, 20))

        pygame.display.flip()

    # Mostrar mensaje de fin de partida antes de regresar al menú
    pygame.time.wait(5000)
    
def salir():
    pygame.quit()
    sys.exit()
