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

        self.ultimo_checkpoint5_jugador1 = 0
        self.ultimo_checkpoint5_jugador2 = 0
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
        self.coord_x20 = 125
        self.coord_y20 = 300
        self.coord_x21 = 125
        self.coord_y21 = 180
        self.coord_x22 = 125
        self.coord_y22 = 360
        self.coord_x23 = 125
        self.coord_y23 = 430
        self.coord_x24 = 460
        self.coord_y24 = 180
        self.coord_x25 = 620
        self.coord_y25 = 360
        self.coord_x26 = 620
        self.coord_y26 = 400
        self.coord_x27 = 500
        self.coord_y27 = 430
        self.coord_x28 = 500
        self.coord_y28 = 300

        #Velocidad de animacion
        self.speed_x20 = 3
        self.speed_y20 = 3
        self.speed_x21 = 3
        self.speed_y21 = 3
        self.speed_x22 = 3
        self.speed_y22 = 3
        self.speed_x23 = 3
        self.speed_y23 = 3
        self.speed_x24 = 3
        self.speed_y24 = 3
        self.speed_x25 = 3
        self.speed_y25 = 3
        self.speed_x26 = 3
        self.speed_y26 = 3
        self.speed_x27 = 3
        self.speed_y27 = 3
        self.speed_x28 = 3
        self.speed_y28 = 3

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
        
    def jugarNivel5(self):

        def eventos_teclado5():
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
            if(self.coord_x20<125 or self.coord_x20 >200):
                self.speed_y20 *= -1
                self.speed_x20 *= -1
            if(self.coord_x21<125 or self.coord_x21 >330):
                self.speed_y21 *= -1
                self.speed_x21 *= -1
            if(self.coord_x22<125 or self.coord_x22 >330):
                self.speed_y22 *= -1
                self.speed_x22 *= -1
            if(self.coord_x23<125 or self.coord_x23 >430):
                self.speed_y23 *= -1
                self.speed_x23 *= -1
            if(self.coord_x24<460 or self.coord_x24 >760):
                self.speed_y24 *= -1
                self.speed_x24 *= -1
            if(self.coord_x25<620 or self.coord_x25 >760):
                self.speed_y25 *= -1
                self.speed_x25 *= -1
            if(self.coord_x26<620 or self.coord_x26 >760):
                self.speed_y26 *= -1
                self.speed_x26 *= -1
            if(self.coord_x27<500 or self.coord_x27 >760):
                self.speed_y27 *= -1
                self.speed_x27 *= -1
            if(self.coord_x28<500 or self.coord_x28 >650):
                self.speed_y28 *= -1
                self.speed_x28 *= -1
            
            
                
            #Inicio de la animación
            self.coord_x20 += self.speed_x20
            self.coord_x21 += self.speed_x21
            self.coord_x22 += self.speed_x22
            self.coord_x23 += self.speed_x23
            self.coord_x24 += self.speed_x24
            self.coord_x25 += self.speed_x25
            self.coord_x26 += self.speed_x26
            self.coord_x27 += self.speed_x27
            self.coord_x28 += self.speed_x28

            #Inicio animacion jugador 1 y 2
            self.x_coord += self.x_speed
            self.y_coord += self.y_speed
            self.x1_coord += self.x1_speed
            self.y1_coord += self.y1_speed

        def dibujar_juego5():

            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(0)

            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            
            self.checkpoint5 = []
            self.zonas_muerte5 = []
            self.zonas_negra5 = []
            
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
            zona = pygame.Rect(100, 150, 700, 300)
            self.zonas_muerte5.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)

            #Zonas de control
            spawn = pygame.draw.rect(screen, self.GREEN_2, (200,278,50,50))
            self.checkpoint5.append(spawn)

            control = pygame.draw.rect(screen, self.GREEN_2, (425,150,50,300))
            self.checkpoint5.append(control)

            self.meta5 = pygame.draw.rect(screen, self.GREEN, (650,275,50,50))
            
            
            #Objeto a mover con teclado
            self.jugador1 = pygame.draw.rect (screen, self.RED, (self.x1_coord, self.y1_coord, 10, 10))
            self.jugador2 = pygame.draw.rect (screen, self.BLUE, (self.x_coord, self.y_coord, 10, 10))
            
            #Zonas negras
            plataforma = pygame.draw.rect(screen, self.BLACK, (120, 180, 3, 120))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (330, 180, 3, 180))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (120, 360, 3, 70))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (760, 180, 3, 180))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (500, 300, 3, 130))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (620, 360, 3, 40))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (760, 400, 3, 30))
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x20, self.coord_y20), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x21, self.coord_y21), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x22, self.coord_y22), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x23, self.coord_y23), 5)
            self.zonas_negra5.append(plataforma)
        
            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x24, self.coord_y24), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x25, self.coord_y25), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x26, self.coord_y26), 5)
            self.zonas_negra5.append(plataforma)

            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x27, self.coord_y27), 5)
            self.zonas_negra5.append(plataforma)
        
            plataforma = pygame.draw.circle(screen, self.BLACK, (self.coord_x28, self.coord_y28), 5)
            self.zonas_negra5.append(plataforma)


            #Creando espacio en el que se podrá jugar
            self.limites_negros5 = []
            
            #Dibujar todo el contorno negro
            for x in range(100, 800, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros5.extend([borde1, borde2])
            
            
            for x in range(650, 700, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros5.extend([borde1, borde2])

            for y in range(278, 325, 3):
                borde1 = pygame.Rect(248, y, 3, 3)  
                borde2 = pygame.Rect(698, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (248, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (698, y, 3, 3))
                self.limites_negros5.extend([borde1, borde2])
            
            for x in range(200, 250, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros5.extend([borde1, borde2])
            
            for y in range(150, 450, 3):
                borde1 = pygame.Rect(100, y, 3, 3)  
                borde2 = pygame.Rect(800, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3))
                self.limites_negros5.extend([borde1, borde2])
            
            
        def colisiones5():
            # Actualizar la lógica del juego, movimiento de jugadores, colisiones5, etc.
            # Colisión con límites negros para jugador 1
            for limite in self.limites_negros5:
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
            for limite in self.limites_negros5:
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
            
            # Verificar si los jugadores están tocando "spawn," "meta5" o "zona_negra"
            no_colision_jugador1 = True  # Suponemos que no hay colisión inicialmente
            
            

            # Verificar colisiones5 con los checkpoint5s
            if self.checkpoint5[0].colliderect(self.jugador1):
                self.ultimo_checkpoint5_jugador1 = 0
                no_colision_jugador1 = False
            
            if self.checkpoint5[1].colliderect(self.jugador1):
                self.ultimo_checkpoint5_jugador1 = 1
                no_colision_jugador1 = False

            # Verificar colisiones5 con las zonas negras
            for zona_negra_rect in self.zonas_negra5:
                if zona_negra_rect.colliderect(self.jugador1):
                    no_colision_jugador1 = False
                    break  # Si hay una colisión, no es necesario seguir verificando

            # Verificar colisiones5 con la meta5
            if self.meta5.colliderect(self.jugador1):
                no_colision_jugador1 = False

            # Si no hubo colisiones5 con ningún elemento
            if no_colision_jugador1:
                if self.ultimo_checkpoint5_jugador1 == 0:
                    # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                    self.x1_coord = 220
                    self.y1_coord = 285
                if self.ultimo_checkpoint5_jugador1 == 1:
                    self.x1_coord = 450
                    self.y1_coord = 170
                self.sonido_muerte.play()

            # Verificar colisiones5 para el jugador 2 (puedes repetir el mismo proceso)
            no_colision_jugador2 = True

            if self.checkpoint5[0].colliderect(self.jugador2):
                self.ultimo_checkpoint5_jugador2 = 0
                no_colision_jugador2 = False
            
            if self.checkpoint5[1].colliderect(self.jugador2):
                self.ultimo_checkpoint5_jugador2 = 1
                no_colision_jugador2 = False

            for zona_negra_rect in self.zonas_negra5:
                if zona_negra_rect.colliderect(self.jugador2):
                    no_colision_jugador2 = False
                    break

            if self.meta5.colliderect(self.jugador2):
                no_colision_jugador2 = False

            if no_colision_jugador2:
                if self.ultimo_checkpoint5_jugador2 == 0:
                    # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                    self.x_coord = 220
                    self.y_coord = 285
                if self.ultimo_checkpoint5_jugador2 == 1:
                    self.x_coord = 450
                    self.y_coord = 180
                self.sonido_muerte.play()

            if (self.meta5.colliderect(self.jugador1) or self.meta5.colliderect(self.jugador2)):
                self.sonido_ganar.play()
            if (self.meta5.colliderect(self.jugador1) and self.meta5.colliderect(self.jugador2)):
                self.jugarNivel5()
        
        while True:
            dibujar_juego5()
            eventos_teclado5()
            colisiones5()
            self.clock.tick(60) 
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.jugarNivel5()
