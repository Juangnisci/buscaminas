import pygame, random, sys, json
# Constantes

pygame.init()
pygame.mixer.init()

ANCHO = 1000
ALTO = 800
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NOMBRE_FUENTE = pygame.font.SysFont("Pixeled.ttf", 20, bold=True)
ARCHIVO_PUNTAJES = "puntajes.json"
reloj = pygame.time.Clock()


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
imagen_fondo = pygame.image.load('fondo_buscaminas.jpeg')
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

def crear_matriz_en_0(filas, columnas):
    """
    Crea una matriz (lista de listas) con las dimensiones especificadas.
    Cada celda se inicializa con 0.

    :param filas: Número de filas de la matriz
    :param columnas: Número de columnas de la matriz
    :return: Matriz de tamaño filas x columnas
    """
    matriz = []  # Inicializar matriz vacía
    for i in range(filas):
        fila = []  # Crear una nueva fila
        for j in range(columnas):
            fila.append(0)  # Agregar 0 a la fila
        matriz.append(fila)  # Agregar la fila a la matriz
    return matriz

def crear_matriz_buscamina(filas, columnas, num_minas):
    matriz = crear_matriz_en_0(filas, columnas)
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
    """
    Modifica la matriz reemplazando las celdas con valor 0 por el número
    de minas (-1) que están en las celdas contiguas.

    :param matriz: La matriz que contiene los valores a modificar
    :return: La matriz modificada
    """
    for i in range(len(matriz)):  # Recorrer las filas de la matriz
        for j in range(len(matriz[0])):  # Recorrer las columnas de la matriz
            if matriz[i][j] == 0:  # Solo modificar las celdas con valor 0
                contiguas = 0  # Inicializar el contador de minas contiguas
                # Recorrer las filas adyacentes (i-1, i, i+1)
                for k in range(i - 1, i + 2):
                    # Asegurarse de que k esté dentro de los límites de la matriz
                    if k >= 0 and k < len(matriz):
                        # Recorrer las columnas adyacentes (j-1, j, j+1)
                        for l in range(j - 1, j + 2):
                            # Asegurarse de que l esté dentro de los límites de la matriz
                            if l >= 0 and l < len(matriz[0]):
                                # Comprobar si hay una mina en la celda (k, l)
                                if matriz[k][l] == -1:
                                    contiguas += 1
                # Si se encontraron minas contiguas, se actualiza la celda
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
    raton = pygame.mouse.get_pos()  # Obtener la posición del ratón
    clic = pygame.mouse.get_pressed()  # Obtener el estado del clic

    rect_boton = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo para el botón

    if rect_boton.collidepoint(raton):  # Determinar si el ratón está sobre el botón
        pygame.draw.rect(pantalla, color_activo, rect_boton)  # Botón activo
        if clic[0] == 1 and accion is not None:  # Si se hace clic y hay acción
            accion
    else:
        pygame.draw.rect(pantalla, color_inactivo, rect_boton)  # Botón inactivo

    dibujar_texto(pantalla, texto, 16, rect_boton.centerx, rect_boton.centery - 18)

    return rect_boton  # Retornar el rectángulo del botón

#Configuracion de niveles
def seleccionar_nivel():
    nivel_seleccionado = False
    resultado = None  # Variable auxiliar para almacenar el resultado

    while not nivel_seleccionado:  # Se repite hasta que se seleccione un nivel
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
                    resultado = (8, 8, 10)  # Fácil: 8x8 con 10 minas
                    nivel = "facil"
                    nivel_seleccionado = True
                elif boton_medio.collidepoint(event.pos):
                    resultado = (16, 16, 40)  # Medio: 16x16 con 40 minas
                    nivel = "medio"
                    nivel_seleccionado = True
                elif boton_dificil.collidepoint(event.pos):
                    resultado = (16, 30, 100)  # Difícil: 16x30 con 100 minas
                    nivel = "dificil"
                    nivel_seleccionado = True

        pygame.display.flip()
    
    # Ahora, fuera del bucle, retornamos el valor almacenado en 'resultado'
    return resultado


    
        
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

