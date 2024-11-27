import pygame, random, sys, json
# Constantes
pygame.init()
pygame.mixer.init()
ANCHO = 1000
ALTO = 800
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NOMBRE_FUENTE = pygame.font.SysFont("archivos_extras/VCRosdNEUE.ttf", 35, bold=True)
ARCHIVO_PUNTAJES = "puntajes.json"

# Colores
COLOR_BOTON = (0, 200, 0)
COLOR_TEXTO = (255, 255, 255)

# Variables del juego
# puntos = 0
fin_juego = False
silencio = False  # Bandera de silencio para sonidos

# Cargar y configurar sonidos
sonido_fondo = pygame.mixer.Sound("archivos_extras/ringtones-got-theme.mp3")
sonido_fondo.set_volume(0.2) # Configurar volumen set_volume es la cantidad de sonido que se reproduce, 0.2 es el porcentaje de volumen que se reproduce

# Cargar iconos
icono_sonido_encendido = pygame.image.load('archivos_extras/unmute.png')
icono_sonido_apagado = pygame.image.load('archivos_extras/mute.png')
tamano_icono = 50
posicion_icono = (ANCHO - tamano_icono - 10, 10)  # Esquina superior derecha

# Cargar imagen de fondo
imagen_fondo = pygame.image.load('archivos_extras/fondo_buscaminas.jpeg')
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Fuentes
fuente = pygame.font.Font("archivos_extras/VCRosdNEUE.ttf", 35)  # Tamaño de la fuente de texto (36 pixeles) 

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
icono_pantalla = pygame.image.load("archivos_extras/flag.png")
pygame.display.set_icon(icono_pantalla)
pygame.display.set_caption('BUSCAMINAS')

# Constantes de posición
POSICION_TITULO = (ANCHO / 2, 50) # Centrar el texto en la pantalla, 2 ,50 son las coordenadas
POSICION_PUNTOS = (ANCHO / 2, 250) # Centrar el texto en la pantalla, 2, 250 son las coordenadas
ANCHO_BOTON, ALTO_BOTON = 200, 50 # Tamaño de los botones
INICIO_BOTON_Y = ALTO / 2 - 100 # Posición inicial de los botones
ESPACIADO_BOTON = 70 # Espaciado entre botones

def crear_matriz_en_0(filas:int, columnas:int) -> list:
    """
    Crea una matriz (lista de listas) con las dimensiones especificadas.
    Cada celda se inicializa con 0.
    :param filas: Número de filas de la matriz
    :param columnas: Número de columnas de la matriz
    :return: Matriz de tamaño filas x columnas
    """
    matriz = []  # Inicializar matriz vacía
    for _ in range(filas):
        fila = []  # Crear una nueva fila
        for _ in range(columnas):
            fila.append(0)  # Agregar 0 a la fila
        matriz.append(fila)  # Agregar la fila a la matriz
    return matriz

def crear_matriz_buscamina(filas:int, columnas:int, num_minas:int) -> list:
    """
    Crea una matriz para el juego de Buscaminas con las dimensiones especificadas y coloca un número determinado de minas.

    Las celdas que no contienen minas muestran el número de minas adyacentes.

    :param filas: Número de filas de la matriz.
    :param columnas: Número de columnas de la matriz.
    :param num_minas: Número de minas a colocar en la matriz.
    :return: Matriz de tamaño filas x columnas con minas y números indicando minas adyacentes.
    """
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
            for i in range(fila - 1, fila + 2):
                for j in range(columna - 1, columna + 2):
                    if 0 <= i < filas and 0 <= j < columnas and matriz[i][j] == -1:
                        matriz[fila][columna] += 1
            
    return matriz

# Funciones de dibujo
def dibujar_texto(surf, texto:str, tamano:int, x:int, y:int) -> None: 
    """
        Una función que representa texto en una superficie en una posición y alineación específicas.

        Args:
        surf: La superficie sobre la que representar el texto.
        texto: El texto en el ultimo proceso.
        tamano: El tamaño de fuente del texto..
        x: La posición de la coordenada x.
        y: la posición de la coordenada y.

        Returns:
            None
    """
    fuente = pygame.font.Font("archivos_extras/VCRosdNEUE.ttf", tamano) # Cargar fuente de texto en la superficie en el tamanio indicado 
    superficie_texto = fuente.render(texto, True, BLANCO) # Rerpesenta el texto en la superficie
    rectangulo_texto = superficie_texto.get_rect() # Crea un rectángulo que cubre el texto
    rectangulo_texto.midtop = (x, y) # El rectángulo se centra en la superficie, .midtop representa el punto medio superior del rectángulo 
    surf.blit(superficie_texto, rectangulo_texto) # Rellena el rectángulo con el texto

