import pygame, sys, random, math, threading
import time

#Iniciando 
pygame.init()

#Crear ventana
size = (900, 600)
screen = pygame.display.set_mode(size)
fuente = pygame.font.SysFont("cambria", 25)
fuenteTimer = pygame.font.SysFont("cambria", 20)

#Icono y título del videojuego
pygame.display.set_caption("Hicube")

class Game:

    def __init__(self):
        
         # Definir el tiempo inicial (3 minutos en segundos)
        self.initial_time = 120
        self.timer = self.initial_time
        self.start_time = time.time() 

        # Inicialización de variables, ventanas, sonidos, etc.
        self.icono = pygame.image.load("Imagenes/Icono.png")
        pygame.display.set_icon(self.icono)

        #Tipo de letra
        self.fuente = pygame.font.SysFont("cambria", 20)

        self.ultimo_checkpoint_jugador1 = 0
        self.ultimo_checkpoint_jugador2 = 0
        #Paleta de colores
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (100,0,0)
        self.BLUE = (0,0,100)
        self.GREY = (31,31,31)
        self.GREEN = (38, 190, 78)
        self.GREEN_2 = (154, 215, 149)
        self.YELLOW = (253, 236, 166)

        #Definicion de sonidos
        self.sonido_muerte = pygame.mixer.Sound("audios/error-126627.mp3")
        self.sonido_ganar = pygame.mixer.Sound("audios/success-1-6297.mp3")
        self.sonido_ganar.set_volume(0.2)
        self.musica_fondo = pygame.mixer.Sound("audios/SHAKE.mp3")

        #Definir fondo de pantalla
        self.fondo_menu_princial = pygame.image.load("Imagenes/MenuPrincipal.png")
        self.fondo_pantalla_carga = pygame.image.load("Imagenes/pantallaCarga.png")
        self.fondo_tutorial0 = pygame.image.load("Imagenes/Tutorial0.png")
        self.fondo_tutorial1 = pygame.image.load("Imagenes/Tutorial1.png")
        self.fondo_tutorial2 = pygame.image.load("Imagenes/Tutorial2.png")
        self.fondo_tutorial3 = pygame.image.load("Imagenes/Tutorial3.png")
        self.fondo_tutorial4 = pygame.image.load("Imagenes/Tutorial4.png")
        self.fondo_tutorial5 = pygame.image.load("Imagenes/Tutorial5.png")
        self.fondo_tutorial7 = pygame.image.load("Imagenes/Tutorial7.png")

        # Definir Barras de carga 
        self.barra_carga_fondo = pygame.image.load("Imagenes/barraCargaFondo.png")
        self.fondo_barra_carga = self.barra_carga_fondo.get_rect(center=(450, 400))

        self.barra_carga = pygame.image.load("Imagenes/barraCarga.png")
        self.rectangulo_barra_carga = self.barra_carga.get_rect(midleft=(200, 360))
        self.barra_carga_terminada = False
        self.cargar_progreso = 0
        self.extension_barra_carga = 10

        self.TRABAJO = 10500000
         

        #Tamaño ventana
        self.size = (900, 600)

        #Crear ventana
        self.screen = pygame.display.set_mode(self.size)

        #Definir reloj (Para controlar los FPS del juego)
        self.clock = pygame.time.Clock()

        #Definir imagen de fondo
        self.fondo = pygame.image.load("Imagenes/MenuPrincipal.png")
        #Definir botones
        self.imagen_boton = pygame.image.load("Imagenes/Boton_Jugar.png")
        self.imagen_boton = pygame.transform.scale(self.imagen_boton, (250, 60))

        #Coordenadas zonas obscuras
        self.coord_x = 100
        self.coord_y = 280
        self.coord_x2 = 200
        self.coord_y2 = 540
        self.coord_x4 = 800
        self.coord_y4 = 275
        self.coord_x5 = 800
        self.coord_y5 = 150
        self.coord_x6 = 800
        self.coord_y6 = 50
        self.coord_x7 = 500
        self.coord_y7 = 50
        self.coord_x8 = 500
        self.coord_y8 = 275

        #Velocidad de animacion
        self.speed_x = 3
        self.speed_y = 3
        self.speed_x2 = 3
        self.speed_y2 = 3
        self.speed_x4 = 3
        self.speed_y4 = 3
        self.speed_x5 = 3
        self.speed_y5 = 3
        self.speed_x6 = 3
        self.speed_y6 = 3
        self.speed_x7 = 3
        self.speed_y7 = 3
        self.speed_x8 = 3
        self.speed_y8 = 3

        #Jugador 1 y 2
        self.x_coord = 220
        self.y_coord = 285
        self.x1_coord = 220
        self.y1_coord = 300

        #Velocidad jugador 1 y 2
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0

    def eventos_teclado2(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Manejar otros eventos, como entrada de teclado, aquí
            #Eventos teclado player 1
            if event.type  == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                            self.x_speed = -3
                    if event.key == pygame.K_RIGHT:
                            self.x_speed = 3
                    if event.key == pygame.K_UP:
                            self.y_speed = -3
                    if event.key == pygame.K_DOWN:
                            self.y_speed = 3
            if event.type  == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                            self.x_speed = 0
                    if event.key == pygame.K_RIGHT:
                            self.x_speed = 0
                    if event.key == pygame.K_UP:
                            self.y_speed = 0
                    if event.key == pygame.K_DOWN:
                            self.y_speed = 0
                            
            #Eventos teclado player 2
            if event.type  == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                            self.x1_speed = -3
                    if event.key == pygame.K_d:
                            self.x1_speed = 3
                    if event.key == pygame.K_w:
                            self.y1_speed = -3
                    if event.key == pygame.K_s:
                            self.y1_speed = 3
            if event.type  == pygame.KEYUP:
                    if event.key == pygame.K_a:
                            self.x1_speed = 0
                    if event.key == pygame.K_d:
                            self.x1_speed = 0
                    if event.key == pygame.K_w:
                            self.y1_speed = 0
                    if event.key == pygame.K_s:
                            self.y1_speed = 0
           
        

            
        #Hacer que los recuadros negros permanezcan en ese rango
        if(self.coord_y>525 or self.coord_y<275):
            self.speed_y *= -1
        if(self.coord_x2>650 or self.coord_x2<150):
            self.speed_x2 *= -1
        if(self.coord_y4>325 or self.coord_y4<175):
            self.speed_y4 *= -1
        if(self.coord_y5>175 or self.coord_y5<50):
            self.speed_y5 *= -1
        if(self.coord_x6>800 or self.coord_x6<500):
            self.speed_x6 *= -1
        if(self.coord_y7>275 or self.coord_y7<50):
            self.speed_y7 *= -1
        if(self.coord_x8>600 or self.coord_x8<500):
            self.speed_x8 *= -1
        
        
            
        #Inicio de la animación
        self.coord_y += self.speed_y
        self.coord_x2 += self.speed_x2
        self.coord_y4 += self.speed_y4
        self.coord_y5 += self.speed_y5
        self.coord_x6 += self.speed_x6
        self.coord_y7 += self.speed_y7
        self.coord_x8 += self.speed_x8

        #Inicio animacion jugador 1 y 2
        self.x_coord += self.x_speed
        self.y_coord += self.y_speed
        self.x1_coord += self.x1_speed
        self.y1_coord += self.y1_speed

    def show_timer(self):
        minutes = self.timer // 60
        seconds = self.timer % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        text = self.fuente.render(timer_text, True, (255, 255, 255))
        self.screen.blit(text, (425, 8))
        
    def dibujar_juego2(self):

        #Hacer visible/invisible el mouse
        pygame.mouse.set_visible(0)

        # Dibujar elementos del juego en la pantalla
        #Color de fondo
        screen.fill(self.GREY)
        
        self.checkpoint = []
        self.zonas_muerte2 = []
        self.zonas_negras = []

        spawn = pygame.draw.rect(screen, self.GREEN_2, (200,275,50,50))
        self.checkpoint.append(spawn)

        self.meta = pygame.draw.rect(screen, self.GREEN, (650,275,50,50))
        
        #Zona del contador
        for z in range(0, 900, 1):
            pygame.draw.rect(screen, self.BLACK, (z, 0, 40, 40))
            pygame.draw.rect(screen, self.WHITE, (z, 40, 1, 1))
        
        # Calcula el tiempo transcurrido desde el inicio
        elapsed_time = time.time() - self.start_time

        # Actualiza el temporizador restando el tiempo transcurrido
        self.timer = max(self.initial_time - int(elapsed_time), 0)

        if self.timer == 0:
            # El tiempo ha terminado, puedes tomar acciones aquí
            running = False  # Por ejemplo, terminar el juego
            
        # Limpia la pantalla y muestra el temporizador
        self.show_timer()
        

        #Zonas amarillas del mapa
        for z in range(275, 550, 50):
            zona = pygame.Rect(100, z, 100, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
            

        for z in range(200, 700, 50):
            zona= pygame.Rect(z, 525, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(600, 750, 50):
            zona= pygame.Rect(z, 475, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(650, 800, 50):
            zona= pygame.Rect(z, 425, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(700, 850, 50):
            zona= pygame.Rect(z, 375, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(750, 850, 50):
            zona= pygame.Rect(z, 325, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(50, 350, 50):
            zona = pygame.Rect(800, z, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(500, 800, 50):
            zona= pygame.Rect(z, 50, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        for z in range(50, 325, 25):
            zona = pygame.Rect(500, z, 100, 25)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
        zona = pygame.Rect(600, 275, 50, 50)
        self.zonas_muerte2.append(zona)
        pygame.draw.rect(screen, self.YELLOW, zona)

        #Zonas de control
        control = pygame.draw.rect(screen, self.GREEN_2, (100,528,100,50))
        self.checkpoint.append(control)

        control = pygame.draw.rect(screen, self.GREEN_2, (803,325,50,50))
        self.checkpoint.append(control)
    
        control = pygame.draw.rect(screen, self.GREEN_2, (803,50,50,50))
        self.checkpoint.append(control)

        #Objeto a mover con teclado
        self.jugador1 = pygame.draw.rect (screen, self.RED, (self.x1_coord, self.y1_coord, 10, 10))
        self.jugador2 = pygame.draw.rect (screen, self.BLUE, (self.x_coord, self.y_coord, 10, 10))
        
        
        
        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x, self.coord_y, 100, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x2, self.coord_y2), 10)
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (630, 525, 20, 20))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (650, 475, 50, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (700, 425, 50, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (750, 375, 50, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x4, self.coord_y4, 50, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x5, self.coord_y5, 50, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x6, self.coord_y6, 50, 50))
        self.zonas_negras.append(plataforma)
    
        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x7, self.coord_y7, 100, 50))
        self.zonas_negras.append(plataforma)

        plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x8, self.coord_y8, 100, 50))
        self.zonas_negras.append(plataforma)


        #Creando espacio en el que se podrá jugar
        self.limites_negros = []
        
        #Dibujar todo el contorno negro
        for x in range(100, 200, 3):
            borde1 = pygame.Rect(x, 275, 3, 3)  
            borde2 = pygame.Rect(x, 575, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])

        for y in range(275, 325, 3):
            borde1 = pygame.Rect(100, y, 3, 3)  
            borde2 = pygame.Rect(250, y, 3, 3)  
            pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(200, 250, 3):
            borde1 = pygame.Rect(x, 275, 3, 3)  
            borde2 = pygame.Rect(x, 325, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(325, 525, 3):
            borde1 = pygame.Rect(100, y, 3, 3)  
            borde2 = pygame.Rect(200, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(525, 575, 3):
            borde1 = pygame.Rect(100, y, 3, 3)  
            borde2 = pygame.Rect(700, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(200, 600, 3):
            borde1 = pygame.Rect(x, 525, 3, 3)  
            borde2 = pygame.Rect(x, 575, 3, 3)  
            pygame.draw.rect(screen, self.BLACK, (x, 525, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3))
            self.limites_negros.extend([borde1, borde2])

        for x in range(600, 650, 3):
            borde1 = pygame.Rect(x, 475, 3, 3)  
            borde2 = pygame.Rect(x, 575, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (x, 475, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(650, 700, 3):
            borde1 = pygame.Rect(x, 425, 3, 3)  
            borde2 = pygame.Rect(x, 575, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (x, 425, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(700, 750, 3):
            borde1 = pygame.Rect(x, 375, 3, 3)  
            borde2 = pygame.Rect(x, 525, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (x, 375, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 525, 3, 3))  
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(750, 800, 3):
            borde1 = pygame.Rect(x, 325, 3, 3)  
            borde2 = pygame.Rect(x, 475, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 475, 3, 3))  
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(800, 850, 3):
            borde1 = pygame.Rect(x, 50, 3, 3)  
            borde2 = pygame.Rect(x, 425, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 425, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(475, 525, 3):
            borde1 = pygame.Rect(600, y, 3, 3)  
            borde2 = pygame.Rect(750, y, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (600, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (750, y, 3, 3))  
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(425, 475, 3):
            borde1 = pygame.Rect(650, y, 3, 3)  
            borde2 = pygame.Rect(800, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(375, 425, 3):
            borde1 = pygame.Rect(700, y, 3, 3)  
            borde2 = pygame.Rect(850, y, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3))  
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(325, 375, 3):
            borde1 = pygame.Rect(750, y, 3, 3)  
            borde2 = pygame.Rect(850, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (750, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(50, 325, 3):
            borde1 = pygame.Rect(500, y, 3, 3)  
            borde2 = pygame.Rect(850, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(100, 275, 3):
            borde1 = pygame.Rect(600, y, 3, 3)  
            borde2 = pygame.Rect(800, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (600, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for y in range(275, 325, 3):
            borde1 = pygame.Rect(700, y, 3, 3)  
            borde2 = pygame.Rect(800, y, 3, 3) 
            pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(700, 800, 3):
            borde1 = pygame.Rect(x, 50, 3, 3)  
            borde2 = pygame.Rect(x, 100, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 100, 3, 3))  
            self.limites_negros.extend([borde1, borde2])
        
        for x in range(600, 700, 3):
            borde1 = pygame.Rect(x, 50, 3, 3)  
            borde2 = pygame.Rect(x, 100, 3, 3) 
            borde3 = pygame.Rect(x, 275, 3, 3)  
            borde4 = pygame.Rect(x, 325, 3, 3)
            pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 100, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))  
            self.limites_negros.extend([borde1, borde2, borde3, borde4])
        
        for x in range(500, 600, 3):
            borde1 = pygame.Rect(x, 50, 3, 3)  
            borde2 = pygame.Rect(x, 325, 3, 3)  
            pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))
            self.limites_negros.extend([borde1, borde2])
        
    def colisiones2(self):
        # Actualizar la lógica del juego, movimiento de jugadores, colisiones2, etc.
        # Colisión con límites negros para jugador 1
        for limite in self.limites_negros:
            if self.jugador1.colliderect(limite):
                if self.x1_speed > 0 and limite.left <= self.jugador1.right:
                    self.x1_speed = 0
                    self.x1_coord = limite.left - self.jugador1.width
                elif self.x1_speed < 0 and limite.right >= self.jugador1.left:
                    self.x1_speed = 0
                    self.x1_coord = limite.right
                if self.y1_speed > 0 and limite.top <= self.jugador1.bottom:
                    self.y1_speed = 0
                    self.y1_coord = limite.top - self.jugador1.height
                elif self.y1_speed < 0 and limite.bottom >= self.jugador1.top:
                    self.y1_speed = 0
                    self.y1_coord = limite.bottom

        # Colisión con límites negros para jugador 2
        for limite in self.limites_negros:
            if self.jugador2.colliderect(limite):
                if self.x_speed > 0 and limite.left <= self.jugador2.right:
                    self.x_speed = 0
                    self.x_coord = limite.left - self.jugador2.width
                elif self.x_speed < 0 and limite.right >= self.jugador2.left:
                    self.x_speed = 0
                    self.x_coord = limite.right
                if self.y_speed > 0 and limite.top <= self.jugador2.bottom:
                    self.y_speed = 0
                    self.y_coord = limite.top - self.jugador2.height
                elif self.y_speed < 0 and limite.bottom >= self.jugador2.top:
                    self.y_speed = 0
                    self.y_coord = limite.bottom

        # Colisión entre jugadores
        if self.jugador1.colliderect(self.jugador2):
            # Calcula el vector entre los dos jugadores
            self.dx = self.x1_coord - self.x_coord
            self.dy = self.y1_coord - self.y_coord
            self.distancia = math.sqrt(self.dx ** 2 + self.dy ** 2)
        
            # Calcula el vector de separación mínimo (evita la división por cero)
            if self.distancia != 0:
                overlap = (self.jugador1.width + self.jugador2.width) - self.distancia
                self.dx /= self.distancia
                self.dy /= self.distancia
            else:
                overlap = 1.0
        
            # Ajusta las posiciones para evitar la superposición
            self.x1_coord += self.dx * (overlap / 2)
            self.y1_coord += self.dy * (overlap / 2)
            self.x_coord -= self.dx * (overlap / 2)
            self.y_coord -= self.dy * (overlap / 2)
        
            # Detiene a ambos jugadores
            self.x1_speed = 0
            self.y1_speed = 0
            self.x_speed = 0
            self.y_speed = 0
        
        # Verificar si los jugadores están tocando "spawn," "meta" o "zona_negra"
        no_colision_jugador1 = True  # Suponemos que no hay colisión inicialmente
        
        

        # Verificar colisiones2 con los checkpoints
        if self.checkpoint[0].colliderect(self.jugador1):
            self.ultimo_checkpoint_jugador1 = 0
            no_colision_jugador1 = False
        
        if self.checkpoint[1].colliderect(self.jugador1):
            self.ultimo_checkpoint_jugador1 = 1
            no_colision_jugador1 = False
        
        if self.checkpoint[2].colliderect(self.jugador1):
            self.ultimo_checkpoint_jugador1 = 2
            no_colision_jugador1 = False
        
        if self.checkpoint[3].colliderect(self.jugador1):
            self.ultimo_checkpoint_jugador1 = 3
            no_colision_jugador1 = False

        # Verificar colisiones2 con las zonas negras
        for zona_negra_rect in self.zonas_negras:
            if zona_negra_rect.colliderect(self.jugador1):
                no_colision_jugador1 = False
                break  # Si hay una colisión, no es necesario seguir verificando

        # Verificar colisiones2 con la meta
        if self.meta.colliderect(self.jugador1):
            no_colision_jugador1 = False

        # Si no hubo colisiones2 con ningún elemento
        if no_colision_jugador1:
            if self.ultimo_checkpoint_jugador1 == 0:
                # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                self.x1_coord = 220
                self.y1_coord = 285
            if self.ultimo_checkpoint_jugador1 == 1:
                self.x1_coord = 150
                self.y1_coord = 540
            if self.ultimo_checkpoint_jugador1 == 2:
                self.x1_coord = 820
                self.y1_coord = 350
            if self.ultimo_checkpoint_jugador1 == 3:
                self.x1_coord = 820
                self.y1_coord = 70
            self.sonido_muerte.play()

        # Verificar colisiones2 para el jugador 2 (puedes repetir el mismo proceso)
        no_colision_jugador2 = True

        if self.checkpoint[0].colliderect(self.jugador2):
            self.ultimo_checkpoint_jugador2 = 0
            no_colision_jugador2 = False
        
        if self.checkpoint[1].colliderect(self.jugador2):
            self.ultimo_checkpoint_jugador2 = 1
            no_colision_jugador2 = False
        
        if self.checkpoint[2].colliderect(self.jugador2):
            self.ultimo_checkpoint_jugador2 = 2
            no_colision_jugador2 = False
        
        if self.checkpoint[3].colliderect(self.jugador2):
            self.ultimo_checkpoint_jugador2 = 3
            no_colision_jugador2 = False

        for zona_negra_rect in self.zonas_negras:
            if zona_negra_rect.colliderect(self.jugador2):
                no_colision_jugador2 = False
                break

        if self.meta.colliderect(self.jugador2):
            no_colision_jugador2 = False

        if no_colision_jugador2:
            if self.ultimo_checkpoint_jugador2 == 0:
                # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                self.x_coord = 220
                self.y_coord = 285
            if self.ultimo_checkpoint_jugador2 == 1:
                self.x_coord = 150
                self.y_coord = 540
            if self.ultimo_checkpoint_jugador2 == 2:
                self.x_coord = 820
                self.y_coord = 350
            if self.ultimo_checkpoint_jugador2 == 3:
                self.x_coord = 820
                self.y_coord = 70
            self.sonido_muerte.play()
        print(self.ultimo_checkpoint_jugador1, self.ultimo_checkpoint_jugador2)

        if (self.meta.colliderect(self.jugador1) or self.meta.colliderect(self.jugador2)):
            self.sonido_ganar.play()
        if (self.meta.colliderect(self.jugador1) and self.meta.colliderect(self.jugador2)):
            self.jugarNivelDos()
      
    def jugarNivelDos(self):
        while True:
            self.dibujar_juego2()
            self.eventos_teclado2()
            self.colisiones2()
            self.clock.tick(60) 
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.jugarNivelDos()
