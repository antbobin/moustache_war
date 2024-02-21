import pygame

from parameters import *
from fighter import Fighter

class Game:

    def __init__(self) -> None:
        """
        Initialisation de la fenêtre, des images, ... 
        """

        # Initialisation de la fenêtre
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        # Indication de run et endgame
        self.running = True

        # Scores
        self.score_left = 0
        self.score_right = 0

        # Horloge
        self.clock = pygame.time.Clock()

        # Musique
        pygame.mixer.music.load("assets/musics/80s_arcade.mp3")
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1, 0., 5000)
        hit_sound = pygame.mixer.Sound("assets/musics/hit.wav")
        hit_sound.set_volume(EFFECTS_VOLUME)

        # Texte
        self.font = pygame.font.SysFont("Arial", SCORE_FONTSIZE)

        # Background 
        self.background_image = pygame.image.load("assets/images/boxing_background_final.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Recherche de manettes (qu'on utilisera par défaut)
        controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        left_controller = controllers[0] if len(controllers) > 0 else None
        right_controller = controllers[1] if len(controllers) > 1 else None

        # Création de 2 personnages
        left_fighter_image = pygame.image.load("assets/images/robin.png").convert_alpha()
        right_fighter_image = pygame.image.load("assets/images/kevin.png").convert_alpha()
    
        right_fighter_attack_image = pygame.image.load("assets/images/kevin_attack.png").convert_alpha()
        left_fighter_attack_image = pygame.image.load("assets/images/robin_attack.png").convert_alpha()
        impact_image = pygame.transform.scale(pygame.image.load("assets/images/impact.png").convert_alpha(), (IMPACT_SIZE, IMPACT_SIZE))
        self.left_fighter = Fighter(300, FLOOR_HEIGHT-FIGHTER_HEIGHT, LEFT_FIGHTER_KEYS, ORIENTATION.RIGHT, left_controller, left_fighter_image, left_fighter_attack_image, impact_image, hit_sound)
        self.right_fighter = Fighter(1600, FLOOR_HEIGHT-FIGHTER_HEIGHT, RIGHT_FIGHTER_KEYS, ORIENTATION.LEFT, right_controller, right_fighter_image, right_fighter_attack_image, impact_image, hit_sound)

    def reset(self) -> None:
        """
        Reset des positions et barres de vie
        """
        self.left_fighter.rectangle.x = 300
        self.left_fighter.rectangle.y = FLOOR_HEIGHT-FIGHTER_HEIGHT
        self.left_fighter.health_points = FIGHTER_HEALTH
        self.left_fighter.orientation = ORIENTATION.RIGHT

        self.right_fighter.rectangle.x = 1600
        self.right_fighter.rectangle.y = FLOOR_HEIGHT-FIGHTER_HEIGHT
        self.right_fighter.health_points = FIGHTER_HEALTH
        self.right_fighter.orientation = ORIENTATION.LEFT
    
    def update_time(self) -> None:
        """
        Mise à jour du temps sur les fps paramètres
        """
        self.clock.tick(GAME_FRAME_RATE)
    
    def draw_all(self) -> None:
        """
        Affichage de l'image de fond et des personnages
        """
        # background
        self.screen.blit(self.background_image, (0,0))
        # Combattants
        self.left_fighter.draw(self.screen)
        self.right_fighter.draw(self.screen)
        # Barres de vies (fond et HP actuels)
        pygame.draw.rect(self.screen, COLOR.YELLOW, (HEALTHBAR_MARGIN - HEALTHBAR_BORDER, SCREEN_HEIGHT - HEALTHBAR_MARGIN - HEALTHBAR_BORDER, 
                                                     HEALTHBAR_WIDTH + 2*HEALTHBAR_BORDER, HEALTHBAR_HEIGHT+ 2*HEALTHBAR_BORDER))
        pygame.draw.rect(self.screen, COLOR.RED, (HEALTHBAR_MARGIN, SCREEN_HEIGHT - HEALTHBAR_MARGIN, HEALTHBAR_WIDTH * self.left_fighter.health_points/FIGHTER_HEALTH, HEALTHBAR_HEIGHT))
        pygame.draw.rect(self.screen, COLOR.YELLOW, (SCREEN_WIDTH - HEALTHBAR_MARGIN - HEALTHBAR_WIDTH - HEALTHBAR_BORDER, SCREEN_HEIGHT - HEALTHBAR_MARGIN - HEALTHBAR_BORDER, 
                                                     HEALTHBAR_WIDTH + 2*HEALTHBAR_BORDER, HEALTHBAR_HEIGHT + 2*HEALTHBAR_BORDER))
        pygame.draw.rect(self.screen, COLOR.RED, (SCREEN_WIDTH - HEALTHBAR_MARGIN - HEALTHBAR_WIDTH, SCREEN_HEIGHT - HEALTHBAR_MARGIN, 
                                                  HEALTHBAR_WIDTH * self.right_fighter.health_points/FIGHTER_HEALTH, HEALTHBAR_HEIGHT))
        
        # Score
        score_left = self.font.render(f"TEAM ROBIN : {self.score_left}", True, COLOR.WHITE)
        self.screen.blit(score_left,(HEALTHBAR_MARGIN, SCREEN_HEIGHT - 1.5*HEALTHBAR_MARGIN))
        score_right = self.font.render(f"TEAM KEVIN : {self.score_right}", True, COLOR.WHITE)
        self.screen.blit(score_right,(SCREEN_WIDTH - HEALTHBAR_MARGIN - HEALTHBAR_WIDTH, SCREEN_HEIGHT - 1.5*HEALTHBAR_MARGIN))
        
        pygame.display.update()
    

    def handle_events(self) -> None:
        """
        Gestion des événements
        """

        # Parcours des événements 
        for event in pygame.event.get():
            # Arrêt
            if event.type == pygame.QUIT:
                self.running = False

    def handle_keys(self) -> None:
        """
        Vérifie les touches pressées et appelle les actions en conséquence
        """

        # Récupération des touches
        keys = pygame.key.get_pressed()

        # Déplacement
        self.left_fighter.move(keys, self.right_fighter)
        self.right_fighter.move(keys, self.left_fighter)
        # Attaques
        self.left_fighter.attack(keys, self.right_fighter)
        self.right_fighter.attack(keys, self.left_fighter)

    def check_scores(self) -> None:
        """
        Check si la vie d'un combattant tombe à 0
        """
        if not self.left_fighter.health_points:
            self.score_right += 1
            self.reset()
        if not self.right_fighter.health_points:
            self.score_left += 1
            self.reset()

    def run(self) -> None:
        """
        Définition de la boucle 
        """

        while self.running:
            self.update_time()
            self.handle_keys()
            self.check_scores()
            self.draw_all()
            self.handle_events()
            
        pygame.quit()

# Main
if __name__ == '__main__':
    game = Game()
    game.run()
