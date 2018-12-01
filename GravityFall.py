# encoding: UTF-8
# Autor: Roberto Emmanuel González Muñoz
# Muestra cómo utilizar pygame en programas que dibujan en la pantalla

from random import randint
import pygame   # Librería de pygame
import sys

# Dimensiones de la pantalla
ANCHO = 600
ALTO = 800

# Colores
BLANCO = (255, 255, 255)  # R,G,B en el rango [0,255], 0 ausencia de color, 255 toda la intensidad
VERDE_BANDERA = (27, 94, 32)    # un poco de rojo, más de verde, un poco de azul
ROJO = (255, 0, 0)      # solo rojo, nada de verde, nada de azul
AZUL = (0, 0, 255)      # nada de rojo, ni verde, solo azul
NEGRO = (0, 0, 0)       # negro

# Estados
MENU = 1
JUGANDO = 2


# Estados de movimiento
QUIETO = 1
IZQUIERDA = 2
DERECHA = 3


def imagen(filename, transparent = False):
    try: image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

# Estructura básica de un programa que usa pygame para dibujar

def dibujarPersonaje(ventana, spritePlanta):
    ventana.blit(spritePlanta.image, spritePlanta.rect)


def dibujarEnemigos(ventana, listaEnemigos):
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)


def actualizarEnemigos(listaEnemigos):
    for enemigos in listaEnemigos:          # Visitar cada enemigo
        enemigos.rect.bottom -= 1


def dibujarBalas(ventana, listaBalas):
    for balas in listaBalas:
        ventana.blit(balas.image, balas.rect)


def actualizarBalas(listaBalas):
    for balas in listaBalas:
        balas.rect.left +=30


def verificarColisiones(listaBalas,listaEnemigos):
    # Recorre las listas al revés
    for k in range(len(listaBalas)-1,-1,-1):
        bala = listaBalas[k]
        borrarBala = False
        for e in range(len(listaEnemigos)-1,-1,-1):
            enemigo = listaEnemigos[e]
            # bala vs enemigo
            xb = bala.rect.left
            yb = bala.rect.bottom
            xe, ye, anchoe, altoe = enemigo.rect
            if xb >= xe and xb <= xe + anchoe and yb >= ye and yb <= ye - altoe:
                listaEnemigos.remove(enemigo)  # borra enemigo
                borrarBala = True
                break

        if borrarBala:
            listaBalas.remove(bala)


def dibujarFondo(ventana, imgFondo):
    ventana.blit(imgFondo, (0, 0))


