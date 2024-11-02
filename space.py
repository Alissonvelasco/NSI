import pygame  # Importa la biblioteca Pygame que permite crear juegos en Python
import sys  # Importa el módulo sys, que proporciona acceso a algunas variables y funciones utilizadas o mantenidas por el intérprete
import random  # Importa el módulo random, que permite generar números aleatorios
import math  # Importa el módulo math, que proporciona acceso a funciones matemáticas (aunque no se utiliza en el código)

pygame.init()  # Inicializa todos los módulos de Pygame

# Configura la ventana del juego con un tamaño de 800x600 píxeles
screen = pygame.display.set_mode((800, 600))
# Establece el título de la ventana del juego
pygame.display.set_caption("Space Invaders")

# Carga la imagen de fondo para el juego
fond = pygame.image.load('background.png')

class Joueur:  # Define la clase Joueur (Jugador)
    def __init__(self):  # Método constructor que inicializa el jugador
        self.position = 400  # Posición horizontal inicial del jugador
        self.image = pygame.image.load("vaisseau.png")  # Carga la imagen del jugador
        self.sens = "O"  # Dirección en la que se mueve el jugador (O significa "ninguna" en este contexto)
        self.vitesse = 5  # Velocidad de movimiento del jugador
        self.score = 0  # Inicializa el puntaje del jugador
        self.points_de_vie = 3  # Puntos de vida del jugador
        self.niveau = 1  # Nivel del jugador
        self.en_cours = True  # Indica si el juego está en curso

    def afficher_score(self):  # Método para mostrar el puntaje del jugador
        font = pygame.font.SysFont(None, 36)  # Crea una fuente para el texto
        texte = font.render(f'Score: {self.score}', True, (255, 255, 255))  # Renderiza el texto del puntaje en blanco
        screen.blit(texte, (10, 10))  # Dibuja el texto en la pantalla en la posición (10, 10)

    def augmenter_niveau(self):  # Método para aumentar el nivel del jugador
        self.niveau += 1  # Incrementa el nivel en 1

    def prendre_dommage(self):  # Método para manejar el daño al jugador
        self.points_de_vie -= 1  # Reduce los puntos de vida en 1
        if self.points_de_vie <= 0:  # Si los puntos de vida son 0 o menos
            self.perdre()  # Llama al método perdre (perder)

    def perdre(self):  # Método que se llama cuando el jugador pierde
        self.en_cours = False  # Cambia el estado del juego a no en curso
        print("Game Over")  # Imprime "Game Over" en la consola
        pygame.quit()  # Cierra Pygame
        sys.exit()  # Termina el programa

    def deplacer(self):  # Método para mover al jugador
        if self.sens == "droite" and self.position < 740:  # Si se mueve a la derecha y no está en el borde derecho
            self.position += self.vitesse  # Aumenta la posición del jugador
        elif self.sens == "gauche" and self.position > 0:  # Si se mueve a la izquierda y no está en el borde izquierdo
            self.position -= self.vitesse  # Disminuye la posición del jugador

class Balle:  # Define la clase Balle (Bala)
    def __init__(self, tireur):  # Método constructor que recibe al tirador (jugador)
        self.tireur = tireur  # Asigna el tirador
        self.depart = tireur.position  # La posición inicial de la bala es la del tirador
        self.hauteur = 492  # Altura inicial de la bala
        self.image = pygame.image.load("balle.png")  # Carga la imagen de la bala
        self.etat = "chargee"  # Estado inicial de la bala (cargada)
        self.vitesse = 5  # Velocidad de la bala

    def bouger(self):  # Método para mover la bala
        if self.etat == "chargee":  # Si la bala está cargada
            self.depart = self.tireur.position  # Actualiza la posición inicial de la bala
            self.hauteur = 492  # Resetea la altura de la bala
        elif self.etat == "tiree":  # Si la bala ha sido disparada
            self.hauteur -= self.vitesse  # Disminuye la altura de la bala (se mueve hacia arriba)
            if self.hauteur < 0:  # Si la bala sale de la pantalla
                self.etat = "chargee"  # Resetea el estado de la bala a cargada

    def toucher(self, ennemi):  # Método para verificar si la bala toca a un enemigo
        if abs(self.hauteur - ennemi.hauteur) < 40 and abs(self.depart - ennemi.depart) < 40:  # Verifica la colisión
            self.etat = "chargee"  # Resetea el estado de la bala a cargada
            return True  # Devuelve verdadero si tocó al enemigo
        return False  # Devuelve falso si no tocó

