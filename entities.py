import pygame, random, math, numpy as np
from settings import *


# Game objects
class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, loc=[0, 0]):
        super().__init__()
        self.image = image
        self.game = game
        self.rect = self.image.get_rect()
        self.move_to(loc)
        self.on_platform = False
        self.num = 0
        self.at_edge = False
        
    def move_to(self, loc):
        self.rect.centerx = loc[0] * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = loc[1] * GRID_SIZE + GRID_SIZE // 2
        
    def apply_gravity(self):
        self.vy += self.game.gravity

    def reverse(self):
        if not self.name == "player":
            self.vx *= -1

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def move_and_check_platforms(self):
        self.rect.y += self.vy
        self.on_platform = False

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        hits_1 = pygame.sprite.spritecollide(self, self.game.floating_platforms, False)
        for platform in hits:
            if self.vy < 0:
                self.rect.top = platform.rect.bottom
            elif self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.on_platform = True
        for platform in hits_1:
            if platform.vx > 0 or platform.vx < 0:
                self.rect.x += platform.vx
            if self.vy < 0:
                self.rect.top = platform.rect.bottom
            elif self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.on_platform = True
        if len(hits) > 0 or len(hits_1) > 0:
            if self.name == "player" and self.vy > 20:
                    self.game.screen_shake = self.vy - 10
                    fall_snd.play()
            self.vy = 0
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        hits_1 = pygame.sprite.spritecollide(self, self.game.floating_platforms, False)
        if self.name == "player":
            self.can_wall_jump_left = False
            self.can_wall_jump_right = False
        for platform in hits:
            if self.vx < 0:
                self.rect.left = platform.rect.right
                if self.name == "player" and not self.on_platform and not self.vy == 0:
                    self.wall_slide()
                    self.game.can_control = False
                    self.can_wall_jump_right = True
                    self.facing_right = False
            elif self.vx > 0:
                self.rect.right = platform.rect.left
                if self.name == "player" and not self.on_platform and not self.vy == 0:
                    self.wall_slide()
                    self.game.can_control = False
                    self.can_wall_jump_left = True
                    self.facing_right = True
        for platform in hits_1:
            if self.vx < 0:
                self.rect.left = platform.rect.right
                if self.name == "player" and not self.on_platform and not self.vy == 0:
                    self.wall_slide()
                    self.game.can_control = False
                    self.can_wall_jump_right = True
                    self.facing_right = False
            elif self.vx > 0:
                self.rect.right = platform.rect.left
                if self.name == "player" and not self.on_platform and not self.vy == 0:
                    self.wall_slide()
                    self.game.can_control = False
                    self.can_wall_jump_left = True
                    self.facing_right = True
        if len(hits) > 0 or len(hits_1) > 0:
            self.reverse()
        elif len(hits) == 0 and self.name == "player" or len(hits_1) == 0 and self.name == "player":
            self.wall_sliding = False
            self.game.can_control = True
            self.can_wall_jump_left = False
            self.can_wall_jump_right = False
        
    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        self.at_edge = True
        for platform in hits:
            if self.vx < 0:
                if self.rect.left >= platform.rect.left:
                    self.at_edge = False
            elif self.vx > 0:
                if self.rect.right <= platform.rect.right:
                    self.at_edge = False
        if self.at_edge:
            if self.name == "mouse_1":
                if self.move_direction == RIGHT:
                    self.move_direction = LEFT
                elif self.move_direction == LEFT:
                    self.move_direction = RIGHT
            elif self.name == "bowman":
                self.can_move_back = False
            self.reverse()

    def check_world_edges(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > self.game.world_width:
            self.rect.right = self.game.world_width
            self.reverse()
        if self.rect.top > self.game.world_height:
            self.health = 0
        
class AnimatedEntity(Entity):
    def __init__(self, game, images, loc=[0, 0]):
        super().__init__(game, images[0], loc)
        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 7
        
    def set_image_list(self):
        self.images = self.images
        
    def animate(self):
        self.set_image_list()
        self.ticks += 1
        if self.ticks % self.animation_speed == 0:
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.image = self.images[self.image_index]
            self.image_index += 1
        if self.game.should_advance and self.name == "player":
            self.image_scale_1 -= 1
            self.image_scale_2 -= 1
            self.image_scale_3 -= 2
            self.vy -= 1.01
            self.image = pygame.transform.scale(self.image, (self.image_scale_1, self.image_scale_2))
            self.image = pygame.transform.rotate(self.image, self.image_scale_3)


# ---------- ITEMS / NPC'S ---------- #

class Orb(Entity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        

class Merchant(AnimatedEntity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = 0
        self.vy = 0
        self.name = "merchant"
        self.health = 5
    
    def check_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.player, False)
        if len(hits) > 0:
            self.game.can_show_shop = True
        else:
            self.game.can_show_shop = False
            self.game.should_show_shop = False
    
    def update(self):
        self.animate()
        self.move_and_check_platforms()
        self.apply_gravity()
        self.check_collisions()
    
class Slash(AnimatedEntity):
    def __init__(self, game, image, loc, vx, from_x, from_y, type, strength):
        super().__init__(game, image, loc)
        self.vy = 0
        self.vx = vx
        self.rect.centerx = from_x
        self.rect.centery = from_y
        self.name = "slash"
        self.type = type
        self.health = strength
        self.animation_speed = 1
        self.timer = 5
    
    def set_image_list(self):
        if self.type == "1":
            if self.vx > 0:
                self.images = player_slash_1_rt_imgs
            elif self.vx < 0:
                self.images = player_slash_1_lt_imgs
        elif self.type == "2":
            if self.vx > 0:
                self.images = player_slash_2_rt_imgs
            elif self.vx < 0:
                self.images = player_slash_2_lt_imgs
        elif self.type == "3":
            if self.vx > 0:
                self.images = player_slash_3_rt_imgs
            elif self.vx < 0:
                self.images = player_slash_3_lt_imgs
    
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
    
    # Check collisions with platforms and enemies
    def check_collisions(self):
        self.game.should_draw_particles = False
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if len(hits) > 0:
            for enemy in hits:
                if enemy.is_alive and enemy.health > 0:
                    self.health -= 1
                    enemy.health -= 1
                    enemy.hurt = True
                    enemy.knockback()
                    self.game.screen_shake = 5

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        hits1 = pygame.sprite.spritecollide(self, self.game.floating_platforms, False)
        if len(hits) > 0 or len(hits1) > 0:
            offset_x, offset_y = self.game.get_offsets()

            #                        Velocity x,                   Velocity y
            particle_speed = [random.randint(-10, 10), random.randint(-30, 15)/10 - 1.5]
            particle_size = random.randint(2, 5)
            if self.vx > 0:
                location = [self.rect.right - offset_x, self.rect.centery - offset_y]
            else:
                location = [self.rect.left - offset_x, self.rect.centery - offset_y]

            self.game.spark_particles.append([location, particle_speed, particle_size])
            # Make the slash slower when it hits the wall.
            self.vx = 0.65 * self.vx
            # Shake screen.
            self.game.screen_shake = 2

    def animate(self):
        self.set_image_list()
        self.ticks += 1
        if self.ticks % self.animation_speed == 0:
            self.image = self.images[self.image_index]
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.kill()
    
    def live(self):
        if self.health > 0:
            pass
        else:
            self.kill()
    
    def update(self):
        self.animate()
        self.move()
        self.check_collisions()
        self.live()

class Arrow(Entity):
    def __init__(self, game, image, loc, x, y, direction):
        super().__init__(game, image, loc)
        self.vx = 4.5 * direction
        self.vy = 0
        self.health = 1
        self.rect.centerx = x
        self.rect.centery = y

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
    
    def check_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        hits2 = pygame.sprite.spritecollide(self, self.game.player, False)
        hits3 = pygame.sprite.spritecollide(self, self.game.player_slashes, False)
        if len(hits) > 0 or len(hits3) > 0:
            self.kill()
        if len(hits2) > 0:
            self.health -= 1
        
    def live(self):
        if self.health > 0:
            pass
        else:
            self.kill()

    def update(self):
        self.move()
        self.check_collisions()
        self.live()

class Counter(Entity):
    def __init__(self, game, image, loc, x, y):
        super().__init__(game, image, loc)
        offset_x, offset_y = self.game.get_offsets()
        self.rect.centerx = x + offset_x
        self.rect.centery = y + offset_y
        self.timer = 50
    
    def move_to(self, loc):
        pass

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
        # self.apply_gravity()
        # self.move_and_check_platforms()

class EnemyDrop_Coin(Entity):
    def __init__(self, game, image, loc, x, y):
        super().__init__(game, image, loc)
        self.vx = 0
        self.vy = -10
        self.rect.centerx = x
        self.rect.centery = y
        self.name = "enemydrop_coin"
    
    def move_to(self, loc):
        pass 
    
    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()

    
# ---------- ENEMIES ---------- #

class Enemy(AnimatedEntity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.counter = 25
        self.speed = 2
        self.should_stall = False
        self.death_counter = 10
        self.knock_counter = 1
        self.blood_location = self.rect.centerx, self.rect.centery
        self.hurt = False
        self.attacking = False
        self.coin_y = self.rect.centery
        self.hero_is_close = False
        self.facing_left = True
        self.facing_right = False
        self.move_direction = STAY
        
    # Set variables facing_right and facing_left to true or false based on velocity x
    def set_direction(self):
        if self.vx < 0:
            self.facing_left = True
            self.facing_right = False
        elif self.vx > 0:
            self.facing_left = False
            self.facing_right = True
    
    # Add a location for a foglight to appear at and remove it if enemy dies
    def create_spotlights(self):
        if not self.is_alive:
            self.game.fog_lights.append([None, None, self, LIGHT_RADIUS])
        else:
            self.game.fog_lights.append([None, None, self, LIGHT_RADIUS])
    
    def remove_spotlights(self):
        for light in self.game.fog_lights:
            if light[2] == self:
                self.game.fog_lights.remove(light)
    
    def live(self):
        if self.health <= 0:
            self.is_alive = False
        if not self.is_alive:
            if self.death_counter > 0:
                self.death_counter -= 1
                self.vx = 0
                self.knockback()
            else:
                self.vx = 0
                if self.image_index >= len(self.images):
                    self.remove_spotlights()
                    self.kill()
                    x = self.rect.centerx
                    y = self.rect.centery
                    loc = [x, y]
                    c = EnemyDrop_Coin(self.game, coin_img, loc, x, y)
                    self.game.enemy_drops.add(c)
                    self.game.all_sprites.add(c)

    def update(self):
        self.live()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()
        self.set_direction()
        
class Mouse_1(Enemy):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = 0
        self.vy = 0
        self.speed = 3
        self.health = 2
        self.score = 1
        self.attack_counter = 0
        self.name = "mouse_1"
        self.is_alive = True
        self.animation_speed = 7
        self.move_time = random.randint(160, 175)
        self.move_counter = self.move_time
        self.shot = False
        self.hurt = False
        self.hurt_tick = 3
        self.icon = guard_icon_img
        self.hero_is_close = False
        self.is_docile = self.game.level == 1
    
    def determine_direction(self):
        if not self.game.gameplay_paused:
            rand = random.randint(0, 3)
            if self.is_docile:
                self.move_direction = STAY
            elif rand == 0:
                self.move_direction = LEFT
            elif rand == 1:
                self.move_direction = RIGHT
            else:
                self.move_direction = STAY

    def move(self):
        if self.move_counter > 0:
            self.move_counter -= 1
        elif self.move_counter == 0:
            self.move_counter = self.move_time
            self.determine_direction()
        if self.move_direction == STAY:
            self.stop()
        elif self.move_direction == RIGHT:
            self.go_right()
        elif self.move_direction == LEFT:
            self.go_left()

    def stop(self):
        if self.vx > 0:
            self.vx -= 0.5
        elif self.vx < 0:
            self.vx += 0.5
    
    def go_right(self):
        if self.vx < self.speed:
            self.vx += 0.5
        elif self.vx > self.speed:
            self.vx -= 0.5
        elif self.vx == self.speed:
            self.vx = self.speed

    def go_left(self):
        if self.vx < -self.speed:
            self.vx += 0.5
        elif self.vx > -self.speed:
            self.vx -= 0.5
        elif self.vx == -self.speed:
            self.vx = -self.speed

    def set_image_list(self):
        if self.is_alive:
            if self.facing_right:
                if self.hurt:
                    self.images = guard_hurt_rt_imgs
                    self.hurt_tick -= 1
                    if self.hurt_tick == 0:
                        self.hurt = False
                        self.hurt_tick = 3
                elif self.attacking:
                    self.images = guard_attack_rt_imgs
                elif self.vx > 0:
                    self.images = guard_walk_rt_imgs
                else:
                    self.images = guard_idle_rt_imgs
            elif self.facing_left:
                if self.hurt:
                    self.images = guard_hurt_lt_imgs
                    self.hurt_tick -= 1
                    if self.hurt_tick == 0:
                        self.hurt = False
                        self.hurt_tick = 3
                elif self.attacking:
                    self.images = guard_attack_lt_imgs
                elif self.vx < 0:
                    self.images = guard_walk_lt_imgs
                else:
                    self.images = guard_idle_lt_imgs

        # Draw particles when mouse dies, to look like blood.
        else:
            if self.facing_right:
                offset_x, offset_y = self.game.get_offsets()
                self.game.blood_particles.append([[self.rect.centerx - offset_x, self.rect.centery - offset_y], [random.randint(-5, 5), random.randint(-30, 15)/10 - 1.5], random.randint(2, 5)])
                self.images = guard_die_rt_imgs
            else:
                offset_x, offset_y = self.game.get_offsets()
                self.game.blood_particles.append([[self.rect.centerx - offset_x, self.rect.centery - offset_y], [random.randint(-5, 5), random.randint(-30, 15)/10 - 1.5], random.randint(2, 5)])
                self.images = guard_die_lt_imgs
    
    def check_distance(self):
        self.distancex = self.game.hero.rect.centerx - self.rect.centerx
        self.distancey = self.game.hero.rect.centery - self.rect.centery
        if -96 < self.distancex < 96 and -96 < self.distancey < 96:
            self.hero_is_close = True
        else:
            self.hero_is_close = False

    # Knockback enemy based on if player is left or right of the enemy
    def knockback(self):
        if self.knock_counter > 0:
            self.knock_counter -= 1
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.vx -= self.speed * 2
                self.vy -= 7
                self.image_index = 0
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.vx += self.speed * 2
                self.vy -= 7
                self.image_index = 0
    
    def knockback_check(self):
        hits = pygame.sprite.spritecollide(self, self.game.player, False)
        if len(hits) > 0:
            for player in hits:
                if player.attacking and not self.game.hero.has_sword_equipped:
                    self.knockback()
                    self.hurt = True
                else:
                    self.vx *= -1
    
    def attack_check(self, hero_is_close):
        if hero_is_close:
            if self.attack_counter > 0:
                self.attacking = False
                self.attack_counter -= 1
            else:
                if self.image_index >= len(self.images):
                    self.attack_counter = 50
                    self.vx = 0
                self.attacking = True
        else:
            self.attack_counter = 0
            self.attacking = False

    # Check collisions with hero, set enemy to attacking, and knockback or change to hurt image if hero is attacking
    def check_player(self):
        self.check_distance()
        self.attack_check(self.hero_is_close)
        self.knockback_check()

    def update(self):
        super().update()
        self.move()
        self.apply_gravity()
        self.check_platform_edges()
        self.check_player()

class Bowman(Enemy):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = 0
        self.vy = 0
        self.health = 2
        self.move_back_counter = 25
        self.attack_counter = 50
        self.speed = 3
        self.name = "bowman"

        self.is_alive = True
        self.shooting = False
        self.can_move_back = False
        self.move_direction = STAY
        self.icon = bowman_icon_img
    
    def move_back(self):
        self.vx = -self.speed
    
    def stand_idle(self):
        if self.vx < 0:
            self.vx += 0.5
        elif self.vx > 0:
            self.vx -= 0.5
    
    def move_right(self):
        if self.vx > self.speed:
            self.vx -= 0.5
        elif self.vx < self.speed:
            self.vx += 0.5
        else:
            self.vx = self.speed
    
    def move_left(self):
        if self.vx > -self.speed:
            self.vx -= 0.5
        elif self.vx < -self.speed:
            self.vx += 0.5
        else:
            self.vx = -self.speed

    def move(self):
        if self.move_direction == RIGHT:
            self.move_right()
        elif self.move_direction == LEFT:
            self.move_left()
        else:
            self.stand_idle()
    
    def reset_directions(self):
        self.move_direction = STAY
    
    def get_distance_from_player(self):
        distancex = self.game.hero.rect.centerx - self.rect.centerx
        distancey = self.game.hero.rect.centery - self.rect.centery

        return distancex, distancey
    
    # Returns two variables: in_range, is_too_close. Either are returned true based on far away the player 
    def in_range(self):

        distancex, distancey = self.get_distance_from_player()

        in_range, is_too_close = False, False
        range = 512
        close = 256

        if self.game.should_show_cave_bg:
            range /= 2
            close /= 2

        in_range = -range < distancex < range and -32 < distancey < 32
        is_too_close = -close < distancex < close and -32 < distancey < 32

        return in_range, is_too_close
    
    # Randomly back up for a set amount of time. (Walk opposite way of player)
    def back_up(self):
        # Has a 1 / 100 chance to move back again and reset move_back_counter to 25.
        if not self.can_move_back:
            rand = random.randint(0, 100)
            if rand == 0:
                self.move_back_counter = 25
        # Set move back to true while move_back_counter is greater than zero.
        if self.move_back_counter > 0:
            self.move_back_counter -= 1
            self.can_move_back = True
        # Set can_move_back to false because move_back_counter equals zero.
        else:
            self.reset_directions()
            self.can_move_back = False
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.facing_right = True
                self.facing_left = False
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.facing_left = True
                self.facing_right = False
        # Walk away based on hero position.
        if self.can_move_back:
            self.reset_directions()
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.move_direction = LEFT
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.move_direction = RIGHT
    
    def shoot(self):
        if self.game.hero.rect.centerx > self.rect.centerx:
            direction = 1
        else:
            direction = -1
        y = self.rect.centery
        x = self.rect.right - 24
        loc = [x, y]
        a = Arrow(self.game, arrow_lt_img, loc, x, y, direction)
        self.game.enemy_attacks.add(a)
        self.game.all_sprites.add(a)


    def act(self):
        in_range, is_too_close = self.in_range()

        if is_too_close:
            self.shooting = False
            self.back_up()
        elif in_range:
            self.reset_directions()
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.facing_right = True
                self.facing_left = False
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.facing_left = True
                self.facing_right = False
            if self.attack_counter > 0:
                self.attack_counter -= 1
                self.shooting = False
            else:
                self.shooting = True
                if self.image_index >= len(self.images):
                    self.attack_counter = 55
                    self.shoot()
        else:
            self.shooting = False

    def set_image_list(self):
        if self.is_alive:
            if self.facing_right:
                if self.vx > 0:
                    self.images = bowman_walk_rt_imgs
                elif self.shooting:
                    self.images = bowman_attack_rt_imgs
                else:
                    self.images = bowman_idle_rt_imgs
            elif self.facing_left:
                if self.vx < 0:
                    self.images = bowman_walk_lt_imgs
                elif self.shooting:
                    self.images = bowman_attack_lt_imgs
                else:
                    self.images = bowman_idle_lt_imgs
                    
        else:
            if self.facing_right:
                offset_x, offset_y = self.game.get_offsets()
                self.game.blood_particles.append([[self.rect.centerx - offset_x, self.rect.centery - offset_y], [random.randint(-5, 5), random.randint(-30, 15)/10 - 1.5], random.randint(2, 5)])
                self.images = bowman_die_rt_imgs
            else:
                offset_x, offset_y = self.game.get_offsets()
                self.game.blood_particles.append([[self.rect.centerx - offset_x, self.rect.centery - offset_y], [random.randint(-5, 5), random.randint(-30, 15)/10 - 1.5], random.randint(2, 5)])
                self.images = bowman_die_lt_imgs

    # Knockback enemy based on if player is left or right of the enemy
    def knockback(self):
        if self.knock_counter > 0:
            self.knock_counter -= 1
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.vx -= self.speed * 2
                self.vy -= 7
                self.image_index = 0
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.vx += self.speed * 2
                self.vy -= 7
                self.image_index = 0
    
    def update(self):
        super().update()
        self.act()
        self.move()
        self.check_platform_edges()
        self.animate()
        self.apply_gravity()

class Elite(Enemy):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.name = "elite"
        self.vx = 0
        self.vy = 0
        self.health = 3

        self.is_alive = True

        self.icon = elite_icon_img
    
    def set_image_list(self):
        self.images = elite_idle_rt_imgs

    # Knockback enemy based on if player is left or right of the enemy
    def knockback(self):
        if self.knock_counter > 0:
            self.knock_counter -= 1
            if self.game.hero.rect.centerx > self.rect.centerx:
                self.vx -= self.speed * 2
                self.vy -= 7
                self.image_index = 0
            elif self.game.hero.rect.centerx < self.rect.centerx:
                self.vx += self.speed * 2
                self.vy -= 7
                self.image_index = 0

    
    def update(self):
        super().update()
        self.check_platform_edges()
        self.animate()
        self.apply_gravity()



# ---------- OTHER ENTITIES ---------- #

class Portal(AnimatedEntity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.name = "portal"
    
    def make_player_float_around(self):
        if self.game.hero.rect.centerx > self.rect.centerx:
            self.game.hero.vx -= 1
        elif self.game.hero.rect.centerx < self.rect.centerx:
            self.game.hero.vx += 1
            
        if self.game.hero.rect.centery > self.rect.centery:
            self.game.hero.vy -= 0.5
        elif self.game.hero.rect.centery < self.rect.centery:
            self.game.hero.vy += 0.5
    
    def check_collisions(self):
        hits = pygame.sprite.spritecollide(self, self.game.player, False)
        if hits:
            self.game.player_hitting_portal = True
            self.make_player_float_around()
        else:
            self.game.player_hitting_portal = False
    
    def update(self):
        self.check_collisions()
        self.animate()

class FloatingPlatform(Entity):
    def __init__(self, game, image, loc, type, min, max):
        super().__init__(game, image, loc)
        self.direction = type
        if self.direction == 1:
            self.vx = 0
            self.vy = -1
        elif self.direction == 2:
            self.vx = 0.1
            self.vy = 0
        self.name = "floating_platform"
        
        self.min_x = self.rect.centerx - min
        self.max_x = self.rect.centerx - max
        self.min_y = self.rect.centery - min
        self.max_y = self.rect.centery + max
    
    def bounce(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.direction == 1:
            if self.rect.centery < self.min_y:
                self.vy += 0.2
                if self.vy == 0:
                    self.vy = -self.vy
            elif self.rect.centery > self.max_y:
                self.vy -= 0.2
                if self.vy == 0:
                    self.vy = -self.vy
        else:
            if self.rect.centerx < self.min_x:
                self.vx += 0.1
                if self.vx == 0:
                    self.vx = -self.vx
            elif self.rect.centerx > self.max_x:
                self.vx -= 0.1
                if self.vx == 0:
                    self.vx = -self.vx

    def update(self):
        self.bounce()
        self.check_world_edges()


class Bullet(Entity):
    def __init__(self, game, image, loc, direction, from_x, from_y):
        super().__init__(game, image, loc)
        self.speed_1 = 10 * direction
        self.name = "bullet"
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = from_x
        self.rect.centery = from_y
        self.speed = 15
        if self.game.has_mouse:
            to_x, to_y = pygame.mouse.get_pos()
            offset_x, offset_y = self.game.get_offsets()
            dx = from_x - to_x - offset_x
            dy = from_y - to_y - offset_y
            hyp = math.sqrt(dx**2 + dy**2)
            self.vx = (dx * self.speed) / hyp
            self.vy = (dy * self.speed) / hyp
            angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(self.image, -angle + 180)
        
    def update(self):
        self.check_world_edges()
        if self.game.has_mouse:
            self.rect.x -= self.vx
            self.rect.y -= self.vy
        else:
            self.rect.centerx += self.speed_1
        objects = pygame.sprite.spritecollide(self, self.game.all_sprites_except_player, False)
        if len(objects) > 0:
            for thing in objects:
                if thing.category == "enemy":
                    if thing.is_alive:
                        if thing.health == 1:
                            thing.shot = True
                            thing.is_alive = False
                        thing.health -= 1
                        self.kill()
                    else:
                        pass
                else:
                    self.kill()

class WalkThru(Entity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.name = "walkthru"
        self.category = "walkthru"

class AnimatedWalkThru(AnimatedEntity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.name = "walkthru"
        self.category = "walkthru"
    
    def update(self):
        self.animate()

class Platform(Entity):
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.name = "platform"
        self.category = "platform"