def dibujar():

    # Inicializa el motor de pygame
    pygame.init()

    # Crea una ventana de ANCHO x ALTO
    ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana donde dibujará
    reloj = pygame.time.Clock()  # Para limitar los fps
    termina = False  # Bandera para saber si termina la ejecución, iniciamos suponiendo que no


    # Imagenes de Fondo
    imgFondo = pygame.image.load("CieloAzul.jpg")
    imgFondoMenu = pygame.image.load("imagenMenu.jpg")
    imgNewSerio = pygame.image.load("NewtonSerio.jpg")
    imgNewLoco = pygame.image.load("NewtonLoco.jpg")
    imgRevelacion = pygame.image.load("NewtonRevelacion.jpg")
    imgManzana = pygame.image.load("manzana.jpg")
    imgNube = pygame.image.load("Nube.png")
    imgMarcador = pygame.image.load("Scoreboard.jpg")

    xFondo = 0
    xNube = 0

    # Tiempo
    time = 0   # Acumulador de tiempo
    score = 0

    # Audio
    pygame.mixer.init()
    efecto = pygame.mixer.Sound("shoot.wav")
    pygame.mixer.music.load("musicaFondo.mp3")
    pygame.mixer.music.play(-1)

    # Texto
    fuente = pygame.font.SysFont("monospace", 54)

    #Personaje principal
    imgPlanta = pygame.image.load("manzana.jpg")
    spritePlanta = pygame.sprite.Sprite()
    spritePlanta.image = imgPlanta
    spritePlanta.rect = imgPlanta.get_rect()
    spritePlanta.rect.left = ANCHO//2 - spritePlanta.rect.width//2
    spritePlanta.rect.bottom = ALTO//4 + spritePlanta.rect.height//2

    movimiento = QUIETO

    # Personaje secundarios(Enemigos)
    listaEnemigos = []      #Lista vacía de enemigos
    #imgZombie = pygame.image.load("Nube.png")
    #spriteZombie = pygame.sprite.Sprite()
    #spriteZombie.image = imgZombie
    #spriteZombie.rect = imgZombie.get_rect()
    #spriteZombie.rect.left = randint(0, ALTO -spriteZombie.rect.width)
    #spriteZombie.rect.bottom = randint(0 + spriteZombie.rect.height//2+270, ALTO)
    #listaEnemigos.append(spriteZombie)


    # Proyectiles
    imgBala = pygame.image.load("Bala.png")
    listaBalas = []

    # Estado del juego
    estado = MENU           #Estado inicial

    # Imágenes para el menú
    imgBtnJugar = pygame.image.load("button_play.png")


    while not termina: # Ciclo principal, MIENTRAS la variable termina sea False, el ciclo se repite automáticamente

        # Procesa los eventos que recibe
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # El usuario hizo click en el botón de salir
                termina = True      # Queremos terminar el ciclo

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    spritePlanta.rect.left -= 5
                    movimiento = IZQUIERDA

                elif evento.key == pygame.K_RIGHT:
                    spritePlanta.rect.right += 5
                    movimiento = DERECHA

                elif evento.key == pygame.K_z:
                    spriteBala = pygame.sprite.Sprite()
                    spriteBala.image = imgBala
                    spriteBala.rect = imgBala.get_rect()
                    spriteBala.rect.left = spritePlanta.rect.width + spritePlanta.rect.left
                    spriteBala.rect.bottom = spritePlanta.rect.bottom - spritePlanta.rect.height//2
                    listaBalas.append(spriteBala)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                xm, ym = pygame.mouse.get_pos()
                xb = ANCHO//2 - 128
                yb = ALTO//2 + 150
                anchoB = 256
                altoB = 100

                if xm >= xb and xm <= xb + anchoB and ym >= yb and ym <= yb + altoB:
                    estado = JUGANDO


        # Pregunta en qué estado está el juego
        if estado == MENU:
            # Borrar pantalla
            ventana.fill(NEGRO)
            pygame.display.set_caption("GRAVITY FALL")
            #ventana.blit(imgFondoMenu, (0, 0))
            ventana.blit(imgNewSerio, (ANCHO // 2-235, ALTO//2-350))
            #ventana.blit(imgNewLoco, (ANCHO // 2-235, ALTO // 2-350))
            ventana.blit(imgBtnJugar, (ANCHO//2 - 128, ALTO//2 + 150))  # Se restan las dimensiones de la imágen.
            titulo = fuente.render("GRAVITY FALL", 1, BLANCO)
            ventana.blit(titulo, (100, 100))

        elif estado == JUGANDO:

            # Actualizar Objetos
            actualizarEnemigos(listaEnemigos)
            actualizarBalas(listaBalas)
            verificarColisiones(listaBalas, listaEnemigos)


            # Mover personaje
            if movimiento == IZQUIERDA:
                if spritePlanta.rect.left >= 0:
                    spritePlanta.rect.left -= 2
            elif movimiento == DERECHA:
                if spritePlanta.rect.right <= ANCHO:
                    spritePlanta.rect.right += 2


            # Borrar pantalla
            ventana.blit(imgFondo, (0, xFondo))
            ventana.blit(imgFondo, (0, xFondo + 600))  # 800 = ancho de la imágen
            xFondo -= 3
            if xFondo <= -600:
                xFondo = 0

            # Nubes
            ventana.blit(imgNube, (200, xNube + 300))
            ventana.blit(imgNube, (0, xNube + 700))
            ventana.blit(imgNube, (200, xNube + 1100))
            xNube -= 2
            if xNube <= -800:
                xNube = 0

            # Dibujar personaje
            #dibujarFondo(ventana, imgFondo)
            dibujarPersonaje(ventana, spritePlanta)
            dibujarEnemigos(ventana, listaEnemigos)
            #dibujarBalas(ventana, listaBalas)

            # Dibujar texto Y marcador
            ventana.blit(imgMarcador, (100,0))
            texto = fuente.render("%d" % time, 1, BLANCO)
            ventana.blit(texto, (265, 15))
            xcore = fuente.render("%d" % score, 2, NEGRO)
            ventana.blit(xcore, (120, 15))



        pygame.display.flip()  # Actualiza trazos (Si no llamas a esta función, no se dibuja)
        reloj.tick(40)  # 40 fps
        time += 1/10
        score += 2/10



    # Después del ciclo principal
    pygame.quit()  # termina pygame


# Función principal, aquí resuelves el problema
def main():
    dibujar()   # Por ahora, solo dibuja


# Llamas a la función principal
main()