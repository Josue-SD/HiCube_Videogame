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
        self.coord_x9 = 250
        self.coord_y9 = 150
        self.coord_x10 = 300
        self.coord_y10 = 400
        self.coord_x11 = 400
        self.coord_y11 = 150
        self.coord_x12 = 450
        self.coord_y12 = 400
        self.coord_x13 = 550
        self.coord_y13 = 150
        self.coord_x14 = 600
        self.coord_y14 = 400

        #Velocidad de animacion
        self.speed_x9 = 2
        self.speed_y9 = 2
        self.speed_x10 = 2
        self.speed_y10 = 2
        self.speed_x11 = 2
        self.speed_y11 = 2
        self.speed_x12 = 2
        self.speed_y12 = 2
        self.speed_x13 = 2
        self.speed_y13 = 2
        self.speed_x14 = 2
        self.speed_y14 = 2

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

    def contador(self):
        minutes = self.timer // 60
        seconds = self.timer % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        text = self.fuente.render(timer_text, True, (255, 255, 255))
        self.screen.blit(text, (425, 8))
        
    def jugarNivel2(self):

        def eventos_teclado2():
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
            if(self.coord_y9>400 or self.coord_y9<150):
                self.speed_y9 *= -1
            if(self.coord_y10>400 or self.coord_y10<150):
                self.speed_y10 *= -1
            if(self.coord_y11>400 or self.coord_y11<150):
                self.speed_y11 *= -1
            if(self.coord_y12>400 or self.coord_y12<150):
                self.speed_y12 *= -1
            if(self.coord_y13>400 or self.coord_y13<150):
                self.speed_y13 *= -1
            if(self.coord_y14>400 or self.coord_y14<150):
                self.speed_y14 *= -1
            
            
                
            #Inicio de la animación
            self.coord_y9 += self.speed_y9
            self.coord_y10 += self.speed_y10
            self.coord_y11 += self.speed_y11
            self.coord_y12 += self.speed_y12
            self.coord_y13 += self.speed_y13
            self.coord_y14 += self.speed_y14

            #Inicio animacion jugador 1 y 2
            self.x_coord += self.x_speed
            self.y_coord += self.y_speed
            self.x1_coord += self.x1_speed
            self.y1_coord += self.y1_speed

        def dibujar_juego2():

            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(0)

            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            
            self.checkpoint = []
            self.zonas_muerte2 = []
            self.zonas_negras = []

            spawn = pygame.draw.rect(screen, self.GREEN_2, (200,275,53,50))
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
            self.contador()
            

            #Zonas amarillas del mapa
            for z in range(150, 450, 50):
                zona = pygame.Rect(253, z, 100, 50)
                self.zonas_muerte2.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)

                zona = pygame.Rect(400, z, 100, 50)
                self.zonas_muerte2.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)

                zona = pygame.Rect(550, z, 100, 50)
                self.zonas_muerte2.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
                
            zona = pygame.Rect(500, 275, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)

            zona = pygame.Rect(350, 275, 50, 50)
            self.zonas_muerte2.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)
        
            
            #Objeto a mover con teclado
            self.jugador1 = pygame.draw.rect (screen, self.RED, (self.x1_coord, self.y1_coord, 10, 10))
            self.jugador2 = pygame.draw.rect (screen, self.BLUE, (self.x_coord, self.y_coord, 10, 10))
            
            #Zonas negras
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x9, self.coord_y9, 50, 50))
            self.zonas_negras.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x10, self.coord_y10, 50, 50))
            self.zonas_negras.append(plataforma)


            plataforma = pygame.draw.rect(screen, self.BLACK, (350, 275, 53, 50))
            self.zonas_negras.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (500, 275, 53, 50))
            self.zonas_negras.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x11, self.coord_y11, 50, 50))
            self.zonas_negras.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x12, self.coord_y12, 50, 50))
            self.zonas_negras.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x13, self.coord_y13, 50, 50))
            self.zonas_negras.append(plataforma)
        
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x14, self.coord_y14, 50, 50))
            self.zonas_negras.append(plataforma)


            #Creando espacio en el que se podrá jugar
            self.limites_negros = []
            
            #Dibujar todo el contorno negro
            for x in range(250, 350, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])

            for x in range(400, 500, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for x in range(550, 650, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for x in range(350, 400, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for x in range(500, 550, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for x in range(650, 700, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])

            for y in range(275, 325, 3):
                borde1 = pygame.Rect(200, y, 3, 3)  
                borde2 = pygame.Rect(700, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                self.limites_negros.extend([borde1, borde2])
            
            for x in range(200, 250, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (350, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (400, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (550, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (350, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (400, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (550, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3)) 
                self.limites_negros.extend([borde1, borde2])
            
        def colisiones2():
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
                self.jugarNivel2()
        
        while True:
            dibujar_juego2()
            eventos_teclado2()
            colisiones2()
            self.clock.tick(60) 
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.jugarNivel2()