def dibujar_boton(pantalla, texto:str, x:int, y:int, ancho:int, alto:int, color_inactivo:tuple, color_activo:tuple):
    """
    Dibuja un botón en la pantalla con el texto proporcionado.

    Args:
        texto: El texto que se mostrará en el botón.
        x: La coordenada x del botón.
        y: La coordenada y del botón.
        ancho: El ancho del botón.
        alto: El alto del botón.
        color_inactivo: El color del botón cuando no se encuentra sobre él.
        color_activo: El color del botón cuando se encuentra sobre él.

    Returns:
        El rectángulo del botón.

    """
    raton = pygame.mouse.get_pos()  # Obtener la posición del ratón
    rect_boton = pygame.Rect(x, y, ancho, alto)  # Crear un rectángulo para el botón

    if rect_boton.collidepoint(raton):  # Determinar si el ratón está sobre el botón
        pygame.draw.rect(pantalla, color_activo, rect_boton)  # Botón activo
    else:
        pygame.draw.rect(pantalla, color_inactivo, rect_boton)  # Botón inactivo

    dibujar_texto(pantalla, texto, 30, rect_boton.centerx, rect_boton.centery - 18)

    return rect_boton  # Retornar el rectángulo del botón

#Configuracion de niveles
def seleccionar_nivel() -> tuple:
    """
    Presenta una pantalla para seleccionar el nivel de dificultad y devuelve una tupla con
    el número de filas, columnas y minas que se utilizarán en el juego.

    Returns:
        resultado: Una tupla que determina la dificultad del juego (filas, columnas, num_minas)
    """
    nivel_seleccionado = False
    resultado = None  # Variable auxiliar para almacenar el resultado

    while not nivel_seleccionado:  # Se repite hasta que se seleccione un nivel
        pantalla.blit(imagen_fondo, (0, 0))
        boton_facil = dibujar_boton(pantalla, "Facil", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y - ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        boton_medio = dibujar_boton(pantalla, "Medio", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        boton_dificil = dibujar_boton(pantalla, "Difícil", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clic inicial
                if event.button == 1:
                    if boton_facil.collidepoint(event.pos):
                        resultado = (8, 8, 10)  # Fácil: 8x8 con 10 minas
                        nivel_seleccionado = True        
                    elif boton_medio.collidepoint(event.pos):
                        resultado = (16, 16, 40)  # Medio: 16x16 con 40 minas
                        nivel_seleccionado = True
                    elif boton_dificil.collidepoint(event.pos):
                        resultado = (16, 30, 100)  # Difícil: 16x30 con 100 minas
                        nivel_seleccionado = True
                
        pygame.display.flip()
    
    # Ahora, fuera del bucle, retornamos el valor almacenado en 'resultado'
    return resultado
         
#configuracion de sonido
def alternar_sonido(silencio:bool, sonido_fondo) -> bool:
    """
    Alterna el estado de silencio del sonido de fondo. Si el sonido estaba
    encendido, lo apaga y viceversa.

    Parametros:
        silencio: Estado actual del sonido (True: apagado, False: encendido)
        sonido_fondo: Sonido de fondo

    Return:
        bool: Nuevo estado del sonido (True: apagado, False: encendido)
    """
    nuevo_silencio = not silencio
    if nuevo_silencio:
        sonido_fondo.stop()
    else:
        sonido_fondo.play(-1)  # Reproducir el sonido indefinidamente
    return nuevo_silencio

#Dibujar tablero
def cargar_imagenes():
    """
    Carga las imágenes necesarias para dibujar el tablero. Retorna una tupla con 6 elementos:
        - imagenes_numeros: Un diccionario con los números del 1 al 8 como clave y la imagen correspondiente como valor.
        - imagen_mina: La imagen de una mina sin explotar.
        - imagen_mina_explotada: La imagen de una mina explotada.
        - imagen_bandera_mina: La imagen de una bandera que se coloca en una celda para indicar que contiene una mina.
        - imagen_vacia: La imagen de una celda vacía.

    Returns:
        tupla: (imagenes_numeros, imagen_mina, imagen_mina_explotada, imagen_bandera_mina, imagen_vacia)
    """

    imagenes_numeros = {    
        1: pygame.image.load("archivos_extras/1.png"),
        2: pygame.image.load("archivos_extras/2.png"),
        3: pygame.image.load("archivos_extras/3.png"),
        4: pygame.image.load("archivos_extras/4.png"),
        5: pygame.image.load("archivos_extras/5.png"),
        6: pygame.image.load("archivos_extras/6.png"),
        7: pygame.image.load("archivos_extras/7.png"),
        8: pygame.image.load("archivos_extras/8.png"),
    }
    imagen_mina = pygame.image.load("archivos_extras/unclicked-bomb.png")
    imagen_mina_explotada = pygame.image.load("archivos_extras/bomb-at-clicked-block.png")
    imagen_bandera_mina = pygame.image.load("archivos_extras/flag.png")
    imagen_vacia = pygame.image.load("archivos_extras/empty-block.png")
    return imagenes_numeros, imagen_mina, imagen_mina_explotada, imagen_bandera_mina, imagen_vacia,

def dibujar_celda(pantalla, x:int, y:int, tam_casilla:int, tipo:str, imagenes:list, numero:int=None):
    """
    Dibuja una celda en la pantalla dada en las coordenadas especificadas con un tipo y tamaño específicos.

    Parámetros:
        pantalla: La superficie sobre la cual se dibuja la celda.
        x: La coordenada x de la esquina superior izquierda de la celda.
        y: La coordenada y de la esquina superior izquierda de la celda.
        tam_casilla: El tamaño de la celda.
        tipo: El tipo de celda a dibujar ('mina_explotada', 'mina', 'bandera', 'numero', 'vacia', 'oculta').
        imagenes: Una lista de imágenes usadas para los diferentes tipos de celdas.
        numero: El número a mostrar si el tipo de celda es 'numero'.

    La función escala y dibuja la imagen apropiada en la pantalla según el tipo de celda.
    """
    imagenes_numeros = imagenes[0]
    imagen_mina = imagenes[1]
    imagen_mina_explotada = imagenes[2]
    imagen_bandera_mina = imagenes[3]
    imagen_vacia = imagenes[4]

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
        mina_vacia = pygame.image.load("archivos_extras/0.png")
        mina_vacia = pygame.transform.scale(mina_vacia, (tam_casilla, tam_casilla))
        pantalla.blit(mina_vacia, (x, y))
    elif tipo == "oculta":
        imagen_vacia_redimensionada = pygame.transform.scale(imagen_vacia, (tam_casilla, tam_casilla))
        pantalla.blit(imagen_vacia_redimensionada, (x, y))

def cargar_imagenes_celdas(pantalla, fila:int, columna:int, x:int, y:int, tam_casilla:int, matriz:list, banderas:list, descubiertas:list, imagenes:list) -> None: 
    """
    Carga y dibuja las imágenes correspondientes en la pantalla para una celda específica.

    Parámetros:
        pantalla: La superficie donde se dibujarán las celdas.
        fila: La fila de la celda que se desea cargar.
        columna: La columna de la celda que se desea cargar.
        x: La coordenada x de la esquina superior izquierda de la celda en la pantalla.
        y: La coordenada y de la esquina superior izquierda de la celda en la pantalla.
        tam_casilla: El tamaño de la celda (ancho y alto).
        matriz: La matriz que representa el tablero de juego donde las celdas pueden contener números o minas.
        banderas: Una matriz que indica si hay una bandera en una celda específica.
        descubiertas: Una matriz que indica qué celdas han sido descubiertas (True) o no (False).
        imagenes: Una lista de imágenes que se usarán para representar diferentes tipos de celdas.
    """
    if descubiertas[fila][columna]:
        if matriz[fila][columna] == 0:
            dibujar_celda(pantalla, x, y, tam_casilla, "vacia", imagenes) 
        else:
            dibujar_celda(pantalla, x, y, tam_casilla, "numero", imagenes, matriz[fila][columna])
        if matriz[fila][columna] == -1:  # Mina
            dibujar_celda(pantalla, x, y, tam_casilla, "mina_explotada", imagenes)
    else:
        dibujar_celda(pantalla, x, y, tam_casilla, "oculta", imagenes)
        if banderas[fila][columna]:
            dibujar_celda(pantalla, x, y, tam_casilla, "bandera", imagenes)

def dibujar_tablero(matriz:list, descubiertas:list, banderas:int, pantalla, tam_casilla:int) -> None:
    """
    Dibuja el tablero de juego en la pantalla.

    Esta función itera sobre cada celda del tablero y llama a la función
    `cargar_imagenes_celdas` para determinar la representación visual
    apropiada para cada celda en función de su estado actual.

    Parámetros:
        - matriz: Matriz del juego que contiene los valores de las celdas.
        - descubiertas: Matriz que indica las celdas descubiertas.
        - banderas: Matriz que indica las celdas marcadas con una bandera.
        - pantalla: Superficie sobre la que dibujar.
        - tam_casilla: Tamaño de cada celda en píxeles.
    """
    imagenes = cargar_imagenes()
    filas, columnas = len(matriz), len(matriz[0])
    ancho_tablero = tam_casilla * columnas
    desplazamiento_x = (ANCHO - ancho_tablero) // 2
    for fila in range(filas):
        for columna in range(columnas):
            x = desplazamiento_x + columna * tam_casilla
            y = fila * tam_casilla + 200  # Ajustar para el área de puntaje
            cargar_imagenes_celdas(pantalla, fila, columna, x, y, tam_casilla, matriz, banderas, descubiertas, imagenes)

def crear_matriz_booleana(filas:int, columnas:int, valor_inicial:bool) -> list:
    """
    Crea una matriz (lista de listas) con las dimensiones especificadas.
    Cada celda se inicializa con el valor proporcionado.

    :param filas: Número de filas de la matriz
    :param columnas: Número de columnas de la matriz
    :param valor_inicial: Valor con el que se inicializarán todas las celdas de la matriz
    :return: Matriz de tamaño filas x columnas con el valor inicial especificado
    """
    matriz = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(valor_inicial)
        matriz.append(fila)
    return matriz
                    
def descubrir_vacias(fila:int, columna:int, matriz:list, descubiertas:list, filas:int, columnas:int) ->  None:
    """
    Descubre automáticamente las celdas comenzando desde una celda específica y expandiéndose a sus celdas adyacentes si son vacías.

    Parámetros:
        fila: La coordenada de la fila de la celda desde la cual iniciar el descubrimiento.
        columna: La coordenada de la columna de la celda desde la cual iniciar el descubrimiento.
        matriz: La matriz del tablero de juego donde cada celda puede ser una mina, un número o vacía.
        descubiertas: Una matriz que indica qué celdas han sido descubiertas (True) o no (False).
        filas: El número total de filas en el tablero.
        columnas: El número total de columnas en el tablero.

    La función explora la celda inicial y, si la celda es vacía, continúa descubriendo las celdas adyacentes no descubiertas. El proceso se repite de manera iterativa para cada celda adyacente vacía, hasta que se descubren todas las celdas vacías conectadas a la celda inicial. Si encuentra celdas con minas o números, el proceso se detiene en ellas.
    """

    celdas_por_descubrir = [(fila, columna)]
    while celdas_por_descubrir:
        celda = celdas_por_descubrir.pop()
        f = celda[0]
        c = celda[1] # Eliminar elemento en el indice especificado y lo retorna

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
    
        

def ajustar_tamano_casilla(filas:int, columnas:int) -> int:
    """
    Ajusta el tamaño de las celdas del tablero de juego de acuerdo al tamaño de la pantalla y al número de filas y columnas.

    La función calcula el tamaño óptimo de las celdas asegurando que el tablero encaje en la pantalla con márgenes 
    predefinidos. Se garantiza un tamaño mínimo para las celdas para mantener la jugabilidad.

    :param filas: Número de filas en el tablero.
    :param columnas: Número de columnas en el tablero.
    :return: Tamaño de las celdas en píxeles.
    """
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

def manejar_evento(fila:int, columna:int, filas:int, columnas:int, event, matriz:list, banderas:list, descubiertas:list, puntaje:int, num_minas:int, cantidad_celdas:int, SONIDO_FIN_JUEGO, SONIDO_CELDA_DESCUBIERTA, SONIDO_VICTORIA) -> dict:
    """
    Maneja los eventos del juego, como el clic del jugador en una celda, y actualiza el estado del juego en función de la acción realizada.

    Parámetros:
        fila: La fila de la celda sobre la que se hizo clic.
        columna: La columna de la celda sobre la que se hizo clic.
        filas: El número total de filas en el tablero.
        columnas: El número total de columnas en el tablero.
        event: El evento que se maneja, que incluye información sobre el clic del jugador.
        matriz: La matriz que representa el estado del tablero, donde las minas están representadas por `-1` y los números indican la cantidad de minas adyacentes.
        banderas: Una matriz que indica si una celda tiene una bandera colocada.
        descubiertas: Una matriz que indica si una celda ha sido descubierta o no.
        puntaje: El puntaje actual del jugador, que se incrementa cuando se descubren celdas válidas.
        num_minas: El número total de minas en el tablero.
        cantidad_celdas: El número total de celdas en el tablero.
        SONIDO_FIN_JUEGO: El sonido que se reproduce cuando el jugador pierde.
        SONIDO_CELDA_DESCUBIERTA: El sonido que se reproduce cuando el jugador descubre una celda.
        SONIDO_VICTORIA: El sonido que se reproduce cuando el jugador gana.

    Retorna:
        Un diccionario con el puntaje actualizado y un indicador (`fin_juego`) de si el juego ha terminado.

    La función maneja los clics del jugador en las celdas del tablero. Si el jugador hace clic en una celda con una mina, el juego termina, se revelan todas las minas y se reproduce el sonido de fin de juego. Si el jugador hace clic en una celda vacía, se descubren las celdas adyacentes vacías. Si el jugador ha ganado (es decir, ha descubierto todas las celdas no minadas), se reproduce el sonido de victoria. Finalmente, si el juego ha terminado, se solicita al jugador su nombre y se guarda el puntaje.
    """
    resultado = {
        "puntaje": puntaje,
        "fin_juego": False
    }
    
    if event.button == 1:  # Clic izquierdo
        if not banderas[fila][columna]:  # No se puede descubrir si hay una bandera
            if matriz[fila][columna] == -1:  # Si encuentra una mina
                for i in range(len(matriz)):
                    for j in range(len(matriz[0])): # Se recorre toda la matriz para descubrir todas las celdas que contienen minas
                        if matriz[i][j] == -1:
                            descubiertas[i][j] = True
                SONIDO_FIN_JUEGO.play()
                print("Fin del juego! Se descubrió una mina.")
                resultado["fin_juego"] = True                    
            else:
                if not descubiertas[fila][columna]:
                    SONIDO_CELDA_DESCUBIERTA.play()
                    resultado["puntaje"] += 1
                descubrir_vacias(fila, columna, matriz, descubiertas, filas, columnas)
                if verificar_victoria(matriz, descubiertas, num_minas, cantidad_celdas):
                    SONIDO_VICTORIA.play()
                    resultado["fin_juego"] = True                    
                    
    if resultado["fin_juego"]:
        nick = pedir_nick()
        guardar_puntaje(nick, puntaje)
        pantalla.blit(imagen_fondo, (0, 0))  # Fondo para mostrar la matriz final
        pygame.display.flip()
        
    
    return resultado

def reiniciar(filas:int, columnas:int, num_minas:int):
    """
    Reinicia las variables del juego para empezar una nueva partida con los mismos parámetros.

    :param filas: Número de filas del tablero
    :param columnas: Número de columnas del tablero
    :param num_minas: Número de minas en el tablero
    :return: Tupla con la matriz, el estado de las casillas descubiertas, el estado de las banderas, el puntaje y el contador de segundos
    """
    matriz = crear_matriz_buscamina(filas, columnas, num_minas) # Reiniciar la matriz
    descubiertas = crear_matriz_booleana(filas, columnas, False)  # Reiniciar el estado de las casillas descubiertas
    banderas = crear_matriz_booleana(filas, columnas, False)  # Reiniciar el estado de las banderas
    puntaje = 0
    contador_segundos = 0
    return matriz, descubiertas, banderas, puntaje, contador_segundos

def guardar_puntaje(nick:str, puntaje:int, archivo:str="puntajes.json") -> None:
    """
    Guarda un nuevo puntaje en un archivo JSON.

    Si el archivo ya existe, lee los puntajes existentes y agrega el nuevo puntaje.
    Si el archivo no existe, lo crea y guarda el nuevo puntaje.

    Args:
        nick: El apodo del jugador que ha obtenido el puntaje.
        puntaje: La puntuación obtenida por el jugador.
        archivo: Ruta del archivo JSON donde se guardan los puntajes. Por defecto es "puntajes.json".
    """
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
def pedir_nick() -> str:
    """
    Pide al usuario que ingrese un nick (nombre de usuario) para el juego.

    Muestra una pantalla con un texto que indica que debe ingresar su nick,
    y un rectángulo donde se va a dibujar el texto del nick.

    El usuario puede ingresar caracteres con el teclado, y borrarlos con
    la tecla Backspace. Para confirmar el nick, debe presionar Enter.

    La función devuelve el nick ingresado por el usuario.
    """
    nick = ""
    ingresando = True
    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Permitir salir del juego
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nick) > 0:  # Confirmar con Enter
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar un carácter
                    nick = nick[:-1]
                else:
                    # Agregar el carácter ingresado, si es imprimible
                    if len(evento.unicode) == 1 and evento.unicode.isprintable():
                        nick += evento.unicode

        # Dibujar pantalla de entrada
        pantalla.blit(imagen_fondo, (0, 0))  # Fondo
        texto = fuente.render("Ingresa tu Nick (Enter para confirmar):", True, BLANCO)
        texto_nick = fuente.render(nick, True, BLANCO)

        # Rectángulo de contraste
        rect_x = ANCHO // 2 - texto.get_width() // 2 - 10
        rect_y = ALTO // 3 - 10
        rect_ancho = texto.get_width() + 20
        rect_alto = texto.get_height() + 200
        pygame.draw.rect(pantalla, NEGRO, (rect_x, rect_y, rect_ancho, rect_alto))

        # Dibujar el texto encima del rectángulo
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 3))
        pantalla.blit(texto_nick, (ANCHO // 2 - texto_nick.get_width() // 2, ALTO // 2))
        pygame.display.flip()
    return nick

def swap(lista: list, indice_uno: int, indice_dos: int) -> list:
    """
    Swapea los valores de dos índices de una lista.

    Args:
        lista: Lista que contiene los valores a intercambiar.
        indice_uno: Índice del valor a intercambiar.
        indice_dos: Índice del segundo valor a intercambiar.

    Returns:
        list: Retorna la lista con los valores intercambiados.
    """
    auxiliar = lista[indice_uno]
    lista[indice_uno] = lista[indice_dos]
    lista[indice_dos] = auxiliar
    return lista  

def ordenar(lista: list, clave: str) -> list: 
    """
    Ordena una lista de diccionarios en base a una clave de forma descendente.

    Args:
        lista: Lista de diccionarios a ordenar.
        clave: Clave a usar para ordenar la lista.

    Returns:
        Retorna la lista de diccionarios ordenada.
    """
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if int(lista[i][clave]) < int(lista[j][clave]):
                swap(lista, i, j)
    return lista

def generar_json(nombre:str, lista:list, clave:str) -> None:
    """
    Genera un archivo JSON con la lista proporcionada bajo la clave dada.

    Args:
        nombre: El nombre del archivo JSON a generar.
        lista: La lista de datos a guardar en el archivo JSON.
        clave: La clave bajo la cual se guardará la lista en el archivo JSON.
    """
    data = {clave: lista}
    with open(nombre, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def leer_archivo(archivo_nombre:str) -> dict:
    """
    Lee el contenido de un archivo JSON. Si el archivo no existe, devuelve un diccionario vacío.

    Args:
        archivo_nombre: Ruta del archivo JSON.

    Returns:
        Contenido del archivo JSON como un diccionario. Si no existe, retorna un diccionario vacío.
    """
    try:
        with open(archivo_nombre, 'r') as archivo:
            contenido = json.load(archivo)
    except FileNotFoundError:
        contenido = {}  # Devuelve un diccionario vacío si el archivo no existe

    return contenido
    
def guardar_puntajes(nuevo_puntaje:dict, archivo_puntajes:str) -> None:
    """
    Agrega un nuevo puntaje al archivo JSON.

    Args:
        nuevo_puntaje: Diccionario con las claves "apodo" y "puntos" que representa el puntaje.
        archivo_puntajes: Ruta del archivo JSON donde se guardan los puntajes.
    """
    datos = leer_archivo(archivo_puntajes)
    puntajes = datos.get("puntajes", [])  # Obtiene la lista de puntajes o la inicializa vacía

    puntajes.append(nuevo_puntaje)
    puntajes = ordenar(puntajes, clave='puntos')  # Ordena los puntajes
    generar_json(archivo_puntajes, puntajes, "puntajes")

def cargar_puntajes(archivo_puntajes:str) -> list:
    """
    Carga las puntuaciones más altas desde un archivo JSON.

    Args:
        archivo_puntajes: Ruta del archivo JSON que contiene los puntajes.

    Returns:
        Lista de diccionarios que representan las puntuaciones más altas.
    """
    datos = leer_archivo(archivo_puntajes)
    puntajes = []

    # Validar si el archivo fue leído correctamente
    if datos is None:
        print(f"Advertencia: El archivo '{archivo_puntajes}' no pudo ser leído.")
    else:
        # Validar el tipo de los datos cargados
        if type(datos) == dict:
            puntajes = datos.get("puntajes", [])
        elif type(datos) == list:
            puntajes = datos
        else:
            # Caso de formato inesperado
            print(f"Advertencia: El archivo '{archivo_puntajes}' tiene un formato inesperado.")
    
    # Retornar los puntajes (que puede ser una lista vacía en caso de error)
    return puntajes

def mostrar_ranking(pantalla, archivo_puntajes:str, imagen_fondo, ancho:int, en_menu:bool) -> bool:
    """
    Muestra el ranking de los 5 mejores puntajes en una pantalla, junto con un botón para volver al menú.

    Parámetros:
        pantalla: La superficie sobre la que se dibujarán el ranking y el botón de volver.
        archivo_puntajes: El archivo donde se encuentran los puntajes almacenados, desde el cual se cargan.
        imagen_fondo: La imagen que se usará como fondo en la pantalla de ranking.
        ancho: El ancho de la pantalla para posicionar correctamente los elementos.
        en_menu: Un valor que indica si el jugador está en el menú o en la pantalla de ranking. Se modifica al regresar al menú.

    Retorna:
        El valor actualizado de `en_menu`, que se establece en `True` cuando el jugador presiona el botón de volver.
    """
    en_menu = False
    puntajes = cargar_puntajes(archivo_puntajes)
    puntajes = ordenar(puntajes, clave='puntaje')[:3]  # Top 5 puntajes
    pantalla.blit(imagen_fondo, (0, 0))
    dibujar_texto(pantalla, "TOP 3", 100, ancho / 2, 100)
    desplazamiento_y = 300
    for clave in puntajes:
        dibujar_texto(pantalla, f"{clave['nick']}: {clave['puntaje']}", 36, ancho / 2, desplazamiento_y)
        desplazamiento_y += 50
    pygame.display.flip()
    
    while en_menu == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if boton_volver.collidepoint(event.pos):
                        en_menu = True
        boton_volver = dibujar_boton(pantalla, "Volver", 50, 50, 120, 50, NEGRO, (200, 200, 200))  
        pygame.display.flip()
    return en_menu
   
def verificar_victoria(matriz:list, descubiertas:list, num_minas:int, cantidad_celdas:int) -> bool:
    """
    Verifica si el jugador ha ganado el juego comprobando el número de celdas descubiertas.

    Args:
        matriz: La matriz del tablero de juego donde las minas están representadas por -1.
        descubiertas: Una matriz que indica qué celdas han sido descubiertas.
        num_minas: El número total de minas en el tablero.
        cantidad_celdas: El número total de celdas en el tablero.

    Returns:
        True si el número de celdas descubiertas que no son minas es igual al número total de celdas que no son minas, indicando victoria; False en caso contrario.
    """
    resultado = False
    contador_true = 0
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if matriz[fila][columna] != -1: # Si no es una mina
                if descubiertas[fila][columna] == True: # Si la celda está descubierta
                    contador_true += 1
    if contador_true == cantidad_celdas - num_minas:
        resultado = True
    return resultado