class Ennemi:  # Define la clase Ennemi (Enemigo)
    NbEnnemis = 6  # Número máximo de enemigos

    def __init__(self):  # Método constructor para inicializar un enemigo
        self.depart = random.randint(1, 700)  # Posición horizontal aleatoria del enemigo
        self.hauteur = 10  # Altura inicial del enemigo
        self.type = random.choice([1, 2])  # Elige aleatoriamente un tipo de enemigo
        if self.type == 1:  # Si es del tipo 1
            self.image = pygame.image.load("invader1.png")  # Carga la imagen del enemigo tipo 1
            self.vitesse = 1  # Velocidad del enemigo tipo 1
        else:  # Si es del tipo 2
            self.image = pygame.image.load("invader2.png")  # Carga la imagen del enemigo tipo 2
            self.vitesse = 2  # Velocidad del enemigo tipo 2

    def avancer(self):  # Método para mover al enemigo hacia abajo
        self.hauteur += self.vitesse  # Aumenta la altura del enemigo según su velocidad

    def disparaitre(self):  # Método para hacer que el enemigo reaparezca
        self.depart = random.randint(1, 700)  # Reasigna una posición horizontal aleatoria
        self.hauteur = 10  # Resetea la altura del enemigo

# Création des objets (Creación de objetos)
player = Joueur()  # Crea una instancia de la clase Joueur
tir = Balle(player)  # Crea una instancia de la clase Balle asociada al jugador
tir.etat = "chargee"  # Establece el estado de la bala como cargada
listeEnnemis = [Ennemi() for _ in range(Ennemi.NbEnnemis)]  # Crea una lista de enemigos

running = True  # Variable que controla el bucle del juego
while running:  # Bucle principal del juego
    screen.blit(fond, (0, 0))  # Dibuja el fondo en la pantalla
    player.afficher_score()  # Muestra el puntaje del jugador

    for event in pygame.event.get():  # Procesa los eventos de Pygame
        if event.type == pygame.QUIT:  # Si se recibe un evento de cierre de ventana
            running = False  # Cambia el estado del bucle a falso
            sys.exit()  # Termina la ejecución del programa

        if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
            if event.key == pygame.K_LEFT:  # Si es la tecla de izquierda
                player.sens = "gauche"  # Cambia la dirección del jugador a izquierda
            elif event.key == pygame.K_RIGHT:  # Si es la tecla de derecha
                player.sens = "droite"  # Cambia la dirección del jugador a derecha
            elif event.key == pygame.K_SPACE:  # Si se presiona la barra espaciadora
                tir.etat = "tiree"  # Cambia el estado de la bala a disparada

        if event.type == pygame.KEYUP:  # Si se suelta una tecla
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Si es la tecla izquierda o derecha
                player.sens = "O"  # Resetea la dirección del jugador a ninguna

    player.deplacer()  # Llama al método para mover al jugador
    tir.bouger()  # Llama al método para mover la bala
    
    for ennemi in listeEnnemis:  # Recorre la lista de enemigos
        ennemi.avancer()  # Mueve al enemigo
        if tir.toucher(ennemi):  # Verifica si la bala toca al enemigo
            ennemi.disparaitre()  # Si se toca, hace que el enemigo reaparezca en una nueva posición
            player.score += 1  # Incrementa el puntaje del jugador en 1

    # Dibuja la imagen del jugador en la posición actual
    screen.blit(player.image, (player.position, 500))  
    if tir.etat == "tiree":  # Si la bala está en estado "tiree" (disparada)
        screen.blit(tir.image, (tir.depart, tir.hauteur))  # Dibuja la bala en la pantalla

    for ennemi in listeEnnemis:  # Recorre la lista de enemigos
        screen.blit(ennemi.image, (ennemi.depart, ennemi.hauteur))  # Dibuja cada enemigo en la pantalla

    pygame.display.update()  # Actualiza la pantalla para mostrar todos los cambios