def dibujar_tablero(matriz, descubiertas, banderas, pantalla, tam_casilla):
    imagenes = cargar_imagenes()
    filas, columnas = len(matriz), len(matriz[0])
    ancho_tablero = tam_casilla * columnas
    desplazamiento_x = (ANCHO - ancho_tablero) // 2
    for fila in range(filas):
        for columna in range(columnas):
            x = desplazamiento_x + columna * tam_casilla
            # x = columna * tam_casilla + (ANCHO - columna * tam_casilla)//2 
            y = fila * tam_casilla + 200  # Ajustar para el área de puntaje
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

# def ajustar_tamano_casilla(filas, columnas):
#     pantalla_ancho, pantalla_alto = pantalla.get_size()  # Obtener tamaño de la pantalla
#     # Ajustar el tamaño de las celdas para que el tablero entre en la pantalla
#     espacio_ancho = pantalla_ancho - 100  # 100px de margen
#     espacio_alto = pantalla_alto - 200  # 200px de margen (ajusta según sea necesario)

#     tam_casilla_ancho = espacio_ancho // columnas
#     tam_casilla_alto = espacio_alto // filas

#     # Elegir el tamaño mínimo entre ancho y alto para que encaje correctamente
#     tam_casilla = min(tam_casilla_ancho, tam_casilla_alto)

#     # Asegurarse de que el tamaño de la celda no sea demasiado pequeño
#     tam_casilla = max(tam_casilla, 30)

#     return tam_casilla

def ajustar_tamano_casilla(filas, columnas):
    pantalla_ancho, pantalla_alto = pantalla.get_size()  # Obtener tamaño de la pantalla

    # Definir márgenes
    margen_x = 100  # Margen horizontal (izquierda y derecha)
    margen_y = 200  # Margen vertical (arriba y abajo)

    # Calcular espacio disponible para el tablero
    espacio_ancho = pantalla_ancho - margen_x  # Espacio para el tablero a lo largo del eje X
    espacio_alto = pantalla_alto - margen_y    # Espacio para el tablero a lo largo del eje Y

    # Calcular el tamaño máximo de las celdas
    tam_casilla_ancho = espacio_ancho // columnas
    tam_casilla_alto = espacio_alto // filas

    # Elegir el tamaño mínimo entre el tamaño calculado por el ancho y el alto para asegurar que el tablero encaje
    tam_casilla = min(tam_casilla_ancho, tam_casilla_alto)

    # Asegurarse de que el tamaño de la celda no sea demasiado pequeño
    tam_casilla = max(tam_casilla, 30)

    return tam_casilla


"""def iniciar_juego():
    
    Inicia un nuevo juego de Buscaminas.

    Esta función reinicia las variables del juego y llama a la función `juego_principal()`.
    
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
"""

"""def menu_principal():
    
    Muestra el menú principal del juego y permite al jugador seleccionar opciones como iniciar un nuevo juego, ver el marcador o salir del juego.

    Esta función inicializa las variables globales del juego e inicia el bucle del juego. Actualiza continuamente la pantalla con la imagen de fondo del juego y muestra el título del juego. También dibuja botones para iniciar un nuevo juego, ver el marcador y salir del juego. Además, dibuja un ícono para activar o desactivar el sonido del juego.

    Parameters:
    None

    Returns:
    None
    

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
 """                   

def manejar_evento(fila, columna, filas, columnas, event, matriz, banderas, descubiertas, puntaje, SONIDO_FIN_JUEGO, SONIDO_CELDA_DESCUBIERTA):
    """
    Maneja un evento de clic en el juego Buscaminas.
    
    :param fila: Fila del clic.
    :param columna: Columna del clic.
    :param filas: Número total de filas.
    :param columnas: Número total de columnas.
    :param event: Evento de clic recibido.
    :param matriz: Matriz del juego.
    :param banderas: Matriz que indica si hay una bandera en una celda.
    :param descubiertas: Matriz que indica si una celda ya está descubierta.
    :param puntaje: Puntuación actual.
    :param SONIDO_FIN_JUEGO: Sonido que se reproduce al perder.
    :param SONIDO_CELDA_DESCUBIERTA: Sonido que se reproduce al descubrir una celda.
    :return: Actualización del puntaje y estado de fin de juego.
    """
    resultado = {
        "puntaje": puntaje,
        "fin_juego": False
    }
    
    if 0 <= fila < filas and 0 <= columna < columnas:
        if event.button == 1:  # Clic izquierdo
            if not banderas[fila][columna]:  # No se puede descubrir si hay una bandera
                if matriz[fila][columna] == -1:  # Si encuentra una mina
                    # --------------------------------------------
                    for i in range(len(matriz)):
                        for j in range(len(matriz[0])):
                            if matriz[i][j] == -1:
                                descubiertas[i][j] = True
                    SONIDO_FIN_JUEGO.play()
                    # --------------------------------------------
                    print("¡Boom! Has encontrado una mina. Has perdido la partida.")
                    resultado["fin_juego"] = True
                else:
                    if not descubiertas[fila][columna]:
                        SONIDO_CELDA_DESCUBIERTA.play()
                        resultado["puntaje"] += 1
                    descubrir_vacias(fila, columna, matriz, descubiertas, filas, columnas)
    return resultado
                                 
