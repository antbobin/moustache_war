import pygame

from parameters import *

class Rock:

    def __init__(self, x_position, y_position, x_velocity, y_velocity) -> None:
        """
        Initialisé avec une position et une vitesse
        """
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

        self.init_time = pygame.time.get_ticks()

    def update(self, owner, target) -> bool:
        """
        Déplace la pierre et vérifie si on touche 
        """

        # Mise à jour de la vitesse verticale 
        self.y_velocity += GRAVITY/2
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        
        # Logique de rebond
        if self.y_position > FLOOR_HEIGHT : 
            self.y_velocity *= -1
            self.y_position = FLOOR_HEIGHT - (self.y_position - FLOOR_HEIGHT)

        # Vérification de l'impact sur l'autre combattant
        attack_hitbox_rectangle = pygame.Rect((self.x_position, self.y_position, ROCK_RADIUS*2 , ROCK_RADIUS*2))
        # Collision ? 
        if attack_hitbox_rectangle.colliderect(target.rectangle):
            target.attacked(FIGHTER_THROW_DAMAGE)
            # On indique qu'il faut détruire l'objet
            return True
        
        # Vérification de l'impact sur l'autre pierre
        if target.rock:
            other_rock_hitbox = pygame.Rect((target.rock.x_position, target.rock.y_position, ROCK_RADIUS*2 , ROCK_RADIUS*2))
            if attack_hitbox_rectangle.colliderect(other_rock_hitbox):
                # Impact. Gain au tir le plus récent
                if self.init_time > target.rock.init_time:
                    owner.heal(ROCK_HEAL)
                else:
                    target.heal(ROCK_HEAL)
                # Destruction des pierres
                target.rock = None
                return True
        
        return False

    def draw(self, surface):
        """
        Affichage de la pierre. Il faudrait la faire tourner in fine 
        """

        pygame.draw.circle(surface, COLOR.BROWN, (self.x_position, self.y_position), ROCK_RADIUS)


