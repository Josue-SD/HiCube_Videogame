
import pygame, sys, random, math, threading, time
from tkinter import *
from tkinter.font import *

#Iniciando 
pygame.init()

#Crear ventana
size = (900, 600)
screen = pygame.display.set_mode(size)
fuente = pygame.font.SysFont("cambria", 25)
fuente_grande = pygame.font.SysFont("cambria", 40)
fuenteTimer = pygame.font.SysFont("cambria", 20)

#Icono y título del videojuego
pygame.display.set_caption("Hicube")

class Boton():
    def __init__(self, imagen, x_pos, y_pos, nombre_boton):
        self.imagen = imagen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
        self.nombre_boton = nombre_boton
        self.texto = fuente.render(self.nombre_boton, True, (255, 255, 255))
        self.text_rect = self.texto.get_rect(center=self.rect.center)

    def actualizar(self, screen):
        if self.imagen is not None:
            screen.blit(self.imagen, self.rect)
        screen.blit(self.texto, self.text_rect)

    def checar_presionado(self, posicion):
        if self.rect.collidepoint(posicion):
            return True
        return False

    def cambiar_color(self, posicion):
        if self.rect.collidepoint(posicion):
            self.texto = fuente.render(self.nombre_boton, True, (0, 255, 0))
        else:
            self.texto = fuente.render(self.nombre_boton, True, (255, 255, 255))

