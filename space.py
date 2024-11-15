import pygame  # Importe la bibliothèque Pygame qui permet de créer des jeux en Python
import sys  # Importe le module sys, qui fournit l'accès à certaines variables et fonctions utilisées par l'interpréteur
import random  # Importe le module random, qui permet de générer des nombres aléatoires
import math  # Importe le module math, qui donne accès à des fonctions mathématiques

pygame.init()  # Initialise tous les modules de Pygame

# Configure la fenêtre du jeu avec une taille de 800x600 pixels
screen = pygame.display.set_mode((800, 600))
# Définit le titre de la fenêtre du jeu
pygame.display.set_caption("Space Invaders")
# Charge l'image de fond pour le jeu
fond = pygame.image.load('background.png')

# Charge le fichier de musique
pygame.mixer.init()  # Initialise le module 
pygame.mixer.music.load("byte-blast-8-bit-arcade-music-background-music-for-video-208780.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Charge le son d'explosion
explosion_sound = pygame.mixer.Sound("large-underwater-explosion-190270.mp3")
# Charge l'image de l'explosion
explosion_image = pygame.image.load("blast.png") 


# Fonction pour afficher l'écran de démarrage
def ecran_demarrage():
    screen.fill((0, 0, 0))  # Remplit l'écran en noir
    font = pygame.font.SysFont(None, 72)
    texte_demarrage = font.render("Commencer", True, (255, 255, 255))  # Texte en blanc
    screen.blit(texte_demarrage, (250, 250))  # Position au centre de l'écran
    pygame.display.update()  # Affiche le message à l'écran

    # Attend que l'utilisateur appuie sur une touche pour commencer
    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Détecte toute touche appuyée
                en_attente = False  # Sort de la boucle et commence le jeu

# Appelle l'écran de démarrage avant de commencer le jeu
ecran_demarrage()

class Joueur:  # Définit la classe Joueur
    def __init__(self):  # Méthode constructeur qui initialise le joueur
        self.position = 400  # Position horizontale initiale du joueur
        self.image = pygame.image.load("vaisseau.png")  # Charge l'image du joueur
        self.sens = "O"  # Direction de déplacement du joueur ("O" signifie "aucune" dans ce contexte)
        self.vitesse = 10  # Vitesse de déplacement du joueur
        self.score = 0  # Initialise le score du joueur
        self.points_de_vie = 10  # Points de vie du joueur
        self.niveau = 1  # Niveau du joueur
        self.en_cours = True  # Indique si le jeu est en cours
        self.enemies_eliminated = 0  # Nouvelle variable pour compter les ennemis éliminés
        self.cups = 0  # Compteur de coupes obtenues



    def afficher_score(self):  # Méthode pour afficher le score du joueur
        font = pygame.font.SysFont(None, 36)  # Crée une police pour le texte
        texte = font.render(f'Score: {self.score}', True, (255, 255, 255))  # Texte blanc pour le score
        screen.blit(texte, (10, 10))  # Affiche le score à la position (10, 10)
        # Affiche les points de vie du joueur
        vie = font.render(f'Vie: {self.points_de_vie}', True, (255, 255, 255))
        screen.blit(vie, (10, 50))
        niveau = font.render(f'Level: {self.niveau}', True, (255, 255, 255))
        screen.blit(niveau, (10, 90))
        cups_text = font.render(f'Coupes: {self.cups}', True, (255, 255, 0))  # Texte des coupes
        screen.blit(cups_text, (10, 130))  # Afficher les coupes à l'écran


    def augmenter_niveau(self):  # Méthode pour augmenter le niveau du joueur
        self.niveau += 1  # Incrémente le niveau de 1
        # Augmente la vitesse des ennemis à chaque niveau
        for ennemi in listeEnnemis:
            ennemi.vitesse += 0.2  # Augmente la vitesse de 0,2      
         #À partir du niveau 5, tous les ennemis se déplacent en zigzag
        if self.niveau >= 4 and self.niveau <= 7:
            for i in range(len(listeEnnemis)):
                listeEnnemis[i] = EnnemiZigzag()  # Remplace l'ennemi par un EnnemiZigzag

        
    def prendre_dommage(self):  # Méthode pour gérer les dégâts subis par le joueur
        self.points_de_vie -= 1  # Réduit les points de vie de 1
        if self.points_de_vie <= 0:  # Si les points de vie sont égaux ou inférieurs à 0
            self.perdre()  # Appelle la méthode perdre

    def perdre(self):  # Méthode appelée lorsque le joueur perd
        font = pygame.font.SysFont(None, 72)  # Taille grande pour "Game Over"
        game_over_text = font.render("Game Over", True, (255, 0, 0))  # Texte rouge
        screen.blit(game_over_text, (300, 250))  # Position au centre de l'écran
        pygame.display.update()  # Affiche le message à l'écran
        pygame.time.delay(3000)  # Pause de 3 secondes avant de quitter
        pygame.quit()
        sys.exit()

    def deplacer(self):  # Méthode pour déplacer le joueur
        if self.sens == "droite" and self.position < 740:  # Si le joueur se déplace vers la droite sans dépasser le bord
            self.position += self.vitesse  # Augmente la position du joueur
        elif self.sens == "gauche" and self.position > 0:  # Si le joueur se déplace vers la gauche sans dépasser le bord
            self.position -= self.vitesse  # Diminue la position du joueur

class Balle:  # Définit la classe Balle
    def __init__(self, tireur):  # Méthode constructeur qui reçoit le tireur (joueur)
        self.tireur = tireur  # Assigne le tireur
        self.depart = tireur.position  # La position initiale de la balle est celle du tireur
        self.hauteur = 492  # Hauteur initiale de la balle
        self.image = pygame.image.load("bullets.png")  # Charge l'image de la balle
        self.image = pygame.transform.scale(self.image, (40, 40))  # Redimensionne la balle
        self.etat = "chargee"  # État initial de la balle (chargée)
        self.vitesse = 30  # Vitesse de la balle

    def bouger(self):  # Méthode pour déplacer la balle
        if self.etat == "chargee":  # Si la balle est chargée
            self.depart = self.tireur.position  # Réinitialise la position de départ de la balle
            self.hauteur = 492  # Réinitialise la hauteur de la balle
        elif self.etat == "tiree":  # Si la balle a été tirée
            self.hauteur -= self.vitesse  # Diminue la hauteur de la balle (se déplace vers le haut)
            if self.hauteur < 0:  # Si la balle sort de l'écran
                self.etat = "chargee"  # Réinitialise l'état de la balle en chargée

    def toucher(self, ennemi):  # Méthode pour vérifier si la balle touche un ennemi
        if abs(self.hauteur - ennemi.hauteur) < 40 and abs(self.depart - ennemi.depart) < 40:  # Vérifie la collision
            self.etat = "chargee"  # Réinitialise l'état de la balle
            return True  # Renvoie vrai si la balle touche
        return False  # Renvoie faux si pas de collision

# Nouvelle classe pour les balles des ennemis
class BalleEnnemi:
    def __init__(self, ennemi):
        self.depart = ennemi.depart
        self.hauteur = ennemi.hauteur + 20
        self.image = pygame.image.load("balle.png")  # Image pour les balles ennemies
        self.vitesse = 5

    def bouger(self):
        self.hauteur += self.vitesse  # La balle descend

    def toucher_joueur(self, joueur):
        return abs(self.hauteur - 500) < 20 and abs(self.depart - joueur.position) < 40
    

class Ennemi:  # Définit la classe Ennemi (Ennemi)
    NbEnnemis = 6  # Nombre maximum d'ennemis

    def __init__(self):  # Méthode constructeur pour initialiser un ennemi
        self.depart = random.randint(1, 700)  # Position horizontale aléatoire de l'ennemi
        self.hauteur = 10  # Hauteur initiale de l'ennemi
        self.type = random.choice([1, 2, 3, 4])  # Choisit aléatoirement un type d'ennemi
        if self.type == 1:  # Si c'est un ennemi de type 1
            self.image = pygame.image.load("invader1.png")  # Charge l'image de l'ennemi de type 1
            self.vitesse = 1  # Vitesse de l'ennemi de type 1
        elif self.type == 2:  # Si c'est un ennemi de type 2
            self.image = pygame.image.load("invader2.png")  # Charge l'image de l'ennemi de type 2
            self.vitesse = 1  # Vitesse de l'ennemi de type 2
        elif self.type == 3:  # Si c'est un ennemi de type 3
            self.image = pygame.image.load("bleu.png")  # Charge l'image de l'ennemi de type 3
            self.image = pygame.transform.scale(self.image, (60, 60))  # Taille 60x60
            self.vitesse = 1  # Vitesse de l'ennemi de type 3
        else:  # Si c'est un ennemi de type 4
            self.type == 4  
            self.image = pygame.image.load("violette.png")  # Charge l'image de l'ennemi de type 4
            self.image = pygame.transform.scale(self.image, (60, 60))  # Taille 60x60
            self.vitesse = 1  # Vitesse de l'ennemi de type 4
            self.sens = "droite"  # Direction initiale de l'ennemi

    def avancer(self):  # Méthode pour déplacer l'ennemi vers le bas
        self.hauteur += self.vitesse  # Augmente la hauteur de l'ennemi selon sa vitesse

    def disparaitre(self):  # Méthode pour faire réapparaître l'ennemi
        self.depart = random.randint(1, 700)  # Réassigne une position horizontale aléatoire
        self.hauteur = 10  # Réinitialise la hauteur de l'ennemi

    def deplacer(self):  # Assure que cette méthode est présente dans la classe Ennemi
        self.hauteur += self.vitesse
        
class EnnemiZigzag(Ennemi):  # Nouvelle classe pour l'ennemi en zigzag
    def __init__(self):
        super().__init__()  # Appelle le constructeur de la classe Ennemi
        self.sens = "droite"  # Commence à se déplacer vers la droite
        self.amplitude = 10  # Amplitude du mouvement en zigzag
        self.vitesse_zigzag = 3  # Vitesse du mouvement zigzag

    def deplacer(self):  # Méthode de déplacement en zigzag
        # Déplacement vertical habituel
        self.hauteur += self.vitesse

        # Déplacement en zigzag
        if self.sens == "droite":
            self.depart += self.vitesse_zigzag
            if self.depart > 700 - self.amplitude:  # Si atteint le bord droit
                self.sens = "gauche"  # Change la direction vers la gauche
        elif self.sens == "gauche":
            self.depart -= self.vitesse_zigzag
            if self.depart < self.amplitude:  # Si atteint le bord gauche
                self.sens = "droite"  # Change la direction vers la droite
class BalleClone:
    def __init__(self, clone):
        self.depart = clone.depart  # La posición inicial de la balle
        self.hauteur = clone.hauteur + 10  # Comienza un poco debajo del clone
        self.image = pygame.image.load("balle.png")  # 
        self.vitesse = 5  # Vitesse  de la balle
        self.sens = "joueur"  # La balle vers el joueur

    def bouger(self):
        if self.sens == "joueur":  # Si la bala va hacia el jugador
            self.hauteur += self.vitesse  # Baja la bala

    def toucher_joueur(self, joueur):
        # Si la balle touche le joueur, il perd de la vie
        return abs(self.hauteur - 500) < 20 and abs(self.depart - joueur.position) < 40

class CloneEnnemi:
    def __init__(self):
        # Charger et faire pivoter l'image du joueur de 180 degrés
        self.image = pygame.transform.rotate(pygame.image.load("spaceship.png"), 180)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.depart = random.randint(1, 700)  # Position initiale aléatoire sur l'axe x
        self.hauteur = 10  # Commence en haut de l'écran
        self.vitesse = 3  # Vitesse de déplacement du clone
        self.balles = []  # Liste pour stocker les balles tirées par le clone


    def deplacer(self):
        # Déplacement vertical vers le bas
        self.hauteur += self.vitesse
        # Si le clone sort de l'écran, il réapparaît en haut
        if self.hauteur > 600:
            self.depart = random.randint(1, 700)
            self.hauteur = 10

    def tirer_balle(self):
        # Probabilité que le clone tire une balle (1 chance sur 60 à chaque frame)
        if random.randint(1, 60) == 1:
            self.balles.append(BalleEnnemi(self))  # Crée une balle comme les ennemis normaux

    def update_balles(self):
        # Déplace chaque balle du clone et les supprime si elles sont hors écran ou touchent le joueur
        for balle in self.balles[:]:
            balle.bouger()
            if balle.toucher_joueur(player):
                player.prendre_dommage()  # Le joueur prend des dégâts s’il est touché
                self.balles.remove(balle)  # Supprime la balle qui a touché
            elif balle.hauteur > 600:
                self.balles.remove(balle)  # Supprime les balles hors de l'écran

class Explosion:  # Classe Explosion pour gérer les explosions
    def __init__(self, position):  # Constructeur
        self.image = explosion_image  # Image de l'explosion
        self.position = position  # Position de l'explosion
        self.duree = 2  # Durée de l'explosion
        self.temps_vie = 0  # Compteur de durée de vie

    def afficher(self):  # Méthode pour afficher l'explosion
        if self.duree > 0:  # Si la durée est supérieure à 0
            screen.blit(self.image, self.position)  # Dessine l'image de l'explosion à la position
            self.duree -= 1  # Diminue la durée

    def bouger(self):
        if self.visible:
            self.hauteur += self.vitesse

    def toucher_joueur(self, joueur):
        if self.visible and abs(self.hauteur - 500) < 40 and abs(self.position - joueur.position) < 40:
            self.visible = False
            return True
        return False

# Création des objets
player = Joueur()  # Crée une instance de la classe Joueur
tir = Balle(player)  # Crée une instance de la classe Balle associée au joueur
tir.etat = "chargee"  # Définit l'état de la balle comme chargée
listeEnnemis = [Ennemi() for _ in range(Ennemi.NbEnnemis)]  # Crée une liste d'ennemis
explosions = []  # Liste pour stocker les explosions
balle_ennemi = []
liste_clones = []  # Liste des clones


running = True  # Variable qui contrôle la boucle du jeu
while running:  # Boucle principale du jeu
    screen.blit(fond, (0, 0))  # Affiche le fond à l'écran
    player.afficher_score()  # Affiche le score du joueur et les coupes

    for event in pygame.event.get():  # Traite les événements de Pygame
        if event.type == pygame.QUIT:  # Si un événement de fermeture de fenêtre est reçu
            running = False  # Change l'état de la boucle à faux
            sys.exit()  # Termine l'exécution du programme

        if event.type == pygame.KEYDOWN:  # Si une touche est enfoncée
            if event.key == pygame.K_LEFT:  # Si c'est la touche gauche
                player.sens = "gauche"  # Change la direction du joueur vers la gauche
            elif event.key == pygame.K_RIGHT:  # Si c'est la touche droite
                player.sens = "droite"  # Change la direction du joueur vers la droite
            elif event.key == pygame.K_SPACE:  # Si la barre d'espace est enfoncée
                tir.etat = "tiree"  # Change l'état de la balle à tirée

        if event.type == pygame.KEYUP:  # Si une touche est relâchée
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Si c'est la touche gauche ou droite
                player.sens = "O"  # Réinitialise la direction du joueur à aucune

    player.deplacer()  # Appelle la méthode pour déplacer le joueur
    tir.bouger()  # Appelle la méthode pour déplacer la balle
    # Met à jour l'état de chaque ennemi
    for ennemi in listeEnnemis:
        ennemi.deplacer()  # Appelle la méthode de déplacement de chaque ennemi
        if ennemi.hauteur > 500:
            player.prendre_dommage()
            listeEnnemis.remove(ennemi)
            listeEnnemis.append(Ennemi())    # Remplace l'ennemi détruit par un nouveau

        if tir.toucher(ennemi):
            explosion_sound.play()
            player.score += 10
            player.enemies_eliminated += 1
            listeEnnemis.remove(ennemi)
            listeEnnemis.append(Ennemi())
            explosions.append(Explosion((ennemi.depart, ennemi.hauteur)))
        # Vérifie si le joueur a éliminé quatre ennemis pour monter de niveau
        if player.enemies_eliminated >= 5:
            player.cups += 1  # Augmenter les coupes
            player.augmenter_niveau()  # Augmente le niveau
            player.enemies_eliminated = 0  # Réinitialise le compteur d'ennemis éliminés

        # Logique pour que les ennemis tirent
        if random.randint(2, 500) == 1:  # 1/500 de probabilité par image
            balle_ennemi.append(BalleEnnemi(ennemi))

    # Déplace et vérifie les balles des ennemis
    for balle in balle_ennemi[:]:
        balle.bouger()
        if balle.toucher_joueur(player):
            player.prendre_dommage()
            balle_ennemi.remove(balle)
        elif balle.hauteur > 600:
            balle_ennemi.remove(balle)
    # Dessine les balles des ennemis
    for balle in balle_ennemi:
        screen.blit(balle.image, (balle.depart, balle.hauteur))

    # Met à jour et dessine les explosions
    for explosion in explosions:
        explosion.afficher()
        if explosion.duree <= 0:
            explosions.remove(explosion)

    # Dessine le joueur, la balle et les ennemis
    screen.blit(player.image, (player.position, 500))
    screen.blit(tir.image, (tir.depart, tir.hauteur))
    for ennemi in listeEnnemis:
        screen.blit(ennemi.image, (ennemi.depart, ennemi.hauteur))
    
# générer plusieurs clones entre les niveaux 5 et 10
    if 8 <= player.niveau <= 10 and len(liste_clones) < 5:  # Limite à 5 clones
        if random.randint(1, 100) <= 10:  # 10% de probabilité par frame
            clone = CloneEnnemi()  # Crée un clone
            liste_clones.append(clone)  # Ajoute le clone à la liste des clones

    # Déplacer et gérer les balles des clones
    for clone in liste_clones:
        clone.deplacer()  # Déplace le clone vers le bas
        clone.tirer_balle()  # Le clone a la possibilité de tirer une balle
        clone.update_balles()  # Met à jour les balles tirées par le clone
        screen.blit(clone.image, (clone.depart, clone.hauteur))  # Affiche le clone
    # Afficher les clones et leurs balles
    for clone in liste_clones:
        screen.blit(clone.image, (clone.depart, clone.hauteur))  # Affiche chaque clone
        for balle in clone.balles:
            screen.blit(balle.image, (balle.depart, balle.hauteur))  # Affiche les balles du clone


    pygame.mixer.music.stop
    pygame.display.update()  # Met à jour l'écran pour afficher tous les changements