def boton_presionado(nombre_boton, posicion_clic):
    """
    Verifica si el clic ocurrió dentro de las coordenadas de un botón.

    :param nombre_boton: El texto o nombre del botón que se está verificando.
    :param posicion_clic: Tupla (x, y) que indica la posición del clic.
    :return: True si el clic ocurrió dentro del botón, False en caso contrario.
    """
    # Inicializar presionado como False
    presionado = False
    
    # Obtener las coordenadas y dimensiones del botón según su nombre
    if nombre_boton == "Jugar":
        x = ANCHO / 2 - ANCHO_BOTON / 2
        y = INICIO_BOTON_Y
    elif nombre_boton == "Ver Puntajes":
        x = ANCHO / 2 - ANCHO_BOTON / 2
        y = INICIO_BOTON_Y + ESPACIADO_BOTON
    elif nombre_boton == "Salir":
        x = ANCHO / 2 - ANCHO_BOTON / 2
        y = INICIO_BOTON_Y + 2 * ESPACIADO_BOTON
    else:
        return presionado  # Si el botón no existe, regresamos el valor actual de presionado (que es False)

    # Dimensiones del botón
    ancho = ANCHO_BOTON
    alto = ALTO_BOTON

    # Posición del clic
    clic_x, clic_y = posicion_clic

    # Verificar si el clic está dentro del área del botón
    if x <= clic_x <= x + ancho and y <= clic_y <= y + alto:
        presionado = True
    
    # Retornar el valor final de 'presionado'
    return presionado
                    
"""def juego_principal():
    
    Inicia una nueva partida del Buscaminas y maneja el bucle principal del juego.
    
    SONIDO_CELDA_DESCUBIERTA = pygame.mixer.Sound("coin_mario-[AudioTrimmer.com].mp3")
    SONIDO_FIN_JUEGO = pygame.mixer.Sound("game_over.mp3")

    # Seleccionar nivel y configurar variables del juego
    filas, columnas, num_minas = seleccionar_nivel()
    matriz = crear_matriz_buscamina(filas, columnas, num_minas)
    descubiertas = crear_matriz(filas, columnas, False)
    banderas = crear_matriz(filas, columnas, False)
    puntaje = 0
    fin_juego = False
    tam_casilla = ajustar_tamano_casilla(filas, columnas)
    evento_contador = pygame.USEREVENT + 1
    un_segundo = 1000  # Milisegundos
    pygame.time.set_timer(evento_contador, un_segundo)
    contador_segundos = 0
    contador_texto = fuente.render(f"Time: {contador_segundos}", True, "red")

    # Bucle principal del juego
    while not fin_juego:
        pantalla.blit(imagen_fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x, y = pos
                columna = x // tam_casilla
                fila = (y - 100) // tam_casilla

                if 0 <= fila < filas and 0 <= columna < columnas:
                    if event.button == 1:  # Clic izquierdo
                        resultado = manejar_evento(fila, columna, filas, columnas, event, matriz, banderas, descubiertas, puntaje, SONIDO_FIN_JUEGO, SONIDO_CELDA_DESCUBIERTA)
                        puntaje = resultado["puntaje"]
                        fin_juego = resultado["fin_juego"]
                    elif event.button == 3:  # Clic derecho
                        banderas[fila][columna] = not banderas[fila][columna]

            if event.type == evento_contador:
                contador_segundos += 1
                contador_texto = fuente.render(f"Time: {contador_segundos}", True, "red")

        # Dibujar el tablero y los indicadores
        dibujar_tablero(matriz, descubiertas, banderas, pantalla, tam_casilla)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (20, 20))
        pantalla.blit(contador_texto, (700, 20))

        pygame.display.flip()

    # Mensaje de fin de partida
    pygame.time.wait(5000)"""
    