class Juego:

    def __init__(self):
        
        # Inicialización de variables, ventanas, sonidos, etc.
        self.icono = pygame.image.load("Imagenes/Icono.png")
        pygame.display.set_icon(self.icono)

        self.ultimo_checkpoint_jugador1 = 0
        self.ultimo_checkpoint_jugador2 = 0
        self.bandera_ganar_jugador1 = 0
        self.bandera_ganar_jugador2 = 0
        self.bandera_controles_tutorial = False
        
        self.numero_nivel = {
            "2": self.jugarNivel2,
            "3": self.jugarNivel4,
            "4": self.jugarNivel3,
            "5": self.jugarNivel5,
            # Agrega más mapeos según sea necesario
        }
        
        self.jugando_nivel = "0"

        #Paleta de colores
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (100,0,0)
        self.RED2 = (255,0,0)
        self.ORANGE = (255,102,0)
        self.BLUE = (0,0,100)
        self.BLUE2 = (0,119,255)
        self.AQUA = (0,255,191)
        self.SKYBLUE = (65,148,178)
        self.PURPLE = (93,0,255)
        self.PINK = (242,0,255)
        self.FIUSHA = (255,0,111)
        self.GREY = (31,31,31)
        self.GREY2 = (100,100,100)
        self.GREEN = (0, 255, 0)
        self.GREEN_2 = (0, 255, 140)
        self.GREEN_SELECCION = (0,255,0)
        self.GREEN_PIZARRA = (0, 43, 33)
        self.YELLOW = (255, 255, 0)
        self.YELLOW_MONEDA = (230, 217, 16)
        self.YELLOW2_MONEDA = (236, 187, 0)
        self.MOSTAZA = (255,200,0)
        self.BROWN = (64,16,16)
        
        self.angulo_estrella = 0  
        self.medida_base_estrella = 17

        #Aura de los jugadores 1 y 2
        self.radio_aura = 7
        self.superficie_aura = pygame.Surface((2 * self.radio_aura, 2 * self.radio_aura), pygame.SRCALPHA)
        pygame.draw.circle(self.superficie_aura, (255,242,0, 50), (self.radio_aura, self.radio_aura), self.radio_aura)

        #Color de los jugadores
        self.colorAux1 = self.BLUE
        self.colorAux2 = self.RED

        #Bandera para saber si será juego individual o multijugador
        self.bandera_modo_juego = 0

        #Definicion de sonidos
        self.sonido_muerte = pygame.mixer.Sound("audios/error-126627.mp3")
        self.sonido_muerte.set_volume(0.9)
        self.sonido_ganar = pygame.mixer.Sound("audios/success-1-6297.mp3")
        self.sonido_ganar.set_volume(0.2)
        self.musica_fondo = pygame.mixer.Sound("audios/SHAKE.mp3")
        self.musica_fondo.set_volume(0.3)
        self.musica_fondoNiveles = pygame.mixer.Sound("audios/typical-trap-loop-2b-130751.mp3")
        self.musica_fondoNiveles.set_volume(0.3)
        self.musica_fondoNiveles2 = pygame.mixer.Sound("audios/canx27t-see-in-front-of-me-178511.mp3")
        self.musica_fondoNiveles2.set_volume(0.4)
        self.musica_fondoNiveles3 = pygame.mixer.Sound("audios/donx27t-give-up-180419.mp3")
        self.musica_fondoNiveles3.set_volume(0.3)
        self.musica_fondoNiveles4 = pygame.mixer.Sound("audios/sunbeam-180408.mp3")
        self.musica_fondoNiveles4.set_volume(0.3)
        self.musica_fondoTutorial = pygame.mixer.Sound("audios/sinnesloschen-beam-117362 (1).mp3")
        self.musica_fondoTutorial.set_volume(0.3)
        self.audio_menu = pygame.mixer.Sound("audios/POP.mp3")
        self.audio_menu.set_volume(0.1)

        #Valores para el volumen
        self.volumenPrincipal = 15
        self.volumenMusica = 30
        self.volumenEfectos = 49

        #Definir fondo de pantalla
        self.fondo_menu_princial = pygame.image.load("Imagenes/MenuPrincipal.png")
        self.fondo_pantalla_carga = pygame.image.load("Imagenes/pantallaCarga.png")
        self.fondo_tutorial0 = pygame.image.load("Imagenes/Tutorial0.png")
        self.fondo_tutorial1 = pygame.image.load("Imagenes/Tutorial1_1.png")
        self.fondo_tutorial2 = pygame.image.load("Imagenes/Tutorial2_2.png")
        self.fondo_tutorial3 = pygame.image.load("Imagenes/Tutorial3_3.png")
        self.fondo_tutorial4 = pygame.image.load("Imagenes/Tutorial4_4.png")
        self.fondo_tutorial5 = pygame.image.load("Imagenes/Tutorial5_5.png")
        self.fondo_tutorial7 = pygame.image.load("Imagenes/Tutorial7.png")
        self.fondo_Opciones = pygame.image.load("Imagenes/Opciones.png")
        self.fondo_juego_terminado = pygame.image.load("Imagenes/JuegoTerminado.png")
        self.fondo_nivel_vacio = pygame.image.load("Imagenes/ModoDeJuegoVacio.png")
        self.fondo_nivel_VS = pygame.image.load("Imagenes/ModoDeJuegoVersus.png")
        self.fondo_nivel_solitario = pygame.image.load("Imagenes/ModoDeJuegoSolitario.png")
        self.fondo_comic = pygame.image.load("Imagenes/Comic.png")
        self.fondo_comic2 = pygame.image.load("Imagenes/Comic2.jpg")
        self.fondo_comic3 = pygame.image.load("Imagenes/Comic3.jpg")
        self.fondo_comic4 = pygame.image.load("Imagenes/Comic4.png")

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
        self.imagen_boton2 = pygame.transform.scale(pygame.image.load("Imagenes/transparente.png"), (30, 35))
        self.imagen_boton3 = pygame.transform.scale(pygame.image.load("Imagenes/Boton_Sonido.png"), (60, 60))

        self.boton = Boton(self.imagen_boton, 450, 390, "Jugar")
        self.boton2 = Boton(self.imagen_boton, 450, 460, "Opciones")
        self.boton3 =Boton(self.imagen_boton, 450, 530, "Salir")
        self.boton4 = Boton(self.imagen_boton2, 880,20, "↩")
        self.boton5 = Boton(self.imagen_boton, 750,550, "Siguiente")
        self.boton6 = Boton(self.imagen_boton, 465,420, "Omitir tutorial")
        self.boton7 = Boton(self.imagen_boton, 465,340, "Continuar")
        self.boton8 = Boton(self.imagen_boton, 450,410, "Continuar")
        self.boton9 = Boton(self.imagen_boton, 450,300, "Sonido")
        self.boton10 = Boton(self.imagen_boton, 450,230, "Personalizar")
        self.boton11 = Boton(self.imagen_boton, 450,370, "Creditos")
        self.boton12 = Boton(self.imagen_boton, 750,550, "Menu Principal")
        self.boton13 = Boton(self.imagen_boton, 750,550, "Regresar")
        self.boton14 = Boton(self.imagen_boton2, 880,20, "≡")
        self.boton19 = Boton(self.imagen_boton, 465,330, "Reiniciar")
        self.boton20 = Boton(self.imagen_boton, 465,410, "Menu Principal")
        self.boton21 = Boton(self.imagen_boton, 250,300, "Multijugador")
        self.boton22 = Boton(self.imagen_boton, 250,400, "Solitario")
        
        #Coordenadas zonas obscuras
        self.coord_x0 = 220
        self.coord_y0 = 375
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

        self.coord_x15 = 250
        self.coord_y15 = 275
        self.coord_x16 = 325
        self.coord_y16 = 200
        self.coord_x17 = 400
        self.coord_y17 = 275
        self.coord_x18 = 475
        self.coord_y18 = 200
        self.coord_x19 = 550
        self.coord_y19 = 275

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

        self.speed_x15 = 1
        self.speed_y15 = 1
        self.speed_largo15 = 2
        self.speed_ancho15 = 2
        self.speed_x16 = 1
        self.speed_y16 = 1
        self.speed_largo16 = 2
        self.speed_ancho16 = 2
        self.speed_x17 = 1
        self.speed_y17 = 1
        self.speed_largo17 = 2
        self.speed_ancho17 = 2
        self.speed_x18 = 1
        self.speed_y18 = 1
        self.speed_largo18 = 2
        self.speed_ancho18 = 2
        self.speed_x19 = 1
        self.speed_y19 = 1
        self.speed_largo19 = 2
        self.speed_ancho19 = 2

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

        #Dimensiones de animacion
        self.largo15 = 100
        self.ancho15 = 100
        self.largo16 = 100
        self.ancho16 = 100
        self.largo17 = 100
        self.ancho17 = 100
        self.largo18 = 100
        self.ancho18 = 100
        self.largo19 = 100
        self.ancho19 = 100

        #Jugador 1 y 2
        self.x_coord = 220
        self.y_coord = 385
        self.x1_coord = 220
        self.y1_coord = 400

        #Velocidad jugador 1 y 2
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0
        
    def contador(self):
        minutes = self.timer // 60
        seconds = self.timer % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        text = fuente.render(timer_text, True, (255, 255, 255))
        self.screen.blit(text, (425, 8))

    def dibujar_octagono(self, eje_x, eje_y, tamaño):
        angulo = 360 / 8
        vertices_octagono = []
        for i in range(8):
            x = eje_x + tamaño * pygame.math.Vector2(1, 0).rotate(angulo * i)[0]
            y = eje_y + tamaño * pygame.math.Vector2(1, 0).rotate(angulo * i)[1]
            vertices_octagono.append((x, y))
        return vertices_octagono

    def dibujar_estrella(self, screen, x, y, size, angulo_estrella):
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

        pygame.draw.polygon(screen, self.YELLOW2_MONEDA, points)

    def funcion_carga(self):

        for i in range(self.TRABAJO):
            ecuacion_matematica = 523687 / 789456 * 89456
            self.cargar_progreso = i 

        self.barra_carga_terminada = True  # Debería ser global

    def pantalla_carga(self):

        # Thread
        threading.Thread(target=self.funcion_carga).start()

        while not self.barra_carga_terminada:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Dibujar la imagen de fondo en la ventana
            screen.blit(self.fondo_pantalla_carga, (0, 0)) 

            # Redimensionar la barra de carga según el progreso
            extension_barra_carga = self.cargar_progreso / self.TRABAJO * 400  

            barra_carga_escalada = pygame.transform.scale(self.barra_carga, (int(extension_barra_carga), 48))
            rectangulo_barra_carga = barra_carga_escalada.get_rect(midleft=(250, 400))

            screen.blit(self.barra_carga_fondo, self.fondo_barra_carga)
            screen.blit(barra_carga_escalada, rectangulo_barra_carga)

            pygame.display.update()
            self.clock.tick(60)
            
    def menu_principal(self):
        self.musica_fondoTutorial.stop()
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)
            for event in pygame.event.get():
                #Condiciones para moverse entre los menus
                if event.type == pygame.QUIT:  
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_modo_juego()
                    if self.boton2.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.opciones()
                    if self.boton3.checar_presionado(self.MENU_MOUSE_POS):
                         pygame.quit()
                         sys.exit()

            # Dibujar la imagen de fondo en la ventana
            screen.blit(self.fondo, (0, 0))

            self.boton.actualizar(self.screen)
            self.boton.cambiar_color(pygame.mouse.get_pos())
            self.boton2.actualizar(self.screen)
            self.boton2.cambiar_color(pygame.mouse.get_pos())
            self.boton3.actualizar(self.screen)
            self.boton3.cambiar_color(pygame.mouse.get_pos())

                
            # Actualizar la pantalla
            pygame.display.update()

    def pantalla_tutorial(self):
        #Corrección de bug
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0
        self.x_coord = 220
        self.y_coord = 385
        self.x1_coord = 220
        self.y1_coord = 400

        #Hacer visible/invisible el mouse
        pygame.mouse.set_visible(1)
        aux_sonido = True
        bandera = False
        # Dibujar elementos del juego en la pantalla
        #Color de fondo

        while bandera == False:

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Dibuja la imagen en la pantalla
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial0, (0, 0)) 
            
            self.boton6.cambiar_color(self.MENU_MOUSE_POS)
            self.boton6.actualizar(screen)

            self.boton7.cambiar_color(self.MENU_MOUSE_POS)
            self.boton7.actualizar(screen)

            self.boton14.cambiar_color(self.MENU_MOUSE_POS)
            self.boton14.actualizar(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Condiciones para el boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton6.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.jugarNivel2()
                    
                    if self.boton7.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        bandera = True
                    
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_dentro_del_juego()

            pygame.display.update()

        while bandera:

            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            while aux_sonido:
                self.musica_fondo.stop()
                self.musica_fondoTutorial.play(-1)
                aux_sonido = False
                
            # Dibuja la imagen en la pantalla
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial1, (0, 0)) 
            

            linea1 = fuenteTimer.render("Las zonas de color verde", False, self.GREEN_2)
            linea2 = fuenteTimer.render("son zonas seguras", False, self.GREEN_2)
            screen.blit(linea1, [100, 150])
            screen.blit(linea2, [100, 170]) 

            
            self.boton5.cambiar_color(self.MENU_MOUSE_POS)
            self.boton5.actualizar(screen)

            self.boton14.cambiar_color(self.MENU_MOUSE_POS)
            self.boton14.actualizar(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Condiciones para el boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if self.boton5.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        bandera = False
                
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_dentro_del_juego()
            self.dibujar_juego()
            self.eventos_teclado()
            self.clock.tick(60) 
        
        while bandera==False:

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Dibuja la imagen en la pantalla
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial2, (0, 0)) 
            self.linea3 = fuenteTimer.render("Evita las zonas", False, self.YELLOW)
            self.linea4 = fuenteTimer.render("color amarillo", False, self.YELLOW)
            screen.blit(self.linea3, [380, 170])
            screen.blit(self.linea4, [380, 190]) 

            self.boton5.cambiar_color(self.MENU_MOUSE_POS)
            self.boton5.actualizar(screen)

            self.boton14.cambiar_color(self.MENU_MOUSE_POS)
            self.boton14.actualizar(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Condiciones para el boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton5.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        bandera = True
                    
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_dentro_del_juego()
            self.dibujar_juego()
            self.eventos_teclado()
            self.clock.tick(60) 
        while bandera:

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Dibuja la imagen en la pantalla
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial3, (0, 0)) 
            self.linea5 = fuenteTimer.render("Llega a la zona verde", False, self.GREEN)
            self.linea6 = fuenteTimer.render("para completar el nivel", False, self.GREEN)
            screen.blit(self.linea5, [575, 213])
            screen.blit(self.linea6, [575, 233])

            self.boton5.cambiar_color(self.MENU_MOUSE_POS)
            self.boton5.actualizar(screen)

            self.boton14.cambiar_color(self.MENU_MOUSE_POS)
            self.boton14.actualizar(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Condiciones para el boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton5.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        bandera = False
                    
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_dentro_del_juego()
            self.dibujar_juego()
            self.eventos_teclado()
            self.clock.tick(60) 
        
        while bandera==False:

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Dibuja la imagen en la pantalla
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial4, (0, 0)) 
            self.linea7 = fuenteTimer.render("Usa las plataformas oscuras para", False, self.WHITE)
            self.linea8 = fuenteTimer.render("atravesar zonas de peligro", False, self.WHITE)
            screen.blit(self.linea7, [175, 200])
            screen.blit(self.linea8, [175, 220]) 

            self.boton5.cambiar_color(self.MENU_MOUSE_POS)
            self.boton5.actualizar(screen)

            self.boton14.cambiar_color(self.MENU_MOUSE_POS)
            self.boton14.actualizar(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Condiciones para el boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton5.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.bandera_controles_tutorial = True
                        self.jugar()
                    
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_dentro_del_juego()
            self.dibujar_juego()
            self.eventos_teclado()
            self.clock.tick(60) 
            pygame.display.update()

    def eventos_teclado(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.boton14.actualizar(self.screen)
        self.boton14.cambiar_color(pygame.mouse.get_pos())
        
        if self.bandera_controles_tutorial:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                                self.audio_menu.play()
                                self.menu_dentro_del_juego()
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
                
        pygame.display.flip()   
            
        #Hacer que permanezca siempre en pantalla dentro de los limites
        if(self.coord_x0>650 or self.coord_x0<200):
            self.speed_x *= -1
        if(self.x_coord>880 or self.x_coord<0):
            self.x_speed *= -1
        if(self.y_coord>580 or self.y_coord<0):
            self.y_speed *= -1
        if(self.x1_coord>880 or self.x1_coord<0):
            self.x1_speed *= -1
        if(self.y1_coord>580 or self.y1_coord<0):
            self.y1_speed *= -1
            
        #Inicio de la animación
        self.coord_x0 += self.speed_x
        self.x_coord += self.x_speed
        self.y_coord += self.y_speed
        self.x1_coord += self.x1_speed
        self.y1_coord += self.y1_speed

    def dibujar_juego(self):

        #Hacer visible/invisible el mouse
        pygame.mouse.set_visible(1)

        # Dibujar elementos del juego en la pantalla
        if self.bandera_controles_tutorial:
            screen.fill(self.GREY)
            screen.blit(self.fondo_tutorial5, (0, 0))
        
    
            #Zona del contador
            for z in range(0, 900, 1):
                pygame.draw.rect(screen, self.BLACK, (z, 0, 40, 40))
                pygame.draw.rect(screen, self.WHITE, (z, 40, 1, 1))

        self.spawn = pygame.draw.rect(screen, self.GREEN_2, (200,375,50,50))
        self.meta = pygame.draw.rect(screen, self.GREEN, (650,375,50,50))
        
        for z in range(250, 650, 50):
            self.zona_muerte = pygame.Rect(z, 375, 50, 50)
            pygame.draw.rect(screen, self.YELLOW, (z, 375, 50, 50))

        #Objeto a mover con teclado

        if self.bandera_modo_juego==1:
            self.jugador1 = pygame.draw.rect (screen, self.colorAux1, (self.x1_coord, self.y1_coord, 10, 10))
            self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
        
        if self.bandera_modo_juego==2:
            self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))

        
        #Zona de dibujo
        self.zona_negra = pygame.draw.rect(screen, self.BLACK, (self.coord_x0, self.coord_y0, 50, 50))
        
        for x in range(200, 700, 3):
            pygame.draw.rect(screen, self.BLACK, (x, 375, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (x, 424, 3, 3))

        for y in range(375, 425, 3):
            pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3))
            pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))

        if self.bandera_controles_tutorial:
            #Creando espacio en el que se podrá jugar
                self.limites_negros_tutorial = []
                
                #Dibujar todo el contorno negro
                for x in range(200, 700, 3):
                    borde1 = pygame.Rect(x, 375, 3, 3)  
                    borde2 = pygame.Rect(x, 425, 3, 3) 
                    self.limites_negros_tutorial.extend([borde1, borde2])
                
                for y in range(375, 425, 3):
                    borde1 = pygame.Rect(200, y, 3, 3)  
                    borde2 = pygame.Rect(700, y, 3, 3) 
                    self.limites_negros_tutorial.extend([borde1, borde2])
        
        if self.bandera_modo_juego==1:
            if self.jugador1.colliderect(self.zona_negra):
                screen.blit(self.superficie_aura, (self.x1_coord - 2, self.y1_coord - 2))
            if self.jugador2.colliderect(self.zona_negra):
                screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

        if self.bandera_modo_juego==2:
            if self.jugador2.colliderect(self.zona_negra):
                screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))     
            
    def colisiones(self):
        if self.bandera_modo_juego==1:
            # Actualizar la lógica del juego, movimiento de jugadores, colisiones, etc.
            # Colisión con límites negros para jugador 1
            for limite in self.limites_negros_tutorial:
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
            for limite in self.limites_negros_tutorial:
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
            if (not self.spawn.colliderect(self.jugador1) and not self.meta.colliderect(self.jugador1) and not self.zona_negra.colliderect(self.jugador1)):
                self.x1_coord = 220
                self.y1_coord = 400
                self.sonido_muerte.play()
            if (not self.spawn.colliderect(self.jugador2) and not self.meta.colliderect(self.jugador2) and not self.zona_negra.colliderect(self.jugador2)):
                self.x_coord = 220
                self.y_coord = 385
                self.sonido_muerte.play()
            if self.meta.colliderect(self.jugador1) and self.bandera_ganar_jugador1 == 0:
                self.bandera_ganar_jugador1 = 1
                self.sonido_ganar.play()
            if self.meta.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                self.bandera_ganar_jugador2 = 1
                self.sonido_ganar.play()
            if (self.meta.colliderect(self.jugador1) and self.meta.colliderect(self.jugador2)):
                self.sonido_ganar.play()
                self.bandera_controles_tutorial = False
                self.nivelUno()
        
        if self.bandera_modo_juego==2:
            # Actualizar la lógica del juego, movimiento de jugadores, colisiones, etc.
            # Colisión con límites negros para jugador 2
            for limite in self.limites_negros_tutorial:
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
            
            # Verificar si los jugadores están tocando "spawn," "meta" o "zona_negra"
            
            if (not self.spawn.colliderect(self.jugador2) and not self.meta.colliderect(self.jugador2) and not self.zona_negra.colliderect(self.jugador2)):
                self.x_coord = 220
                self.y_coord = 385
                self.sonido_muerte.play()
            if self.meta.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                self.bandera_ganar_jugador2 = 1
                self.sonido_ganar.play()
                self.bandera_controles_tutorial = False
                self.nivelUno()
    
    def jugar(self):
         
         while True:
            self.dibujar_juego()
            self.eventos_teclado()
            self.colisiones()
            self.clock.tick(60) 
            pygame.display.flip()
    
    def jugarNivel3(self):

        
        def eventos_teclado3():
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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_dentro_del_nivel()
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.boton14.actualizar(self.screen)
            self.boton14.cambiar_color(pygame.mouse.get_pos())
            
            
            #Hacer que los recuadros negros permanezcan en ese rango
            if(self.coord_x15<250 or self.coord_x15 >280):
                self.speed_y15 *= -1
                self.speed_x15 *= -1
                self.speed_largo15 *= -1
                self.speed_ancho15 *= -1
            if(self.coord_x16<325 or self.coord_x16 >355):
                self.speed_y16 *= -1
                self.speed_x16 *= -1
                self.speed_largo16 *= -1
                self.speed_ancho16 *= -1
            if(self.coord_x17<400 or self.coord_x17 >430):
                self.speed_y17 *= -1
                self.speed_x17 *= -1
                self.speed_largo17 *= -1
                self.speed_ancho17 *= -1
            if(self.coord_x18<475 or self.coord_x18 >505):
                self.speed_y18 *= -1
                self.speed_x18 *= -1
                self.speed_largo18 *= -1
                self.speed_ancho18 *= -1
            if(self.coord_x19<550 or self.coord_x19 >580):
                self.speed_y19 *= -1
                self.speed_x19 *= -1
                self.speed_largo19 *= -1
                self.speed_ancho19 *= -1
            
                
            #Inicio de la animación
            self.coord_x15 += self.speed_x15
            self.coord_y15 += self.speed_y15
            self.coord_x16 += self.speed_x16
            self.coord_y16 += self.speed_y16
            self.coord_x17 += self.speed_x17
            self.coord_y17 += self.speed_y17
            self.coord_x18 += self.speed_x18
            self.coord_y18 += self.speed_y18
            self.coord_x19 += self.speed_x19
            self.coord_y19 += self.speed_y19

            #Animaciones de largo y ancho
            self.largo15 -= self.speed_largo15
            self.ancho15 -= self.speed_ancho15
            self.largo16 -= self.speed_largo16
            self.ancho16 -= self.speed_ancho16
            self.largo17 -= self.speed_largo17
            self.ancho17 -= self.speed_ancho17
            self.largo18 -= self.speed_largo18
            self.ancho18 -= self.speed_ancho18
            self.largo19 -= self.speed_largo19
            self.ancho19 -= self.speed_ancho19

            #Inicio animacion jugador 1 y 2
            self.x_coord += self.x_speed
            self.y_coord += self.y_speed
            self.x1_coord += self.x1_speed
            self.y1_coord += self.y1_speed

        def dibujar_juego3():

            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)

            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            screen.blit(self.fondo_comic2, (0, 0)) 
            
            self.checkpoint3 = []
            self.zonas_muerte3 = []
            self.zonas_negras3 = []

            spawn = pygame.draw.rect(screen, self.GREEN_2, (200,278,53,50))
            self.checkpoint3.append(spawn)

            self.meta3 = pygame.draw.rect(screen, self.GREEN, (650,275,50,50))
            
            #Zona del contador
            for z in range(0, 900, 1):
                pygame.draw.rect(screen, self.BLACK, (z, 0, 40, 40))
                pygame.draw.rect(screen, self.WHITE, (z, 40, 1, 1))
            
            # Calcula el tiempo transcurrido desde el inicio
            elapsed_time = time.time() - self.start_time

            # Actualiza el temporizador restando el tiempo transcurrido
            self.timer = max(self.initial_time - int(elapsed_time), 0)

            if self.timer == 0:
                self.pantalla_juego_terminado()
                
            # Limpia la pantalla y muestra el temporizador
            self.contador()
            

            #Zonas amarillas del mapa
            zona = pygame.Rect(253, 150, 397, 300)
            self.zonas_muerte3.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)

            #Objeto a mover con teclado
            if self.bandera_modo_juego==1:
                self.jugador1 = pygame.draw.rect (screen, self.colorAux1, (self.x1_coord, self.y1_coord, 10, 10))
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
            if self.bandera_modo_juego==2:
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
           
            #Zonas negras

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x15, self.coord_y15, self.largo15, self.ancho15))
            self.zonas_negras3.append(plataforma)
            
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x16, self.coord_y16, self.largo16, self.ancho16))
            self.zonas_negras3.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x17, self.coord_y17, self.largo17, self.ancho17))
            self.zonas_negras3.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x18, self.coord_y18, self.largo18, self.ancho18))
            self.zonas_negras3.append(plataforma)
        
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x19, self.coord_y19, self.largo19, self.ancho19))
            self.zonas_negras3.append(plataforma)

            if self.bandera_modo_juego==1:
                for limite in self.zonas_negras3:
                    if self.jugador1.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x1_coord - 2, self.y1_coord - 2))
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

            if self.bandera_modo_juego==2:
                for limite in self.zonas_negras3:
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2)) 

            #Creando espacio en el que se podrá jugar
            self.limites_negros3 = []
            
            #Dibujar todo el contorno negro
            for x in range(250, 650, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros3.extend([borde1, borde2])
            
            
            for x in range(650, 700, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros3.extend([borde1, borde2])

            for y in range(275, 325, 3):
                borde1 = pygame.Rect(200, y, 3, 3)  
                borde2 = pygame.Rect(700, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                self.limites_negros3.extend([borde1, borde2])
            
            for x in range(200, 250, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros3.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(650, y, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3))
                self.limites_negros3.extend([borde1, borde2]) 
            
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3)) 
                self.limites_negros3.extend([borde1, borde2])
            
        def colisiones3():

            if self.bandera_modo_juego==1:
                # Actualizar la lógica del juego, movimiento de jugadores, colisiones3, etc.
                # Colisión con límites negros para jugador 1
                for limite in self.limites_negros3:
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
                for limite in self.limites_negros3:
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
                
                # Verificar colisiones3 con los checkpoints
                if self.checkpoint3[0].colliderect(self.jugador1):
                    self.ultimo_checkpoint3_jugador1 = 0
                    no_colision_jugador1 = False

                # Verificar colisiones3 con las zonas negras
                for zona_negra_rect in self.zonas_negras3:
                    if zona_negra_rect.colliderect(self.jugador1):
                        no_colision_jugador1 = False
                        break  # Si hay una colisión, no es necesario seguir verificando

                # Verificar colisiones3 con la meta
                if self.meta3.colliderect(self.jugador1):
                    no_colision_jugador1 = False

                # Si no hubo colisiones3 con ningún elemento
                if no_colision_jugador1:
                    if self.ultimo_checkpoint3_jugador1 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x1_coord = 220
                        self.y1_coord = 285
                    self.sonido_muerte.play()

                # Verificar colisiones3 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint3[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint3_jugador2 = 0
                    no_colision_jugador2 = False

                for zona_negra_rect in self.zonas_negras3:
                    if zona_negra_rect.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta3.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint3_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    self.sonido_muerte.play()

                if self.meta3.colliderect(self.jugador1) and self.bandera_ganar_jugador1 == 0:
                    self.bandera_ganar_jugador1 = 1
                    self.sonido_ganar.play()
                if self.meta3.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                if (self.meta3.colliderect(self.jugador1) and self.meta3.colliderect(self.jugador2)):
                    self.musica_fondoNiveles2.stop()
                    self.musica_fondo.play(-1)
                    self.jugarNivel4()
            
            if self.bandera_modo_juego==2:
                 # Actualizar la lógica del juego, movimiento de jugadores, colisiones3, etc.
                # Colisión con límites negros para jugador 2
                for limite in self.limites_negros3:
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

                # Verificar colisiones3 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint3[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint3_jugador2 = 0
                    no_colision_jugador2 = False

                for zona_negra_rect in self.zonas_negras3:
                    if zona_negra_rect.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta3.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint3_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    self.sonido_muerte.play()

                if (self.meta3.colliderect(self.jugador2)):
                    self.sonido_ganar.play()
                    self.jugarNivel4()
        
        self.jugando_nivel = "4"

        # Definir el tiempo inicial (3 minutos en segundos)
        self.initial_time = 120
        self.timer = self.initial_time
        self.start_time = time.time()

        self.musica_fondo.stop()
        self.musica_fondoNiveles.stop()
        self.musica_fondoNiveles2.stop()
        self.musica_fondoNiveles2.play(-1)
        #Importante para que no se guarden las ultimas coordenadas
        #Objeto a mover con teclado
        #Jugador 1 y 2
        self.x_coord = 210
        self.y_coord = 285
        self.x1_coord = 210
        self.y1_coord = 300
        self.bandera_ganar_jugador1 = 0
        self.bandera_ganar_jugador2 = 0

        #Corregir un bug que se queda presionado hacia la izquierda
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0

        while True:
            dibujar_juego3()
            eventos_teclado3()
            colisiones3()
            self.clock.tick(60) 
            pygame.display.flip()

    def jugarNivel4(self):

        def eventos_teclado4():

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.boton14.actualizar(self.screen)
            self.boton14.cambiar_color(pygame.mouse.get_pos())

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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                            self.audio_menu.play()
                            self.menu_dentro_del_nivel()

                
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
            if(self.coord_x8>550 or self.coord_x8<500):
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

        def dibujar_juego4():

            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)
            bandera = True
            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            screen.blit(self.fondo_comic3, (0, 0)) 

            #Zona del contador
            for z in range(0, 900, 1):
                pygame.draw.rect(screen, self.BLACK, (z, 0, 40, 40))
                pygame.draw.rect(screen, self.WHITE, (z, 40, 1, 1))

            # Calcula el tiempo transcurrido desde el inicio
            elapsed_time = time.time() - self.start_time

            # Actualiza el temporizador restando el tiempo transcurrido
            self.timer = max(self.initial_time - int(elapsed_time), 0)


            if self.timer == 0:
                self.pantalla_juego_terminado()
                running = False  # Por ejemplo, terminar el juego
                
            # Limpia la pantalla y muestra el temporizador
            self.contador()
            
            self.checkpoint4 = []
            self.zonas_muerte4 = []
            self.zonas_negras4 = []

            spawn = pygame.draw.rect(screen, self.GREEN_2, (200,275,50,50))
            self.checkpoint4.append(spawn)

            self.meta4 = pygame.draw.rect(screen, self.GREEN, (650,275,50,50))

            

            #Zonas amarillas del mapa
            for z in range(275, 550, 50):
                zona = pygame.Rect(100, z, 100, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)

            for z in range(200, 700, 50):
                zona= pygame.Rect(z, 525, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(600, 750, 50):
                zona= pygame.Rect(z, 475, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(650, 800, 50):
                zona= pygame.Rect(z, 425, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(700, 850, 50):
                zona= pygame.Rect(z, 375, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(750, 850, 50):
                zona= pygame.Rect(z, 325, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(50, 350, 50):
                zona = pygame.Rect(800, z, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(500, 800, 50):
                zona= pygame.Rect(z, 50, 50, 50)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            for z in range(50, 325, 25):
                zona = pygame.Rect(500, z, 100, 25)
                self.zonas_muerte4.append(zona)
                pygame.draw.rect(screen, self.YELLOW, zona)
            
            zona = pygame.Rect(600, 275, 50, 50)
            self.zonas_muerte4.append(zona)
            pygame.draw.rect(screen, self.YELLOW, zona)

            #Zonas de control
            control = pygame.draw.rect(screen, self.GREEN_2, (100,528,100,50))
            self.checkpoint4.append(control)

            control = pygame.draw.rect(screen, self.GREEN_2, (803,325,50,50))
            self.checkpoint4.append(control)
        
            control = pygame.draw.rect(screen, self.GREEN_2, (803,50,50,50))
            self.checkpoint4.append(control)

            if self.bandera_modo_juego==1:
                self.jugador1 = pygame.draw.rect (screen, self.colorAux1, (self.x1_coord, self.y1_coord, 10, 10))
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
            if self.bandera_modo_juego==2:
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
            
            #Zonas obscuras
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x, self.coord_y, 100, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x2, self.coord_y2, 20, 20))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (630, 525, 20, 20))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (650, 475, 50, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (700, 425, 50, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (750, 375, 52, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x4, self.coord_y4, 50, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x5, self.coord_y5, 50, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x6, self.coord_y6, 50, 50))
            self.zonas_negras4.append(plataforma)
        
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x7, self.coord_y7, 100, 50))
            self.zonas_negras4.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x8, self.coord_y8, 130, 50))
            self.zonas_negras4.append(plataforma)

            if self.bandera_modo_juego==1:
                    for limite in self.zonas_negras4:
                        if self.jugador1.colliderect(limite):
                            screen.blit(self.superficie_aura, (self.x1_coord - 2, self.y1_coord - 2))
                        if self.jugador2.colliderect(limite):
                            screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

            if self.bandera_modo_juego==2:
                    for limite in self.zonas_negras4:
                        if self.jugador2.colliderect(limite):
                            screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

            #Creando espacio en el que se podrá jugar
            self.limites_negros4 = []
            
            #Dibujar todo el contorno negro
            for x in range(100, 200, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 575, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])

            for y in range(275, 325, 3):
                borde1 = pygame.Rect(100, y, 3, 3)  
                borde2 = pygame.Rect(250, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(200, 250, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(325, 525, 3):
                borde1 = pygame.Rect(100, y, 3, 3)  
                borde2 = pygame.Rect(200, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(525, 575, 3):
                borde1 = pygame.Rect(100, y, 3, 3)  
                borde2 = pygame.Rect(700, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (100, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(200, 600, 3):
                borde1 = pygame.Rect(x, 525, 3, 3)  
                borde2 = pygame.Rect(x, 575, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (x, 525, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3))
                self.limites_negros4.extend([borde1, borde2])

            for x in range(600, 650, 3):
                borde1 = pygame.Rect(x, 475, 3, 3)  
                borde2 = pygame.Rect(x, 575, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 475, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(650, 700, 3):
                borde1 = pygame.Rect(x, 425, 3, 3)  
                borde2 = pygame.Rect(x, 575, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 425, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 575, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(700, 750, 3):
                borde1 = pygame.Rect(x, 375, 3, 3)  
                borde2 = pygame.Rect(x, 525, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (x, 375, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 525, 3, 3))  
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(750, 800, 3):
                borde1 = pygame.Rect(x, 325, 3, 3)  
                borde2 = pygame.Rect(x, 475, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 475, 3, 3))  
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(800, 850, 3):
                borde1 = pygame.Rect(x, 50, 3, 3)  
                borde2 = pygame.Rect(x, 425, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 425, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(475, 525, 3):
                borde1 = pygame.Rect(600, y, 3, 3)  
                borde2 = pygame.Rect(750, y, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (600, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (750, y, 3, 3))  
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(425, 475, 3):
                borde1 = pygame.Rect(650, y, 3, 3)  
                borde2 = pygame.Rect(800, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(375, 425, 3):
                borde1 = pygame.Rect(700, y, 3, 3)  
                borde2 = pygame.Rect(850, y, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3))  
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(325, 375, 3):
                borde1 = pygame.Rect(750, y, 3, 3)  
                borde2 = pygame.Rect(850, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (750, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(50, 325, 3):
                borde1 = pygame.Rect(500, y, 3, 3)  
                borde2 = pygame.Rect(850, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (850, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(100, 275, 3):
                borde1 = pygame.Rect(600, y, 3, 3)  
                borde2 = pygame.Rect(800, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (600, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for y in range(275, 325, 3):
                borde1 = pygame.Rect(700, y, 3, 3)  
                borde2 = pygame.Rect(800, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (800, y, 3, 3)) 
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(700, 800, 3):
                borde1 = pygame.Rect(x, 50, 3, 3)  
                borde2 = pygame.Rect(x, 100, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 100, 3, 3))  
                self.limites_negros4.extend([borde1, borde2])
            
            for x in range(600, 700, 3):
                borde1 = pygame.Rect(x, 50, 3, 3)  
                borde2 = pygame.Rect(x, 100, 3, 3) 
                borde3 = pygame.Rect(x, 275, 3, 3)  
                borde4 = pygame.Rect(x, 325, 3, 3)
                pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 100, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))  
                self.limites_negros4.extend([borde1, borde2, borde3, borde4])
            
            for x in range(500, 600, 3):
                borde1 = pygame.Rect(x, 50, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (x, 50, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3))
                self.limites_negros4.extend([borde1, borde2])
            
            #Correción de bug de dibujo
            zona= pygame.Rect(800, 325, 3, 3)
            self.zonas_muerte4.append(zona)
            pygame.draw.rect(screen, self.BLACK, zona)

            zona= pygame.Rect(600, 525, 3, 3)
            self.zonas_muerte4.append(zona)
            pygame.draw.rect(screen, self.BLACK, zona)
            
        def colisiones4():

            if self.bandera_modo_juego==1:
                # Actualizar la lógica del juego, movimiento de jugadores, colisiones4, etc.
                # Colisión con límites negros para jugador 1
                for limite in self.limites_negros4:
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
                for limite in self.limites_negros4:
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
                
                # Verificar colisiones4 con los checkpoints
                if self.checkpoint4[0].colliderect(self.jugador1):
                    self.ultimo_checkpoint4_jugador1 = 0
                    no_colision_jugador1 = False
                
                if self.checkpoint4[1].colliderect(self.jugador1):
                    self.ultimo_checkpoint4_jugador1 = 1
                    no_colision_jugador1 = False
                
                if self.checkpoint4[2].colliderect(self.jugador1):
                    self.ultimo_checkpoint4_jugador1 = 2
                    no_colision_jugador1 = False
                
                if self.checkpoint4[3].colliderect(self.jugador1):
                    self.ultimo_checkpoint4_jugador1 = 3
                    no_colision_jugador1 = False

                # Verificar colisiones4 con las zonas negras
                for zona_negra_rect in self.zonas_negras4:
                    if zona_negra_rect.colliderect(self.jugador1):
                        no_colision_jugador1 = False
                        break  # Si hay una colisión, no es necesario seguir verificando

                # Verificar colisiones4 con la meta
                if self.meta4.colliderect(self.jugador1):
                    no_colision_jugador1 = False

                # Si no hubo colisiones4 con ningún elemento
                if no_colision_jugador1:
                    if self.ultimo_checkpoint4_jugador1 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x1_coord = 220
                        self.y1_coord = 285
                    if self.ultimo_checkpoint4_jugador1 == 1:
                        self.x1_coord = 150
                        self.y1_coord = 540
                    if self.ultimo_checkpoint4_jugador1 == 2:
                        self.x1_coord = 820
                        self.y1_coord = 350
                    if self.ultimo_checkpoint4_jugador1 == 3:
                        self.x1_coord = 820
                        self.y1_coord = 70
                    self.sonido_muerte.play()

                # Verificar colisiones4 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint4[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 0
                    no_colision_jugador2 = False
                
                if self.checkpoint4[1].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 1
                    no_colision_jugador2 = False
                
                if self.checkpoint4[2].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 2
                    no_colision_jugador2 = False
                
                if self.checkpoint4[3].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 3
                    no_colision_jugador2 = False

                for zona_negra_rect in self.zonas_negras4:
                    if zona_negra_rect.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta4.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint4_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    if self.ultimo_checkpoint4_jugador2 == 1:
                        self.x_coord = 150
                        self.y_coord = 540
                    if self.ultimo_checkpoint4_jugador2 == 2:
                        self.x_coord = 820
                        self.y_coord = 350
                    if self.ultimo_checkpoint4_jugador2 == 3:
                        self.x_coord = 820
                        self.y_coord = 70
                    self.sonido_muerte.play()
                
                if self.meta4.colliderect(self.jugador1) and self.bandera_ganar_jugador1 == 0:
                    self.bandera_ganar_jugador1 = 1
                    self.sonido_ganar.play()
                if self.meta4.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                if (self.meta4.colliderect(self.jugador1) and self.meta4.colliderect(self.jugador2)):
                    self.sonido_ganar.play()
                    self.musica_fondoNiveles3.stop()
                    self.musica_fondo.play(-1)
                    self.jugarNivel5()

            if self.bandera_modo_juego==2:

                # Colisión con límites negros para jugador 2
                for limite in self.limites_negros4:
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

                # Verificar colisiones4 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint4[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 0
                    no_colision_jugador2 = False
                
                if self.checkpoint4[1].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 1
                    no_colision_jugador2 = False
                
                if self.checkpoint4[2].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 2
                    no_colision_jugador2 = False
                
                if self.checkpoint4[3].colliderect(self.jugador2):
                    self.ultimo_checkpoint4_jugador2 = 3
                    no_colision_jugador2 = False

                for zona_negra_rect in self.zonas_negras4:
                    if zona_negra_rect.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta4.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint4_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    if self.ultimo_checkpoint4_jugador2 == 1:
                        self.x_coord = 150
                        self.y_coord = 540
                    if self.ultimo_checkpoint4_jugador2 == 2:
                        self.x_coord = 820
                        self.y_coord = 350
                    if self.ultimo_checkpoint4_jugador2 == 3:
                        self.x_coord = 820
                        self.y_coord = 70
                    self.sonido_muerte.play()
                
                if self.meta4.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                    self.musica_fondoNiveles3.stop()
                    self.musica_fondo.play(-1)
                    self.jugarNivel5()
        
        self.jugando_nivel = "3"

        # Definir el tiempo inicial (3 minutos en segundos)
        self.initial_time = 120
        self.timer = self.initial_time
        self.start_time = time.time()

        self.musica_fondo.stop()
        self.musica_fondoNiveles2.stop()
        self.musica_fondoNiveles3.stop()
        self.musica_fondoNiveles3.play(-1)
        #Importante para que no se guarden las ultimas coordenadas
        #Objeto a mover con teclado
        #Jugador 1 y 2
        self.x_coord = 210
        self.y_coord = 285
        self.x1_coord = 210
        self.y1_coord = 300
        self.bandera_ganar_jugador1 = 0
        self.bandera_ganar_jugador2 = 0

        #Corregir un bug que se queda presionado hacia la izquierda
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0

        while True:
            dibujar_juego4()
            eventos_teclado4()
            colisiones4()
            self.clock.tick(60) 
            pygame.display.flip()

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_dentro_del_nivel()
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.boton14.actualizar(self.screen)
            self.boton14.cambiar_color(pygame.mouse.get_pos())
                
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
            pygame.mouse.set_visible(1)

            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            screen.blit(self.fondo_comic, (0, 0)) 
            
            self.checkpoint2 = []
            self.zonas_muerte2 = []
            self.zonas_negras2 = []

            spawn = pygame.draw.rect(screen, self.GREEN_2, (200,278,53,49))
            self.checkpoint2.append(spawn)

            self.meta2 = pygame.draw.rect(screen, self.GREEN, (650,275,50,50))
            
            #Zona del contador
            for z in range(0, 900, 1):
                pygame.draw.rect(screen, self.BLACK, (z, 0, 40, 40))
                pygame.draw.rect(screen, self.WHITE, (z, 40, 1, 1))
            
            # Calcula el tiempo transcurrido desde el inicio
            elapsed_time = time.time() - self.start_time

            # Actualiza el temporizador restando el tiempo transcurrido
            self.timer = max(self.initial_time - int(elapsed_time), 0)

            if self.timer == 0:
                self.pantalla_juego_terminado()
                
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
            if self.bandera_modo_juego==1:
                self.jugador1 = pygame.draw.rect (screen, self.colorAux1, (self.x1_coord, self.y1_coord, 10, 10))
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
            if self.bandera_modo_juego==2:
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
           
            #Zonas negras
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x9, self.coord_y9, 50, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x10, self.coord_y10, 50, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (350, 275, 53, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (500, 275, 53, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x11, self.coord_y11, 50, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x12, self.coord_y12, 50, 50))
            self.zonas_negras2.append(plataforma)

            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x13, self.coord_y13, 50, 50))
            self.zonas_negras2.append(plataforma)
        
            plataforma = pygame.draw.rect(screen, self.BLACK, (self.coord_x14, self.coord_y14, 50, 50))
            self.zonas_negras2.append(plataforma)

            if self.bandera_modo_juego==1:
                for limite in self.zonas_negras2:
                    if self.jugador1.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x1_coord - 2, self.y1_coord - 2))
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

            if self.bandera_modo_juego==2:
                for limite in self.zonas_negras2:
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2)) 

            #Creando espacio en el que se podrá jugar
            self.limites_negros2 = []
            
            #Dibujar todo el contorno negro
            for x in range(250, 350, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])

            for x in range(400, 500, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for x in range(550, 650, 3):
                borde1 = pygame.Rect(x, 150, 3, 3)  
                borde2 = pygame.Rect(x, 450, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 150, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 450, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for x in range(350, 400, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for x in range(500, 550, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for x in range(650, 700, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])

            for y in range(275, 325, 3):
                borde1 = pygame.Rect(200, y, 3, 3)  
                borde2 = pygame.Rect(700, y, 3, 3)  
                pygame.draw.rect(screen, self.BLACK, (200, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (700, y, 3, 3))
                self.limites_negros2.extend([borde1, borde2])
            
            for x in range(200, 250, 3):
                borde1 = pygame.Rect(x, 275, 3, 3)  
                borde2 = pygame.Rect(x, 325, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (x, 275, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (x, 325, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (350, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(400, y, 3, 3)  
                borde2 = pygame.Rect(500, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (400, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(150, 275, 3):
                borde1 = pygame.Rect(550, y, 3, 3)  
                borde2 = pygame.Rect(650, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (550, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(250, y, 3, 3)  
                borde2 = pygame.Rect(350, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (250, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (350, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(400, y, 3, 3)  
                borde2 = pygame.Rect(500, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (400, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (500, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
            for y in range(325, 450, 3):
                borde1 = pygame.Rect(550, y, 3, 3)  
                borde2 = pygame.Rect(650, y, 3, 3) 
                pygame.draw.rect(screen, self.BLACK, (550, y, 3, 3))
                pygame.draw.rect(screen, self.BLACK, (650, y, 3, 3)) 
                self.limites_negros2.extend([borde1, borde2])
            
        def colisiones2():

            if self.bandera_modo_juego==1:
                # Actualizar la lógica del juego, movimiento de jugadores, colisiones2, etc.
                # Colisión con límites negros para jugador 1
                for limite2 in self.limites_negros2:
                    if self.jugador1.colliderect(limite2):
                        if self.x1_speed > 0 and limite2.left <= self.jugador1.right:
                            self.x1_speed = 0
                            self.x1_coord = limite2.left - self.jugador1.width
                        elif self.x1_speed < 0 and limite2.right >= self.jugador1.left:
                            self.x1_speed = 0
                            self.x1_coord = limite2.right
                        if self.y1_speed > 0 and limite2.top <= self.jugador1.bottom:
                            self.y1_speed = 0
                            self.y1_coord = limite2.top - self.jugador1.height
                        elif self.y1_speed < 0 and limite2.bottom >= self.jugador1.top:
                            self.y1_speed = 0
                            self.y1_coord = limite2.bottom

                # Colisión con límites negros para jugador 2
                for limite2 in self.limites_negros2:
                    if self.jugador2.colliderect(limite2):
                        if self.x_speed > 0 and limite2.left <= self.jugador2.right:
                            self.x_speed = 0
                            self.x_coord = limite2.left - self.jugador2.width
                        elif self.x_speed < 0 and limite2.right >= self.jugador2.left:
                            self.x_speed = 0
                            self.x_coord = limite2.right
                        if self.y_speed > 0 and limite2.top <= self.jugador2.bottom:
                            self.y_speed = 0
                            self.y_coord = limite2.top - self.jugador2.height
                        elif self.y_speed < 0 and limite2.bottom >= self.jugador2.top:
                            self.y_speed = 0
                            self.y_coord = limite2.bottom

                # Colisión entre jugadores
                if self.jugador1.colliderect(self.jugador2):
                    # Calcula el vector entre los dos jugadores
                    self.dx2 = self.x1_coord - self.x_coord
                    self.dy2 = self.y1_coord - self.y_coord
                    self.distancia2 = math.sqrt(self.dx2 ** 2 + self.dy2 ** 2)
                
                    # Calcula el vector de separación mínimo (evita la división por cero)
                    if self.distancia2 != 0:
                        overlap2 = (self.jugador1.width + self.jugador2.width) - self.distancia2
                        self.dx2 /= self.distancia2
                        self.dy2 /= self.distancia2
                    else:
                        overlap2 = 1.0
                
                    # Ajusta las posiciones para evitar la superposición
                    self.x1_coord += self.dx2 * (overlap2 / 2)
                    self.y1_coord += self.dy2 * (overlap2 / 2)
                    self.x_coord -= self.dx2 * (overlap2 / 2)
                    self.y_coord -= self.dy2 * (overlap2 / 2)
                
                    # Detiene a ambos jugadores
                    self.x1_speed = 0
                    self.y1_speed = 0
                    self.x_speed = 0
                    self.y_speed = 0
                
                # Verificar si los jugadores están tocando "spawn," "meta" o "zona_negra"
                no_colision_jugador1 = True  # Suponemos que no hay colisión inicialmente
                
                # Verificar colisiones2 con los checkpoints
                if self.checkpoint2[0].colliderect(self.jugador1):
                    self.ultimo_checkpoint_jugador1 = 0
                    no_colision_jugador1 = False

                # Verificar colisiones2 con las zonas negras
                for zona_negra_rect2 in self.zonas_negras2:
                    if zona_negra_rect2.colliderect(self.jugador1):
                        no_colision_jugador1 = False
                        break

                # Verificar colisiones2 con la meta
                if self.meta2.colliderect(self.jugador1):
                    no_colision_jugador1 = False

                # Si no hubo colisiones2 con ningún elemento
                if no_colision_jugador1:
                    if self.ultimo_checkpoint_jugador1 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x1_coord = 220
                        self.y1_coord = 285
                    self.sonido_muerte.play()

                # Verificar colisiones2 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint2[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint2_jugador2 = 0
                    no_colision_jugador2 = False

                for zona_negra_rect2 in self.zonas_negras2:
                    if zona_negra_rect2.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta2.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint2_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    self.sonido_muerte.play()

                if self.meta2.colliderect(self.jugador1) and self.bandera_ganar_jugador1 == 0:
                    self.bandera_ganar_jugador1 = 1
                    self.sonido_ganar.play()
                if self.meta2.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                if (self.meta2.colliderect(self.jugador1) and self.meta2.colliderect(self.jugador2)):
                    self.jugarNivel3()
            
            if self.bandera_modo_juego==2:
                # Colisión con límites negros para jugador 2
                for limite in self.limites_negros2:
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

                # Verificar colisiones4 para el jugador 2 (puedes repetir el mismo proceso)
                no_colision_jugador2 = True

                if self.checkpoint2[0].colliderect(self.jugador2):
                    self.ultimo_checkpoint2_jugador2 = 0
                    no_colision_jugador2 = False

                for zona_negra_rect in self.zonas_negras2:
                    if zona_negra_rect.colliderect(self.jugador2):
                        no_colision_jugador2 = False
                        break

                if self.meta2.colliderect(self.jugador2):
                    no_colision_jugador2 = False

                if no_colision_jugador2:
                    if self.ultimo_checkpoint2_jugador2 == 0:
                        # Si no ha tocado ningún punto de control, puedes establecer coordenadas predeterminadas
                        self.x_coord = 220
                        self.y_coord = 285
                    self.sonido_muerte.play()
                
                if self.meta2.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                    self.musica_fondoNiveles.stop()
                    self.musica_fondo.play(-1)
                    self.jugarNivel3()

        self.jugando_nivel = "2"

        # Definir el tiempo inicial (3 minutos en segundos)
        self.initial_time = 120
        self.timer = self.initial_time
        self.start_time = time.time()

        self.musica_fondo.stop()
        self.musica_fondoTutorial.stop()
        self.musica_fondoNiveles.stop()
        self.musica_fondoNiveles.play(-1)
        #Importante para que no se guarden las ultimas coordenadas
        #Objeto a mover con teclado
        #Jugador 1 y 2
        self.x_coord = 210
        self.y_coord = 285
        self.x1_coord = 210
        self.y1_coord = 300
        self.bandera_ganar_jugador1 = 0
        self.bandera_ganar_jugador2 = 0

        #Corregir un bug que se queda presionado hacia la izquierda
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0

        
        while True:
            dibujar_juego2()
            eventos_teclado2()
            colisiones2()
            self.clock.tick(60) 
            pygame.display.flip()
    
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
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_dentro_del_nivel()
            
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.boton14.actualizar(self.screen)
            self.boton14.cambiar_color(pygame.mouse.get_pos())

                
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
            pygame.mouse.set_visible(1)

            # Dibujar elementos del juego en la pantalla
            #Color de fondo
            screen.fill(self.GREY)
            screen.blit(self.fondo_comic4, (0, 0)) 
            
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
            self.timer = max(self.initial_time5 - int(elapsed_time), 0)

            if self.timer == 0:
                self.pantalla_juego_terminado()
                
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
            if self.bandera_modo_juego==1:
                self.jugador1 = pygame.draw.rect (screen, self.colorAux1, (self.x1_coord, self.y1_coord, 10, 10))
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
            if self.bandera_modo_juego==2:
                self.jugador2 = pygame.draw.rect (screen, self.colorAux2, (self.x_coord, self.y_coord, 10, 10))
           
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

            if self.bandera_modo_juego==1:
                for limite in self.zonas_negra5:
                    if self.jugador1.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x1_coord - 2, self.y1_coord - 2))
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

            if self.bandera_modo_juego==2:
                for limite in self.zonas_negra5:
                    if self.jugador2.colliderect(limite):
                        screen.blit(self.superficie_aura, (self.x_coord - 2, self.y_coord - 2))

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
            if self.bandera_modo_juego==1:
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

                if self.meta5.colliderect(self.jugador1) and self.bandera_ganar_jugador1 == 0:
                    self.bandera_ganar_jugador1 = 1
                    self.sonido_ganar.play()
                if self.meta5.colliderect(self.jugador2) and self.bandera_ganar_jugador2 == 0:
                    self.bandera_ganar_jugador2 = 1
                    self.sonido_ganar.play()
                if (self.meta5.colliderect(self.jugador1) and self.meta5.colliderect(self.jugador2)):
                    self.musica_fondoNiveles4.stop()
                    self.musica_fondo.play(-1)
                    self.menu_principal()
            
            if self.bandera_modo_juego==2:
                # Actualizar la lógica del juego, movimiento de jugadores, colisiones5, etc.
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

                if (self.meta5.colliderect(self.jugador2)):
                    self.sonido_ganar.play()
                    self.menu_principal()
        
        self.jugando_nivel = "5"

        # Definir el tiempo inicial (3 minutos en segundos)
        self.initial_time5 = 240
        self.timer = self.initial_time5
        self.start_time = time.time()

        self.musica_fondo.stop()
        self.musica_fondoNiveles3.stop()
        self.musica_fondoNiveles4.stop()
        self.musica_fondoNiveles4.play(-1)
        #Importante para que no se guarden las ultimas coordenadas
        #Objeto a mover con teclado
        #Jugador 1 y 2
        self.x_coord = 210
        self.y_coord = 285
        self.x1_coord = 210
        self.y1_coord = 300
        self.bandera_ganar_jugador1 = 0
        self.bandera_ganar_jugador2 = 0

        #Corregir un bug que se queda presionado hacia la izquierda
        self.x_speed = 0
        self.y_speed = 0
        self.x1_speed = 0
        self.y1_speed = 0

        while True:
            dibujar_juego5()
            eventos_teclado5()
            colisiones5()
            self.clock.tick(60) 
            pygame.display.flip()

    def nivelUno(self):
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            pygame.mouse.set_visible(1)
            screen.blit(self.fondo_tutorial7, (0, 0))

            self.angulo_estrella += 0.03
            self.multiplicador_de_medida_estrella = 0.6 + 0.5 * math.sin(self.angulo_estrella)
            vertices_octagono = self.dibujar_octagono(450, 330, 30)
            pygame.draw.polygon(screen, self.BLACK, vertices_octagono, width=3)
            vertices_octagono = self.dibujar_octagono(450, 330, 29)
            pygame.draw.polygon(screen, self.YELLOW_MONEDA, vertices_octagono)
            self.dibujar_estrella(screen, 450, 330, int(self.medida_base_estrella * self.multiplicador_de_medida_estrella), self.angulo_estrella)

            self.boton8.cambiar_color(self.MENU_MOUSE_POS)
            self.boton8.actualizar(screen)
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton8.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.jugarNivel2()

            pygame.display.update()
    
    def opciones(self):
        while True:
            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            screen.blit(self.fondo_Opciones, (0, 0))

            self.boton4.cambiar_color(self.MENU_MOUSE_POS)
            self.boton4.actualizar(screen)

            self.boton9.cambiar_color(self.MENU_MOUSE_POS)
            self.boton9.actualizar(screen)

            self.boton10.cambiar_color(self.MENU_MOUSE_POS)
            self.boton10.actualizar(screen)

            self.boton11.cambiar_color(self.MENU_MOUSE_POS)
            self.boton11.actualizar(screen)


            for event in pygame.event.get():
                # Condiciones para moverse entre los menus
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton4.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_principal()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton9.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.sonido()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton11.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.creditos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton10.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.personalizar()
                

            # Actualizar la pantalla
            pygame.display.update()
 
    def sonido(self):
        ventana=Tk()
        ventana.title("HiCube")
        ventana.iconbitmap("Imagenes/Icono.ico")

        # Obtener el ancho y alto de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Definir el tamaño de la ventana
        ventana_width = 500
        ventana_height = 270

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - ventana_width) // 2
        y = (screen_height - ventana_height) // 2

        # Establecer la geometría de la ventana
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

        #Color de fondo
        color_hex = '#{0:02X}{1:02X}{2:02X}'.format(*self.GREY)
        color_hex2 = '#{0:02X}{1:02X}{2:02X}'.format(*self.YELLOW)
        color_hex3 = '#{0:02X}{1:02X}{2:02X}'.format(*self.BLUE)
        color_hex4 = '#{0:02X}{1:02X}{2:02X}'.format(*self.RED)
        #Color_hex transforma mi color de RGB a Hexadecimal
        ventana.configure(bg=color_hex)

        # Texto para la primera barra
        etiqueta0 = Label(ventana, text="VOLUMEN", fg="white", bg=color_hex, font=("cambria", 16))
        etiqueta0.place(x=200, y=30)

        # Agregar una barra deslizante para ajustar el volumen
        self.volumen = Scale(ventana, from_=0, to=100, orient="horizontal", length=200, showvalue=0)
        self.volumen.set(self.volumenPrincipal)  # Establecer el valor inicial del volumen
        self.volumen.place(x=250, y=82)
        self.volumen.configure(highlightbackground=color_hex2, bg=color_hex, troughcolor="white")

        # Vincular una función de controlador al evento "Motion" (movimiento) del slider
        self.volumen.bind("<Motion>", self.obtener_valor_volumen)

        # Texto para la primera barra
        etiqueta1 = Label(ventana, text="VOLUMEN PRINCIPAL", fg="white", bg=color_hex, font=("cambria", 14))
        etiqueta1.place(x=30, y=80)

        # Agregar una segunda barra deslizante para ajustar el volumen
        self.volumen2 = Scale(ventana, from_=0, to=100, orient="horizontal", length=200, showvalue=0)
        self.volumen2.set(self.volumenMusica)  # Establecer el valor inicial del volumen
        self.volumen2.place(x=250, y=132)
        self.volumen2.configure(highlightbackground=color_hex3, bg=color_hex, troughcolor="white")

        # Vincular una función de controlador al evento "Motion" (movimiento) del slider
        self.volumen2.bind("<Motion>", self.obtener_valor_volumen2)

        # Texto para la segunda barra
        etiqueta2 = Label(ventana, text="VOLUMEN DE LA MÚSICA", fg="white", bg=color_hex, font=("cambria", 14))
        etiqueta2.place(x=30, y=130)

        # Agregar una segunda barra deslizante para ajustar el volumen
        self.volumen3 = Scale(ventana, from_=0, to=100, orient="horizontal", length=200, showvalue=0)
        self.volumen3.set(self.volumenEfectos)  # Establecer el valor inicial del volumen
        self.volumen3.place(x=250, y=182)
        self.volumen3.configure(highlightbackground=color_hex4, bg=color_hex, troughcolor="white")

        # Vincular una función de controlador al evento "Motion" (movimiento) del slider
        self.volumen3.bind("<Motion>", self.obtener_valor_volumen3)

        # Texto para la segunda barra
        etiqueta3 = Label(ventana, text="EFECTOS DE SONIDO", fg="white", bg=color_hex, font=("cambria", 14))
        etiqueta3.place(x=30, y=180)

        ventana.mainloop()
    
    def obtener_valor_volumen(self, event):
        self.volumenPrincipal = self.volumen.get()
        if self.volumenPrincipal == 0:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0)
            self.sonido_ganar.set_volume(0)
            self.musica_fondo.set_volume(0)
            self.musica_fondoNiveles.set_volume(0)
            self.musica_fondoNiveles2.set_volume(0)
            self.musica_fondoNiveles3.set_volume(0)
            self.musica_fondoNiveles4.set_volume(0)
            self.audio_menu.set_volume(0)
            self.musica_fondoTutorial.set_volume(0)
        if self.volumenPrincipal == 10:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.1)
            self.sonido_ganar.set_volume(0.1)
            self.musica_fondo.set_volume(0.1)
            self.musica_fondoNiveles.set_volume(0.1)
            self.musica_fondoNiveles2.set_volume(0.1)
            self.musica_fondoNiveles3.set_volume(0.1)
            self.musica_fondoNiveles4.set_volume(0.1)
            self.musica_fondoTutorial.set_volume(0.1)
            self.audio_menu.set_volume(0.1)
        if self.volumenPrincipal == 20:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.2)
            self.sonido_ganar.set_volume(0.1)
            self.musica_fondo.set_volume(0.2)
            self.musica_fondoNiveles.set_volume(0.2)
            self.musica_fondoNiveles2.set_volume(0.2)
            self.musica_fondoNiveles3.set_volume(0.2)
            self.musica_fondoNiveles4.set_volume(0.2)
            self.musica_fondoTutorial.set_volume(0.2)
            self.audio_menu.set_volume(0.1)
        if self.volumenPrincipal == 30:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.3)
            self.sonido_ganar.set_volume(0.1)
            self.musica_fondo.set_volume(0.3)
            self.musica_fondoNiveles.set_volume(0.3)
            self.musica_fondoNiveles2.set_volume(0.3)
            self.musica_fondoNiveles3.set_volume(0.3)
            self.musica_fondoNiveles4.set_volume(0.3)
            self.musica_fondoTutorial.set_volume(0.3)
            self.audio_menu.set_volume(0.1)
        if self.volumenPrincipal == 40:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.4)
            self.sonido_ganar.set_volume(0.2)
            self.musica_fondo.set_volume(0.4)
            self.musica_fondoNiveles.set_volume(0.4)
            self.musica_fondoNiveles2.set_volume(0.4)
            self.musica_fondoNiveles3.set_volume(0.4)
            self.musica_fondoNiveles4.set_volume(0.4)
            self.musica_fondoTutorial.set_volume(0.4)
            self.audio_menu.set_volume(0.1)
        if self.volumenPrincipal == 50:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.5)
            self.sonido_ganar.set_volume(0.2)
            self.musica_fondo.set_volume(0.5)
            self.musica_fondoNiveles.set_volume(0.5)
            self.musica_fondoNiveles2.set_volume(0.5)
            self.musica_fondoNiveles3.set_volume(0.5)
            self.musica_fondoNiveles4.set_volume(0.5)
            self.musica_fondoTutorial.set_volume(0.5)
            self.audio_menu.set_volume(0.1)
        if self.volumenPrincipal == 60:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.6)
            self.sonido_ganar.set_volume(0.3)
            self.musica_fondo.set_volume(0.6)
            self.musica_fondoNiveles.set_volume(0.6)
            self.musica_fondoNiveles2.set_volume(0.6)
            self.musica_fondoNiveles3.set_volume(0.6)
            self.musica_fondoNiveles4.set_volume(0.6)
            self.musica_fondoTutorial.set_volume(0.6)
            self.audio_menu.set_volume(0.2)
        if self.volumenPrincipal == 70:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.7)
            self.sonido_ganar.set_volume(0.3)
            self.musica_fondo.set_volume(0.7)
            self.musica_fondoNiveles.set_volume(0.7)
            self.musica_fondoNiveles2.set_volume(0.7)
            self.musica_fondoNiveles3.set_volume(0.7)
            self.musica_fondoNiveles4.set_volume(0.7)
            self.musica_fondoTutorial.set_volume(0.7)
            self.audio_menu.set_volume(0.2)
        if self.volumenPrincipal == 80:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.8)
            self.sonido_ganar.set_volume(0.4)
            self.musica_fondo.set_volume(0.8)
            self.musica_fondoNiveles.set_volume(0.8)
            self.musica_fondoNiveles2.set_volume(0.8)
            self.musica_fondoNiveles3.set_volume(0.8)
            self.musica_fondoNiveles4.set_volume(0.8)
            self.audio_menu.set_volume(0.3)
            self.musica_fondoTutorial.set_volume(0.8)
        if self.volumenPrincipal == 90:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.9)
            self.sonido_ganar.set_volume(0.4)
            self.musica_fondo.set_volume(0.9)
            self.musica_fondoNiveles.set_volume(0.9)
            self.musica_fondoNiveles2.set_volume(0.9)
            self.musica_fondoNiveles3.set_volume(0.9)
            self.musica_fondoNiveles4.set_volume(0.9)
            self.audio_menu.set_volume(0.3)
            self.musica_fondoTutorial.set_volume(0.9)
        if self.volumenPrincipal == 100:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.99)
            self.sonido_ganar.set_volume(0.5)
            self.musica_fondo.set_volume(0.99)
            self.musica_fondoNiveles.set_volume(0.99)
            self.musica_fondoNiveles2.set_volume(0.99)
            self.musica_fondoNiveles3.set_volume(0.99)
            self.musica_fondoNiveles4.set_volume(0.99)
            self.audio_menu.set_volume(0.4)
            self.musica_fondoTutorial.set_volume(0.99)
    
    def obtener_valor_volumen2(self, event):
        self.volumenMusica = self.volumen2.get()
        self.musica_fondo.set_volume(self.volumenMusica/100)
        self.musica_fondoNiveles.set_volume(self.volumenMusica/100)
        self.musica_fondoNiveles2.set_volume(self.volumenMusica/100)
        self.musica_fondoNiveles3.set_volume(self.volumenMusica/100)
        self.musica_fondoNiveles4.set_volume(self.volumenMusica/100)
        self.musica_fondoTutorial.set_volume(self.volumenMusica/100)

    def obtener_valor_volumen3(self, event):
        self.volumenEfectos = self.volumen3.get()
        if self.volumenEfectos == 0:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0)
            self.sonido_ganar.set_volume(0)
            self.audio_menu.set_volume(0)
        if self.volumenEfectos == 10:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.1)
            self.sonido_ganar.set_volume(0.1)
            self.audio_menu.set_volume(0.1)
        if self.volumenEfectos == 20:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.2)
            self.sonido_ganar.set_volume(0.1)
            self.audio_menu.set_volume(0.1)
        if self.volumenEfectos == 30:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.3)
            self.sonido_ganar.set_volume(0.1)
            self.audio_menu.set_volume(0.1)
        if self.volumenEfectos == 40:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.4)
            self.sonido_ganar.set_volume(0.2)
            self.audio_menu.set_volume(0.1)
        if self.volumenEfectos == 50:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.5)
            self.sonido_ganar.set_volume(0.2)
            self.audio_menu.set_volume(0.1)
        if self.volumenEfectos == 60:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.6)
            self.sonido_ganar.set_volume(0.3)
            self.audio_menu.set_volume(0.2)
        if self.volumenEfectos == 70:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.7)
            self.sonido_ganar.set_volume(0.3)
            self.audio_menu.set_volume(0.2)
        if self.volumenEfectos == 80:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.8)
            self.sonido_ganar.set_volume(0.4)
            self.audio_menu.set_volume(0.3)
        if self.volumenEfectos == 90:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.9)
            self.sonido_ganar.set_volume(0.4)
            self.audio_menu.set_volume(0.3)
        if self.volumenEfectos == 100:
             #Definicion de sonidos
            self.sonido_muerte.set_volume(0.99)
            self.sonido_ganar.set_volume(0.5)
            self.audio_menu.set_volume(0.4)

    def creditos(self):
        #Hacer visible/invisible el mouse
        pygame.mouse.set_visible(1)
        

        #Creditos
        creditosTexto = [
            "Desarrollado por:",
            "Josué Sánchez Domínguez",
            "",
            "Gracias por jugar",
        ]

        #Coordenadas
        coord_xCreditos = 0
        coord_yCreditos = 0
        coord_xCreditos2 = 880
        coord_yCreditos2 = 580

        #Velocidad de animacion
        speed_xCreditos = 0.5
        speed_yCreditos = 0.5
        speed_xCreditos2 = 0.5
        speed_yCreditos2 = 0.5
        
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            #Color de fondo
            screen.fill(self.BLACK)

            #Zona de dibujo
            pygame.draw.rect(screen, self.RED, (coord_xCreditos, coord_yCreditos, 30, 30))
            pygame.draw.rect(screen, self.BLUE, (coord_xCreditos2, coord_yCreditos2, 30, 30))
            y_pos = 220  # Posición vertical inicial para los créditos

            for line in creditosTexto:
                text_surface = fuente.render(line, True, "white")
                text_rect = text_surface.get_rect(center=(size[0] // 2, y_pos))
                screen.blit(text_surface, text_rect)
                y_pos += 40  # Espacio vertical entre las líneas de crédito

            #Hacer que permanezca siempre en pantalla dentro de los limites
            if(coord_xCreditos>880 or coord_xCreditos<0):
                speed_xCreditos *= -1
            if(coord_yCreditos>580 or coord_yCreditos<0):
                speed_yCreditos *= -1
            if(coord_xCreditos2>880 or coord_xCreditos2<0):
                speed_xCreditos2 *= -1
            if(coord_yCreditos2>580 or coord_yCreditos2<0):
                speed_yCreditos2 *= -1
                
            #Inicio de la animación
            coord_xCreditos += speed_xCreditos
            coord_yCreditos += speed_yCreditos
            coord_xCreditos2 += speed_xCreditos2
            coord_yCreditos2 += speed_yCreditos2

            self.boton12.cambiar_color(self.MENU_MOUSE_POS)
            self.boton12.actualizar(screen)

            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton12.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.menu_principal()
                        
            #Actualizar pantalla
            pygame.display.flip()
    
    def personalizar(self):
        bandera = 0
        lista_coord_lluvia = []
        for i in range (60):
                x = random.randint(0, 900)
                y = random.randint(0, 600)
                lista_coord_lluvia.append([x,y])

        #Hacer visible/invisible el mouse
        pygame.mouse.set_visible(1)

        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            #Color de fondo
            screen.fill(self.BLACK)
            #LLUVIA
            for j in lista_coord_lluvia:
                pygame.draw.circle(screen, self.WHITE, j, 1)
                j[1] += 1
                if j[1] > 600:
                    j[1] = 0

            texto = fuente_grande.render("Color", True, self.WHITE)
            screen.blit(texto, (395, 100))  # (100, 100) son las coordenadas donde se mostrará el texto
            texto = fuente.render("Jugador 1", True, self.WHITE)
            screen.blit(texto, (150, 340))
            texto = fuente.render("Jugador 2", True, self.WHITE)
            screen.blit(texto, (650, 340))


            #Opcion de colores
            color1 = pygame.draw.rect (screen, self.ORANGE, (425, 200, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (425 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
            color2 = pygame.draw.rect (screen, self.RED, (475, 200, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (475 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
            color3 = pygame.draw.rect (screen, self.BLUE, (375, 200, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (375 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
            color4 = pygame.draw.rect (screen, self.MOSTAZA, (425, 250, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (425 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
            color5 = pygame.draw.rect (screen, self.AQUA, (475, 250, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (475 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
            color6 = pygame.draw.rect (screen, self.BLUE2, (375, 250, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (375 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
            color7 = pygame.draw.rect (screen, self.PURPLE, (425, 300, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (425 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
            color8 = pygame.draw.rect (screen, self.FIUSHA, (475, 300, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (475 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
            color9 = pygame.draw.rect (screen, self.RED2, (375, 300, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (375 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
            color10 = pygame.draw.rect (screen, self.PINK, (425, 350, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (425 - 1, 350 - 1, 30 + 2, 30 + 2), 2)
            color11 = pygame.draw.rect (screen, self.BROWN, (475, 350, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (475 - 1, 350 - 1, 30 + 2, 30 + 2), 2)
            color12= pygame.draw.rect (screen, self.SKYBLUE, (375, 350, 30, 30))
            pygame.draw.rect(screen, self.WHITE, (375 - 1, 350 - 1, 30 + 2, 30 + 2), 2)

            #Jugadores 1 y 2
            colorJugador1 = pygame.draw.rect (screen, self.colorAux1, (140, 220, 100, 100))
            colorJugador2 = pygame.draw.rect (screen, self.colorAux2, (640, 220, 100, 100))
            
            self.boton13.cambiar_color(self.MENU_MOUSE_POS)
            self.boton13.actualizar(screen)

            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton13.checar_presionado(self.MENU_MOUSE_POS):
                        self.audio_menu.play()
                        self.opciones()

                    x, y = pygame.mouse.get_pos()
                    if color1.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (425 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
                        bandera=1
                    if color2.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (475 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
                        bandera=2
                    if color3.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (375 - 1, 200 - 1, 30 + 2, 30 + 2), 2)
                        bandera=3
                    if color4.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (425 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
                        bandera=4
                    if color5.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (475 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
                        bandera=5
                    if color6.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (375 - 1, 250 - 1, 30 + 2, 30 + 2), 2)
                        bandera=6
                    if color7.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (425 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
                        bandera=7
                    if color8.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (475 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
                        bandera=8
                    if color9.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (375 - 1, 300 - 1, 30 + 2, 30 + 2), 2)
                        bandera=9
                    if color10.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (425 - 1, 350 - 1, 30 + 2, 30 + 2), 2)
                        bandera=10
                    if color11.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (475 - 1, 350 - 1, 30 + 2, 30 + 2), 2)
                        bandera=11
                    if color12.collidepoint(x, y):
                        self.audio_menu.play()
                        pygame.draw.rect(screen, self.GREEN_SELECCION, (375 - 1, 350 - 1, 30 + 2, 30 + 2), 2)
                        bandera=12

                    if bandera == 1 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.ORANGE
                    elif bandera == 1 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.ORANGE
                    
                    if bandera == 2 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.RED
                    elif bandera == 2 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.RED
                    
                    if bandera == 3 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.BLUE
                    elif bandera == 3 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.BLUE
                    
                    if bandera == 4 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.MOSTAZA
                    elif bandera == 4 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.MOSTAZA
                    
                    if bandera == 5 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.AQUA
                    elif bandera == 5 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.AQUA
                    
                    if bandera == 6 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.BLUE2
                    elif bandera == 6 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.BLUE2
                    
                    if bandera == 7 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.PURPLE
                    elif bandera == 7 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.PURPLE
                    
                    if bandera == 8 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.FIUSHA
                    elif bandera == 8 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.FIUSHA
                    
                    if bandera == 9 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.RED2
                    elif bandera == 9 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.RED2
                    
                    if bandera == 10 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.PINK
                    elif bandera == 10 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.PINK
                    
                    if bandera == 11 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.BROWN
                    elif bandera == 11 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.BROWN
                    
                    if bandera == 12 and colorJugador1.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux1 = self.SKYBLUE
                    elif bandera == 12 and colorJugador2.collidepoint(x,y):
                        self.audio_menu.play()
                        self.colorAux2 = self.SKYBLUE

            #Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(60)    

    def menu_dentro_del_nivel(self):
        
        def dentro(event):
            self.boton15.config(image=self.imagen_cambio_color15)
        def fuera(event):
            self.boton15.config(image=self.imagen15)
            
        def dentro2(event):
            self.boton16.config(fg="#00FF00")
        def fuera2(event):
            self.boton16.config(fg="White")

        def dentro3(event):
            self.boton17.config(fg="#00FF00")
        def fuera3(event):
            self.boton17.config(fg="White")
        
        def dentro4(event):
            self.boton18.config(fg="#00FF00")
        def fuera4(event):
            self.boton18.config(fg="White")

        def fun_reiniciar():
            self.audio_menu.play()
            self.musica_fondoNiveles.stop()
            ventana.destroy()
            if self.jugando_nivel == "2":
                self.numero_nivel["2"]()
            if self.jugando_nivel == "3":
                self.numero_nivel["3"]()
            if self.jugando_nivel == "4":
                self.numero_nivel["4"]()
            if self.jugando_nivel == "5":
                self.numero_nivel["5"]()
        
        def fun_reanudar():
            ventana.destroy()
            self.audio_menu.play()

        def fun_Menu_Principal():
            self.audio_menu.play()
            self.musica_fondo.stop()
            self.musica_fondoNiveles.stop()
            self.musica_fondoNiveles2.stop()
            self.musica_fondoNiveles3.stop()
            self.musica_fondoNiveles4.stop()
            self.musica_fondo.play(-1)
            ventana.destroy()
            self.menu_principal()
            
             
        ventana=Tk()
        ventana.title("HiCube")
        ventana.iconbitmap("Imagenes/Icono.ico")
        fuenteTK = Font(family="cambria", size=15)

        # Obtener el ancho y alto de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Definir el tamaño de la ventana
        ventana_width = 500
        ventana_height = 270

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - ventana_width) // 2
        y = (screen_height - ventana_height) // 2

        # Establecer la geometría de la ventana
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

        #Color de fondo
        color_hex = '#{0:02X}{1:02X}{2:02X}'.format(*self.GREY)
        color_hex2 = '#{0:02X}{1:02X}{2:02X}'.format(*self.YELLOW)
        color_hex3 = '#{0:02X}{1:02X}{2:02X}'.format(*self.BLUE)
        color_hex4 = '#{0:02X}{1:02X}{2:02X}'.format(*self.RED)

        #Color_hex transforma mi color de RGB a Hexadecimal
        ventana.configure(bg=color_hex)

        # Texto para la primera barra
        etiqueta0 = Label(ventana, text="Pausado", fg="white", bg=color_hex, font=("cambria", 20))
        etiqueta0.place(x=193, y=30)

        # Crear un botón con la imagen
        self.imagen15 = PhotoImage(file="Imagenes/Boton_Sonido.png")
        self.imagen_cambio_color15 = PhotoImage(file="Imagenes/Boton_Sonido1.png")
        self.boton15 = Button(ventana, image=self.imagen15, width=20, height=20, bd=0, highlightthickness=0)
        self.boton15.pack()
        self.boton15.place(x=425, y=40)
        self.boton15.config(command=self.sonido)
        self.boton15.bind("<Enter>", dentro)
        self.boton15.bind("<Leave>", fuera)

        self.imagen16 = PhotoImage(file="Imagenes/Boton_Jugar_TK.png")
        self.boton16 = Button(ventana, text="Reiniciar", font=fuenteTK, bd=0, highlightthickness=0, compound="center")
        self.boton16.pack()
        self.boton16.place(x=80, y=100)
        self.boton16.config(command=fun_reiniciar, image=self.imagen16, fg="White")
        self.boton16.bind("<Enter>", dentro2)
        self.boton16.bind("<Leave>", fuera2)

        self.boton17 = Button(ventana, text="Reanudar", font=fuenteTK, bd=0, highlightthickness=0, compound="center")
        self.boton17.pack()
        self.boton17.place(x=280, y=100)
        self.boton17.config(command=fun_reanudar, image=self.imagen16, fg="White")
        self.boton17.bind("<Enter>", dentro3)
        self.boton17.bind("<Leave>", fuera3)

        self.imagen18 = PhotoImage(file="Imagenes/Boton_Jugar_TK2.png")
        self.boton18 = Button(ventana, text="Menu Principal", font=fuenteTK, bd=0, highlightthickness=0, compound="center")
        self.boton18.pack()
        self.boton18.place(x=173, y=180)
        self.boton18.config(command=fun_Menu_Principal, image=self.imagen18, fg="White")
        self.boton18.bind("<Enter>", dentro4)
        self.boton18.bind("<Leave>", fuera4)

        ventana.mainloop() 

    def menu_dentro_del_juego(self):
        
        def dentro(event):
            self.boton15.config(image=self.imagen_cambio_color15)
        def fuera(event):
            self.boton15.config(image=self.imagen15)

        def dentro3(event):
            self.boton17.config(fg="#00FF00")
        def fuera3(event):
            self.boton17.config(fg="White")
        
        def dentro4(event):
            self.boton18.config(fg="#00FF00")
        def fuera4(event):
            self.boton18.config(fg="White")
        
        def fun_reanudar():
            ventana.destroy()
            self.audio_menu.play()

        def fun_Menu_Principal():
            self.audio_menu.play()
            self.bandera_controles_tutorial = False
            self.musica_fondo.stop()
            self.musica_fondoNiveles.stop()
            self.musica_fondo.play(-1)
            ventana.destroy()
            self.menu_principal()
             
        ventana=Tk()
        ventana.title("HiCube")
        ventana.iconbitmap("Imagenes/Icono.ico")
        fuenteTK = Font(family="cambria", size=15)

        # Obtener el ancho y alto de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Definir el tamaño de la ventana
        ventana_width = 500
        ventana_height = 270

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width - ventana_width) // 2
        y = (screen_height - ventana_height) // 2

        # Establecer la geometría de la ventana
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

        #Color de fondo
        color_hex = '#{0:02X}{1:02X}{2:02X}'.format(*self.GREY)
        color_hex2 = '#{0:02X}{1:02X}{2:02X}'.format(*self.YELLOW)
        color_hex3 = '#{0:02X}{1:02X}{2:02X}'.format(*self.BLUE)
        color_hex4 = '#{0:02X}{1:02X}{2:02X}'.format(*self.RED)

        #Color_hex transforma mi color de RGB a Hexadecimal
        ventana.configure(bg=color_hex)

        # Texto para la primera barra
        etiqueta0 = Label(ventana, text="Pausado", fg="white", bg=color_hex, font=("cambria", 20))
        etiqueta0.place(x=193, y=30)

        # Crear un botón con la imagen
        self.imagen15 = PhotoImage(file="Imagenes/Boton_Sonido.png")
        self.imagen_cambio_color15 = PhotoImage(file="Imagenes/Boton_Sonido1.png")
        self.boton15 = Button(ventana, image=self.imagen15, width=20, height=20, bd=0, highlightthickness=0)
        self.boton15.pack()
        self.boton15.place(x=425, y=40)
        self.boton15.config(command=self.sonido)
        self.boton15.bind("<Enter>", dentro)
        self.boton15.bind("<Leave>", fuera)

        self.imagen16 = PhotoImage(file="Imagenes/Boton_Jugar_TK2.png")
        self.boton17 = Button(ventana, text="Reanudar", font=fuenteTK, bd=0, highlightthickness=0, compound="center")
        self.boton17.pack()
        self.boton17.place(x=83, y=140) 
        self.boton17.config(command=fun_reanudar, image=self.imagen16, fg="White")
        self.boton17.bind("<Enter>", dentro3)
        self.boton17.bind("<Leave>", fuera3)

        self.imagen18 = PhotoImage(file="Imagenes/Boton_Jugar_TK2.png")
        self.boton18 = Button(ventana, text="Menu Principal", font=fuenteTK, bd=0, highlightthickness=0, compound="center")
        self.boton18.pack()
        self.boton18.place(x=258, y=140) 
        self.boton18.config(command=fun_Menu_Principal, image=self.imagen18, fg="White")
        self.boton18.bind("<Enter>", dentro4)
        self.boton18.bind("<Leave>", fuera4)

        ventana.mainloop() 
         
    def pantalla_juego_terminado(self):
        self.musica_fondo.stop()
        self.musica_fondoNiveles.stop()
        self.musica_fondo.play(-1)
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)
            for event in pygame.event.get():
                #Condiciones para moverse entre los menus
                if event.type == pygame.QUIT:  
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton19.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.musica_fondo.stop()
                         self.musica_fondoNiveles.stop()
                         self.musica_fondoNiveles.play(-1)
                         if self.jugando_nivel == "2":
                              self.numero_nivel["2"]()
                         if self.jugando_nivel == "3":
                              self.numero_nivel["3"]()
                         if self.jugando_nivel == "4":
                              self.numero_nivel["4"]()
                         if self.jugando_nivel == "5":
                              self.numero_nivel["5"]()
                         
                    if self.boton20.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.musica_fondo.stop()
                         self.musica_fondoNiveles.stop()
                         self.musica_fondo.play(-1)
                         self.menu_principal()

            # Dibujar la imagen de fondo en la ventana
            screen.blit(self.fondo_juego_terminado, (0, 0))

            self.boton19.actualizar(self.screen)
            self.boton19.cambiar_color(pygame.mouse.get_pos())
            self.boton20.actualizar(self.screen)
            self.boton20.cambiar_color(pygame.mouse.get_pos())

                
            # Actualizar la pantalla
            pygame.display.update()
 
    def menu_modo_juego(self):
         while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()
            #Hacer visible/invisible el mouse
            pygame.mouse.set_visible(1)
            for event in pygame.event.get():
                #Condiciones para moverse entre los menus
                if event.type == pygame.QUIT:  
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton14.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.menu_dentro_del_juego()
                    if self.boton21.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.bandera_modo_juego=1
                         self.pantalla_tutorial()
                    if self.boton22.checar_presionado(self.MENU_MOUSE_POS):
                         self.audio_menu.play()
                         self.bandera_modo_juego=2
                         self.pantalla_tutorial()

            # Dibujar la imagen de fondo en la ventana
            screen.blit(self.fondo_nivel_vacio, (0, 0))
            Titulo = fuente_grande.render("Modo de juego", False, self.WHITE)
            screen.blit(Titulo, [130, 190])

            self.boton14.actualizar(self.screen)
            self.boton14.cambiar_color(pygame.mouse.get_pos())
            self.boton21.actualizar(self.screen)
            self.boton21.cambiar_color(pygame.mouse.get_pos())
            self.boton22.actualizar(self.screen)
            self.boton22.cambiar_color(pygame.mouse.get_pos())

            # Cambiar el fondo cuando el mouse está sobre los botones 21 o 22
            if self.boton21.rect.collidepoint(self.MENU_MOUSE_POS):
                screen.blit(self.fondo_nivel_VS, (0, 0))
                self.boton21.actualizar(self.screen)
                self.boton21.cambiar_color(pygame.mouse.get_pos())
                self.boton22.actualizar(self.screen)
                self.boton22.cambiar_color(pygame.mouse.get_pos())
                Titulo = fuente_grande.render("Modo de juego", False, self.WHITE)
                screen.blit(Titulo, [130, 190])
            elif self.boton22.rect.collidepoint(self.MENU_MOUSE_POS):
                screen.blit(self.fondo_nivel_solitario, (0, 0))
                self.boton21.actualizar(self.screen)
                self.boton21.cambiar_color(pygame.mouse.get_pos())
                self.boton22.actualizar(self.screen)
                self.boton22.cambiar_color(pygame.mouse.get_pos())
                Titulo = fuente_grande.render("Modo de juego", False, self.WHITE)
                screen.blit(Titulo, [130, 190])
                
            # Actualizar la pantalla
            pygame.display.update()

    def main(self):
        while True:
            self.pantalla_carga()
            self.musica_fondo.play(-1)
            self.menu_principal()    

if __name__ == "__main__":
    game = Juego()
    game.main()
    #game.jugarNivel2()
    #game.menu_modo_juego()
    
