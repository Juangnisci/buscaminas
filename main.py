from biblioteca import *

sonido_fondo.play(loops=-1)
silencio = False
ejecutando = True

# Inicialización general (antes del bucle principal)
SONIDO_CELDA_DESCUBIERTA = pygame.mixer.Sound("coin_mario-[AudioTrimmer.com].mp3")
SONIDO_FIN_JUEGO = pygame.mixer.Sound("game_over.mp3")
evento_contador = pygame.USEREVENT + 1
un_segundo = 1000
pygame.time.set_timer(evento_contador, un_segundo)
# Variables reutilizables
filas = 0
columnas = 0
num_minas = 0
matriz = None
descubiertas = None
banderas = None  
tam_casilla = 0
puntaje = 0
fin_juego = False
contador_segundos = 0
contador_texto = None

while ejecutando:
    # Menú principal
    en_menu = True
    while en_menu:
        pantalla.blit(imagen_fondo, (0, 0))
        dibujar_texto(pantalla, "BUSCAMINAS", 48, POSICION_TITULO[0], POSICION_TITULO[1])

        # Dibujar botones
        dibujar_boton("Jugar", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        dibujar_boton("Ver Puntajes", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        dibujar_boton("Salir", ANCHO / 2 - ANCHO_BOTON / 2, INICIO_BOTON_Y + 2 * ESPACIADO_BOTON, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))

        # Ícono de sonido
        if silencio:
            pantalla.blit(pygame.transform.scale(icono_sonido_apagado, (tamano_icono, tamano_icono)), posicion_icono)
        else:
            pantalla.blit(pygame.transform.scale(icono_sonido_encendido, (tamano_icono, tamano_icono)), posicion_icono)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar ícono de sonido
                if posicion_icono[0] < event.pos[0] < posicion_icono[0] + tamano_icono and posicion_icono[1] < event.pos[1] < posicion_icono[1] + tamano_icono:
                    silencio = alternar_sonido(silencio, sonido_fondo)
                # Botón Jugar
                elif boton_presionado("Jugar", event.pos):
                    en_menu = False  # Salir del menú y entrar al juego
                # Botón Salir
                elif boton_presionado("Salir", event.pos):
                    pygame.quit()
                    sys.exit()

    # Configuración específica del juego (reiniciar solo las variables necesarias)
    filas, columnas, num_minas = seleccionar_nivel()
    matriz = crear_matriz_buscamina(filas, columnas, num_minas)
    descubiertas = crear_matriz(filas, columnas, False)
    banderas = crear_matriz(filas, columnas, False)
    puntaje = 0
    fin_juego = False
    tam_casilla = ajustar_tamano_casilla(filas, columnas)
    contador_segundos = 0
    contador_texto = fuente.render(f"Time: {contador_segundos}", True, "red")
    # -----------------------------------------------------
    ancho_tablero = tam_casilla * columnas
    margen_izquierdo_x = (ANCHO - ancho_tablero) // 2
    #------------------------------------------------------
    # Bucle principal del juego
    while not fin_juego:
        pantalla.blit(imagen_fondo, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x = pos[0]
                y = pos[1]
                columna = x // tam_casilla
                columna = (x - margen_izquierdo_x) // tam_casilla
                fila = (y - 200) // tam_casilla
                if 0 <= fila < filas and 0 <= columna < columnas:
                    if event.button == 1:  # Clic izquierdo
                        resultado = manejar_evento(fila, columna, filas, columnas, event, matriz, banderas, descubiertas, puntaje, SONIDO_FIN_JUEGO, SONIDO_CELDA_DESCUBIERTA)
                        puntaje = resultado["puntaje"]
                        fin_juego = resultado["fin_juego"]
                    elif event.button == 3:  # Clic derecho
                        banderas[fila][columna] = not banderas[fila][columna]
                elif boton_reiniciar.collidepoint(event.pos):
                    matriz, descubiertas, banderas, puntaje = reiniciar(filas, columnas, num_minas)
                if event.type == evento_contador:
                    contador_segundos += 1

                minutos = contador_segundos // 60
                segundos = contador_segundos % 60

                contador_texto = fuente.render(f"Time: {minutos}:{segundos:02d}", True, "red")
            
            
            

        # Dibujar el tablero y los indicadores
        dibujar_tablero(matriz, descubiertas, banderas, pantalla, tam_casilla)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje:04d}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (20, 20))
        pantalla.blit(contador_texto, (700, 20))
        boton_reiniciar = dibujar_boton("Reiniciar", ANCHO / 2 - ANCHO_BOTON / 2, 20, ANCHO_BOTON, ALTO_BOTON, NEGRO, (200, 200, 200))
        
        pygame.display.flip()

    # Fin de juego y volver al menú
    pygame.time.wait(5000)