def salir():
    pygame.quit()
    sys.exit()

def reiniciar(filas, columnas, num_minas):
    matriz = crear_matriz_buscamina(filas, columnas, num_minas) # Reiniciar la matriz
    descubiertas = crear_matriz(filas, columnas, False)  # Reiniciar el estado de las casillas descubiertas
    banderas = crear_matriz(filas, columnas, False)  # Reiniciar el estado de las banderas
    puntaje = 0
    return matriz, descubiertas, banderas, puntaje

def guardar_puntaje(nick, puntaje, archivo="puntajes.json"):
    datos = []

    # Verificar si el archivo existe abriéndolo directamente
    archivo_existe = False
    with open(archivo, "a+") as file:
        file.seek(0)  # Mover al inicio del archivo
        contenido = file.read()
        if contenido:  # Si tiene contenido, se considera que existe
            archivo_existe = True

    if archivo_existe:
        # Leer datos existentes
        with open(archivo, "r") as file:
            datos = json.load(file)

    # Agregar el nuevo puntaje
    datos.append({"nick": nick, "puntaje": puntaje})

    # Guardar los datos actualizados en el archivo JSON
    with open(archivo, "w") as file:
        json.dump(datos, file, indent=4)

# Pantalla para pedir el nombre (nick)
def pedir_nick():
    nick = ""
    ingresando = True
    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Permitir salir del juego
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Confirmar con Enter
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar un carácter
                    nick = nick[:-1]
                else:
                    # Agregar el carácter ingresado, si es imprimible
                    if len(evento.unicode) == 1 and evento.unicode.isprintable():
                        nick += evento.unicode

        # Dibujar pantalla de entrada
        pantalla.blit(imagen_fondo, (0, 0))  # Fondo
        texto = fuente.render("Ingresa tu Nick (Enter para confirmar):", True, "white")
        texto_nick = fuente.render(nick, True, "white")

        # Rectángulo de contraste
        rect_x = ANCHO // 2 - texto.get_width() // 2 - 10
        rect_y = ALTO // 3 - 10
        rect_ancho = texto.get_width() + 20
        rect_alto = texto.get_height() + 200
        pygame.draw.rect(pantalla, "black", (rect_x, rect_y, rect_ancho, rect_alto))

        # Dibujar el texto encima del rectángulo
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 3))
        pantalla.blit(texto_nick, (ANCHO // 2 - texto_nick.get_width() // 2, ALTO // 2))

        pygame.display.flip()

    return nick


def swap(lista: list, indice_uno: int, indice_dos: int) -> list:
    """
    Swapea los valores de dos índices de una lista.

    Args:
        lista (list): Lista que contiene los valores a intercambiar.
        indice_uno (int): Índice del valor a intercambiar.
        indice_dos (int): Índice del segundo valor a intercambiar.

    Returns:
        list: Retorna la lista con los valores intercambiados.
    """
    auxiliar = lista[indice_uno]
    lista[indice_uno] = lista[indice_dos]
    lista[indice_dos] = auxiliar

    return lista  


def ordenar(lista: list, clave: str, ascendente: bool = True) -> list: 
    """
    Ordena una lista de diccionarios en base a una clave de forma ascendente o descendente.

    Args:
        lista (list): Lista de diccionarios a ordenar.
        clave (str): Clave a usar para ordenar la lista.
        ascendente (bool, opcional): Declara si la lista se ordena de forma ascendente o descendente. 
                                     Se le asigna False para ordenar de forma descendente. 
                                     (Si no se pasa ningún valor booleano, ordena de forma ascendente por defecto.)

    Returns:
        list: Retorna la lista de diccionarios ordenada.
    """
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if ascendente and int(lista[i][clave]) > int(lista[j][clave]) or not ascendente and int(lista[i][clave]) < int(lista[j][clave]):
                swap(lista, i, j)
    return lista

def generar_json(nombre: str, lista: list, clave: str):
    """
    Genera un archivo JSON con la lista proporcionada bajo la clave dada.

    Args:
        nombre (str): El nombre del archivo JSON a generar.
        lista (list): La lista de datos a guardar en el archivo JSON.
        clave (str): La clave bajo la cual se guardará la lista en el archivo JSON.
    """
    data = {clave: lista}
    with open(nombre, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def leer_archivo(archivo_nombre):
    """
    Lee el contenido de un archivo JSON. Si el archivo no existe, devuelve un diccionario vacío.

    Args:
        archivo_nombre (str): Ruta del archivo JSON.

    Returns:
        dict: Contenido del archivo JSON como un diccionario. Si no existe, retorna un diccionario vacío.
    """
    try:
        with open(archivo_nombre, 'r') as archivo:
            contenido = json.load(archivo)
    except FileNotFoundError:
        contenido = {}  # Devuelve un diccionario vacío si el archivo no existe

    return contenido
    
def guardar_puntajes(nuevo_puntaje, archivo_puntajes):
    """
    Agrega un nuevo puntaje al archivo JSON.

    Args:
        nuevo_puntaje (dict): Diccionario con las claves "apodo" y "puntos" que representa el puntaje.
        archivo_puntajes (str): Ruta del archivo JSON donde se guardan los puntajes.
    """
    datos = leer_archivo(archivo_puntajes)
    puntajes = datos.get("puntajes", [])  # Obtiene la lista de puntajes o la inicializa vacía

    puntajes.append(nuevo_puntaje)
    puntajes = ordenar(puntajes, clave='puntos', ascendente=False)  # Ordena los puntajes

    generar_json(archivo_puntajes, puntajes, "puntajes")

def cargar_puntajes(archivo_puntajes):
    """
    Carga las puntuaciones más altas desde un archivo JSON.

    Args:
        archivo_puntajes (str): Ruta del archivo JSON que contiene los puntajes.

    Returns:
        list: Lista de diccionarios que representan las puntuaciones más altas.
    """
    # Paso 1: Leer el archivo usando leer_archivo
    datos = leer_archivo(archivo_puntajes)
    
    # Paso 2: Validar si el archivo fue leído correctamente
    if datos is None:
        print(f"Advertencia: El archivo '{archivo_puntajes}' no pudo ser leído.")
        return []
    
    # Paso 3: Validar el tipo de los datos cargados
    if isinstance(datos, dict):
        # Si es un diccionario, busca la clave "puntajes"
        return datos.get("puntajes", [])
    elif isinstance(datos, list):
        # Si ya es una lista, retorna directamente
        return datos
    
    # Paso 4: Caso de formato inesperado
    print(f"Advertencia: El archivo '{archivo_puntajes}' tiene un formato inesperado.")
    return []

def mostrar_ranking(pantalla, archivo_puntajes, imagen_fondo, ancho, alto):
    """
    Muestra la clasificación de los 5 mejores puntajes en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie de Pygame donde se dibujará el ranking.
        archivo_puntajes (str): Ruta al archivo JSON que contiene los puntajes.
        imagen_fondo (pygame.Surface): Imagen de fondo para el ranking.
        ancho (int): Ancho de la pantalla.
        alto (int): Alto de la pantalla.

    Returns:
        str: "menu_principal" si el usuario hace clic en el botón "Atrás".
    """
    puntajes = cargar_puntajes(archivo_puntajes)
    puntajes = ordenar(puntajes, clave='puntaje', ascendente=False)[:5]  # Top 5 puntajes

    

    pantalla.blit(imagen_fondo, (0, 0))
    texto_puntajes = fuente.render("TOP 5", True, "white")
    pantalla.blit(texto_puntajes, (ancho // 2 - texto_puntajes.get_width() // 2, 100))
    desplazamiento_y = 150
    for clave in puntajes:
        dibujar_texto(pantalla, f"{clave['nick']}: {clave['puntaje']}", 36, ancho / 2, desplazamiento_y)
        desplazamiento_y += 50

    dibujar_boton("Volver", 50, 50, 120, 50, (50, 50, 255), (100, 100, 255), None)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_raton = pygame.mouse.get_pos()
                if 50 < pos_raton[0] < 170 and 50 < pos_raton[1] < 100:
                    return "menu_principal"

def verificar_victoria(matriz, banderas):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if matriz[fila][columna] == -1:  # Es una mina
                if not banderas[fila][columna]:  # Falta una bandera
                    return False
            elif banderas[fila][columna]:  # Bandera mal colocada
                return False
    return True


