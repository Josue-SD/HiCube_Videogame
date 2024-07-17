import pygame
import sys
import random
import math
pygame.init()


#Icono y título del videojuego
pygame.display.set_caption("Hicube")
icono = pygame.image.load("Imagenes/Icono.png")
pygame.display.set_icon(icono)

radio_aura = 7
superficie_aura = pygame.Surface((2 * radio_aura, 2 * radio_aura), pygame.SRCALPHA)
pygame.draw.circle(superficie_aura, (255,242,0, 90), (radio_aura, radio_aura), radio_aura)

#Paleta de colores
BLACK = (0,0,0)
RED = (100,0,0)
BLUE = (0,0,100)
GREY = (227,227,227)
WHITE = (255,255,255)
BROWN = (64,16,16)
GREEN = (38, 190, 78)
GREEN_ZONA_SEGURA = (167, 254, 179)
SKYBLUE = (65,148,178)
YELLOW = (230, 217, 16)
YELLOW2 = (236, 187, 0)

#Tamaño ventana
tamaño = (900, 600)

#Crear ventana
screen = pygame.display.set_mode(tamaño)

#Definir reloj (Para controlar los FPS del juego)
clock = pygame.time.Clock()

#Coordenadas
coord_x = 0
coord_y = 0
coord_x2 = 880
coord_y2 = 580
x_coord = 10
y_coord = 10
x1_coord = 10
y1_coord = 30

#Velocidad de animacion
speed_x = 3
speed_y = 3
speed_x2 = 3
speed_y2 = 3
x_speed = 0
y_speed = 0
x1_speed = 0
y1_speed = 0


lista_coord_lluvia = []
for i in range (60):
        x = random.randint(0, 900)
        y = random.randint(0, 600)
        lista_coord_lluvia.append([x,y])

#Hacer visible/invisible el mouse
pygame.mouse.set_visible(0)

angulo_estrella = 0  # Inicializar el ángulo de rotación
medida_base_estrella = 17

def dibujar_octagono(eje_x, eje_y, tamaño):
    angulo = 360 / 8
    vertices_octagono = []
    for i in range(8):
        x = eje_x + tamaño * pygame.math.Vector2(1, 0).rotate(angulo * i)[0]
        y = eje_y + tamaño * pygame.math.Vector2(1, 0).rotate(angulo * i)[1]
        vertices_octagono.append((x, y))
    return vertices_octagono

def dibujar_estrella(screen, x, y, size, angulo_estrella):
    points = []
    for i in range(5):
        angulo_de_rotacion = i * 2 * math.pi / 5 + angulo_estrella
        x_coord_estrella = x + size * math.cos(angulo_de_rotacion)
        y_coord_estrella = y + size * math.sin(angulo_de_rotacion)
        points.append((x_coord_estrella, y_coord_estrella))

        angulo_de_rotacion = i * 2 * math.pi / 5 + angulo_estrella + math.pi / 5
        x_coord_estrella = x + size * 0.5 * math.cos(angulo_de_rotacion)
        y_coord_estrella = y + size * 0.5 * math.sin(angulo_de_rotacion)
        points.append((x_coord_estrella, y_coord_estrella))

    pygame.draw.polygon(screen, YELLOW2, points)

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()
    
        #Eventos teclado player 1
        if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                        x_speed = -3
                if event.key == pygame.K_RIGHT:
                        x_speed = 3
                if event.key == pygame.K_UP:
                        y_speed = -3
                if event.key == pygame.K_DOWN:
                        y_speed = 3
        if event.type  == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                        x_speed = 0
                if event.key == pygame.K_RIGHT:
                        x_speed = 0
                if event.key == pygame.K_UP:
                        y_speed = 0
                if event.key == pygame.K_DOWN:
                        y_speed = 0
                        
        #Eventos teclado player 2
        if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                        x1_speed = -3
                if event.key == pygame.K_d:
                        x1_speed = 3
                if event.key == pygame.K_w:
                        y1_speed = -3
                if event.key == pygame.K_s:
                        y1_speed = 3
        if event.type  == pygame.KEYUP:
                if event.key == pygame.K_a:
                        x1_speed = 0
                if event.key == pygame.K_d:
                        x1_speed = 0
                if event.key == pygame.K_w:
                        y1_speed = 0
                if event.key == pygame.K_s:
                        y1_speed = 0
        
        

    #Lógica del juego
    #Hacer que permanezca siempre en pantalla dentro de los limites
    if(coord_x>880 or coord_x<0):
        speed_x *= -1
    if(coord_y>580 or coord_y<0):
        speed_y *= -1
    if(coord_x2>880 or coord_x2<0):
        speed_x2 *= -1
    if(coord_y2>580 or coord_y2<0):
        speed_y2 *= -1
    if(x_coord>880 or x_coord<0):
        x_speed *= -1
    if(y_coord>580 or y_coord<0):
        y_speed *= -1
    if(x1_coord>880 or x1_coord<0):
        x1_speed *= -1
    if(y1_coord>580 or y1_coord<0):
        y1_speed *= -1
        
    #Inicio de la animación
    coord_x += speed_x
    coord_y += speed_y
    coord_x2 += speed_x2
    coord_y2 += speed_y2
    x_coord += x_speed
    y_coord += y_speed
    x1_coord += x1_speed
    y1_coord += y1_speed

    angulo_estrella += 0.03
    multiplicador_de_medida_estrella = 0.6 + 0.5 * math.sin(angulo_estrella)
    
    
    #Color de fondo
    screen.fill(SKYBLUE)

    #Objeto a mover con mouse
    #pygame.draw.rect (screen, RED, (x1, y1, 10, 10))

    #Objeto a mover con teclado
    
    jugador1 = pygame.draw.rect (screen, RED, (x1_coord, y1_coord, 10, 10))
    jugador2 = pygame.draw.rect (screen, BLUE, (x_coord, y_coord, 10, 10))
    #Zona de dibujo
    pygame.draw.rect(screen, BLACK, (coord_x, coord_y, 30, 30))
    pygame.draw.rect(screen, BLACK, (coord_x2, coord_y2, 30, 30))

    zonas_negras = []

    for x in range(0, 920, 50):
        plataforma = pygame.draw.rect(screen, BLACK, (x,300,50,50))
        zonas_negras.append(plataforma)
        linea = pygame.draw.line(screen, BLACK, (x, 0), (x,900), 15)
        zonas_negras.append(linea)

    #LLUVIA
    for j in lista_coord_lluvia:
        pygame.draw.circle(screen, BLACK, j, 2)
        j[1] += 1
        if j[1] > 600:
            j[1] = 0

    # Dentro del bucle principal
            
    for limite in zonas_negras:
            if jugador1.colliderect(limite):
                screen.blit(superficie_aura, (x1_coord - 2, y1_coord - 2))
    for limite in zonas_negras:
            if jugador2.colliderect(limite):
                screen.blit(superficie_aura, (x_coord - 2, y_coord - 2))
    
    vertices_octagono = dibujar_octagono(450, 300, 30)
    pygame.draw.polygon(screen, BLACK, vertices_octagono, width=3)
    vertices_octagono = dibujar_octagono(450, 300, 29)
    pygame.draw.polygon(screen, YELLOW, vertices_octagono)

    dibujar_estrella(screen, 450, 300, int(medida_base_estrella * multiplicador_de_medida_estrella), angulo_estrella)


       
        
    #Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)



