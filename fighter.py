import pygame

from parameters import *
from rock import Rock

class Fighter:

    def __init__(self, pos_x: float,  pos_y: float, keys: dict,
                 orientation: int, controller=None, image=None, image_attack=None,
                 impact_image=None, hit_sound=None) -> None:
        """
        Création du personnage à une position donnée
        """
        #Rectangle représentatif pour l'instant
        self.rectangle = pygame.Rect((pos_x, pos_y, FIGHTER_WIDTH, FIGHTER_HEIGHT))
        
        # Mapping des touches de contrôle 
        self.keys = keys
        self.controller = controller

        # Orientation initiale
        self.orientation = orientation

        # Image
        self.image = image
        self.image_attack = image_attack
        self.impact_image = impact_image

        # Pierre jetée
        self.rock = None

        # Impact poing ou pierre 
        self.impact_pos = (0, 0)
        self.impact_timer = -99999
        self.impact_sound = hit_sound

        # Mouvement arrière crée un blocage 
        self.defense = False

        # Vitesse verticale
        self.vertical_speed = 0

        # Indicateur d'attaque et instant de la dernière attaque
        self.attack_status = ATTACK_STATUS.READY
        self.last_attack_time_ms = -99.
        self.throw_status = ATTACK_STATUS.READY
        self.last_throw_time_ms = -99.

        # Nombre de HP initial
        self.health_points = FIGHTER_HEALTH

    def draw(self, surface) -> None:
        """
        Affichage du personnage sur la surface 
        """
        # Combattant 
        if self.image and self.image_attack:
            if self.attack_status == ATTACK_STATUS.READY:
                image = self.image
                x_shift = 0
            else:
                image = self.image_attack
                x_shift = 0 if self.orientation == ORIENTATION.RIGHT else 100
            image = image if self.orientation == ORIENTATION.RIGHT else pygame.transform.flip(image, True, False)
            surface.blit(image, (self.rectangle.x - x_shift, self.rectangle.y))
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rectangle)

        # Pierre
        if self.rock:
            self.rock.draw(surface)

        # Hitbox de l'attaque (à retirer)
        #if self.attack_status != ATTACK_STATUS.READY:
        #    x_position = self.rectangle.x + FIGHTER_WIDTH if self.orientation == ORIENTATION.RIGHT else self.rectangle.x - FIGHTER_ATTACK_RANGE
        #    attack_hitbox_rectangle = pygame.Rect((x_position, self.rectangle.y, FIGHTER_ATTACK_RANGE, FIGHTER_HEIGHT))
        #    pygame.draw.rect(surface, (0, 255, 0), attack_hitbox_rectangle)

        # Affichage de l'impact
        if pygame.time.get_ticks() - self.impact_timer < IMPACT_DURATION:
            surface.blit(self.impact_image, self.impact_pos)
        
    def move(self, keys, target) -> None:
        """
        Déplacement du personnage
        """

        # reset de l'indication
        self.defense = False

        # Avec des touches de clavier : 
        if self.controller == None:
            # Mouvement à gauche dans la limite de l'écran
            if keys[self.keys["left"]]:
                self.rectangle.x = max(0., self.rectangle.x - FIGHTER_SPEED)
                self.defense = True if self.rectangle.x < target.rectangle.x else False
            # Mouvement à droite dans la limite de l'écran
            if keys[self.keys["right"]]:
                self.rectangle.x = min(SCREEN_WIDTH - FIGHTER_WIDTH, self.rectangle.x + FIGHTER_SPEED)
                self.defense = True if self.rectangle.x > target.rectangle.x else False
            
            # Si au sol
            if self.rectangle.y + FIGHTER_HEIGHT == FLOOR_HEIGHT:
                #Saut si le combatant touche le sol et touche jump
                if keys[self.keys["jump"]]:
                    self.vertical_speed = FIGHTER_JUMP_SPEED
                else:
                    self.vertical_speed = 0
            else:                
                self.vertical_speed += GRAVITY
        
        # Si on a une manette 
        else:
            # Mouvement à gauche dans la limite de l'écran
            if self.controller.get_axis(0) < -0.5:
                self.rectangle.x = max(0., self.rectangle.x - FIGHTER_SPEED)
                self.defense = True if self.rectangle.x < target.rectangle.x else False
            # Mouvement à droite dans la limite de l'écran
            elif self.controller.get_axis(0) > 0.5:
                self.defense = True if self.rectangle.x > target.rectangle.x else False
                self.rectangle.x = min(SCREEN_WIDTH - FIGHTER_WIDTH, self.rectangle.x + FIGHTER_SPEED)
            
            # Si au sol
            if self.rectangle.y + FIGHTER_HEIGHT == FLOOR_HEIGHT:
                #Saut si le combatant touche le sol et touche jump
                if self.controller.get_button(0):
                    self.vertical_speed = FIGHTER_JUMP_SPEED
                else:
                    self.vertical_speed = 0
            else:                
                self.vertical_speed += GRAVITY

        # Mise à jour de la position verticale
        self.rectangle.y = min(FLOOR_HEIGHT - FIGHTER_HEIGHT, self.rectangle.y + self.vertical_speed)

        # Mise à jour de l'orientation
        self.orientation = ORIENTATION.LEFT if self.rectangle.x > target.rectangle.x else ORIENTATION.RIGHT

        # Ajout du mouvement de la pierre si elle existe 
        if self.rock:
            destroy_rock = self.rock.update(self,target)
            if destroy_rock:
                # Affichage de l'impact
                self.impact_pos = (self.rock.x_position, self.rock.y_position)
                self.impact_timer = pygame.time.get_ticks()
                # Destruction
                self.rock = None

    def attack(self, keys, target) -> None:
        """
        Gestion de la phase d'attaque après le mouvement de chaque personnage
        """
        time_ms = pygame.time.get_ticks()

        #########
        # POING #
        #########
        
        # Reset du statut 
        if (self.attack_status != ATTACK_STATUS.READY):
            if (time_ms - self.last_attack_time_ms > FIGHTER_ATTACK_DURATION):
                self.attack_status = ATTACK_STATUS.READY
            else:
                self.attack_status = ATTACK_STATUS.COOLDOWN
        
        # Si on n'est disponible à attaquer et la touche est préssée
        if self.controller == None:
            if (self.attack_status == ATTACK_STATUS.READY) and keys[self.keys["attack"]]:
                # Mise à jour des indicateurs 
                self.attack_status = ATTACK_STATUS.ATTACKING
                self.last_attack_time_ms = pygame.time.get_ticks()
        else:
            if (self.attack_status == ATTACK_STATUS.READY) and self.controller.get_button(1):
                # Mise à jour des indicateurs 
                self.attack_status = ATTACK_STATUS.ATTACKING
                self.last_attack_time_ms = pygame.time.get_ticks()


        # Vérification que la hitbox de la cible 
        if (self.attack_status == ATTACK_STATUS.ATTACKING) and self.health_points:
            # hit box
            x_position = self.rectangle.x + FIGHTER_WIDTH if self.orientation == ORIENTATION.RIGHT else self.rectangle.x - FIGHTER_ATTACK_RANGE
            attack_hitbox_rectangle = pygame.Rect((x_position, self.rectangle.y, FIGHTER_ATTACK_RANGE, FIGHTER_HEIGHT))
            # Collision ? 
            if attack_hitbox_rectangle.colliderect(target.rectangle):
                target.attacked(FIGHTER_ATTACK_DAMAGE)
                self.impact_timer = pygame.time.get_ticks()
                self.impact_pos = (x_position + FIGHTER_ATTACK_RANGE / 2, self.rectangle.y - FIGHTER_HEIGHT / 8)
                self.impact_sound.play()

        #########
        # JETER #
        #########
                                
        if (self.throw_status != ATTACK_STATUS.READY):
            if (time_ms - self.last_throw_time_ms > FIGHTER_THROW_DURATION):
                self.throw_status = ATTACK_STATUS.READY
                self.rock = None
            else:
                self.throw_status = ATTACK_STATUS.COOLDOWN

        # Si on est disponible à attaquer et la touche est préssée
        if self.controller == None:
            if (self.throw_status == ATTACK_STATUS.READY) and keys[self.keys["throw"]] and abs(self.rectangle.x - target.rectangle.x) > FIGHTER_THROW_RANGE:
                # Mise à jour des indicateurs 
                self.throw_status = ATTACK_STATUS.ATTACKING
                self.last_throw_time_ms = pygame.time.get_ticks()
        else:
            if (self.throw_status == ATTACK_STATUS.READY) and self.controller.get_button(2) and abs(self.rectangle.x - target.rectangle.x) > FIGHTER_THROW_RANGE:
                # Mise à jour des indicateurs 
                self.throw_status = ATTACK_STATUS.ATTACKING
                self.last_throw_time_ms = pygame.time.get_ticks()

        # Lancer
        if (self.throw_status == ATTACK_STATUS.ATTACKING) and self.health_points:
            x_pos = self.rectangle.x if self.orientation == ORIENTATION.LEFT else self.rectangle.x + FIGHTER_WIDTH
            x_velocity = FIGHTER_THROW_SPEED if self.orientation == ORIENTATION.RIGHT else -FIGHTER_THROW_SPEED
            self.rock = Rock(x_pos, self.rectangle.y + FIGHTER_HEIGHT / 2, x_velocity, -FIGHTER_THROW_SPEED/3)

    def attacked(self, damage: int) -> None:
        """
        Mise à jour de la vie du personnage qui subit une attaque
        """
        # Le mouvement arrière divise les dégats par deux 
        if self.defense:
            self.health_points = max(0, self.health_points - damage / 2)
        else:
            self.health_points = max(0, self.health_points - damage)
        
    def heal(self, heal_points: int) -> None:
        """
        Réception de soins
        """
        self.health_points = min(FIGHTER_HEALTH, self.health_points + heal_points)
        

        

        
    