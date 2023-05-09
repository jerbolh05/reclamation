from re import I
import pygame, random, math
from settings import *
from entities import *

# ---------- PLAYER ---------- #

class Player(AnimatedEntity):
    def __init__(self, game, images, name):
        super().__init__(game, images)
        self.vx = 0
        self.vy = 0
        self.walk_speed = 4
        self.slide_speed = 5
        self.damage = 1
        self.sword_dmg = 1
        self.jump_power = 15
        self.score = 0
        self.money = 5
        self.health = 4
        self.loc = [0, 0]
        self.loc_x = 0
        self.loc_y = 0
        self.image_index = 0
        self.escape_time = 30
        self.angle = 0
        self.fromx = 0
        self.fromy = 0
        self.wall_jump_counter = 20
        self.wall_slide_counter = 15
        self.image_scale_1 = 58
        self.image_scale_2 = 58
        self.image_scale_3 = 360
        self.has_invis_potion = 0
        self.orig_scale = [self.image.get_width, self.image.get_height]

        self.sliding = False
        self.attacking = False
        self.on_platform = False
        self.facing_right = True
        self.walking = False
        self.at_end = False
        self.at_beginning = False
        self.restarting = False
        self.can_wall_jump_left = False
        self.can_wall_jump_right = False
        self.wall_jumping_left = False
        self.wall_jumping_right = False
        self.wall_sliding = False
        self.wall_slide_direction = 0
        self.has_sword_equipped = False
        self.has_bow_equipped = False
        self.switching_to_sword = False
        self.removing_sword = False
        self.can_attack = True
        self.can_gravity = True

        self.name = name
        self.attack_method = "blank"
        self.attacking_method = "0"

        self.current_action = "idle"

        
    def walk_left(self):
        if self.vx == -self.walk_speed:
            self.vx = -self.walk_speed
        elif self.vx > -self.walk_speed:
            self.vx -= 0.5
        elif self.vx < -self.walk_speed:
            self.vx += 0.5
        self.walking = True
        self.facing_right = False
        self.crouching = False
        self.wall_sliding = False
        self.shaking = False
        if self.on_platform:
            self.jumps_remaining = 2
        
    def walk_right(self):
        if self.vx == self.walk_speed:
            self.vx = self.walk_speed
        elif self.vx > self.walk_speed:
            self.vx -= 0.5
        elif self.vx < self.walk_speed:
            self.vx += 0.5
        self.walking = True
        self.facing_right = True
        self.crouching = False
        self.wall_sliding = False
        self.shaking = False
        if self.on_platform:
            self.jumps_remaining = 2
    
    def crouch(self):
        if self.on_platform:
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
            self.crouching = True
            self.sliding = False
        self.walking = False
        self.attacking = False
        self.wall_sliding = False
        self.shaking = False
        if self.on_platform:
            self.jumps_remaining = 2
    
    def set_slide(self):
        self.image_index = 0
        self.sliding = True
    
    def jump(self):
        self.jumping = True
        self.vy = 0
        self.vy -= 1 * self.jump_power
    
    def wall_slide(self):
        self.wall_sliding = True
        self.vy = self.vy // 2
    
    # Add x2 or x3 counter when doing a double or triple attack
    def add_counter(self, image, offset_x, offset_y):
        if self.facing_right:
            x = self.rect.centerx - offset_x - 50
            y = self.rect.centery - offset_y - 25
        else:
            x = self.rect.centerx - offset_x + 50
            y = self.rect.centery - offset_y - 25
        loc = [x, y]
        c = Counter(self.game, image, loc, x, y)
        self.game.all_sprites.add(c)
        self.game.counters.add(c)
    
    # Add a player slash when hitting with the sword
    def add_slash(self):
        if self.facing_right:
            self.vx = -5
            y = self.rect.centery
            x = self.rect.right - 24
            loc = [x, y]
            direction = 6.5
            strength = int(self.sword_dmg)
            s = Slash(self.game, player_slash_1_rt_imgs, loc, direction, x, y, self.attacking_method, strength)
            self.game.player_slashes.add(s)
            self.game.all_sprites.add(s)
            sword_swoosh_snd.play()
        elif not self.facing_right:
            self.vx = 5
            y = self.rect.centery
            x = self.rect.left + 12
            loc = [x, y]
            direction = -5.5
            strength = int(self.sword_dmg)
            s = Slash(self.game, player_slash_1_lt_imgs, loc, direction, x, y, self.attacking_method, strength)
            self.game.player_slashes.add(s)
            self.game.all_sprites.add(s)
            sword_swoosh_snd.play()
    
    def attack(self):
        offset_x, offset_y = self.game.get_offsets()
        self.attacking = True
        self.attack_method = self.game.hero_attack

        if self.attack_method == "punch_1":
            self.attacking_method = "1"
            self.image_index = 0
        elif self.attack_method == "punch_2":
            self.attacking_method = "2"
            self.image_index = 0
        elif self.attack_method == "punch_3":
            self.attacking_method = "3"
            self.image_index = 0
        elif self.attack_method == "sword_slash_1":
            self.attacking_method = "1"
            self.image_index = 0
        elif self.attack_method == "sword_slash_2":
            self.attacking_method = "2"
            self.image_index = 0
            self.add_counter(counterx2_img, offset_x, offset_y)
        elif self.attack_method == "sword_slash_3":
            self.attacking_method = "3"
            self.image_index = 0
            self.add_counter(counterx3_img, offset_x, offset_y)

        if self.has_sword_equipped and self.attacking and self.can_attack:
            self.add_slash()
                    
    def wall_jump_right(self):
        print("wall jump right")
        self.facing_right = True
        self.wall_jumping_right = True
        self.wall_jumping_left = False

    def wall_jump_left(self):
        print("wall jump left")
        self.facing_left = False
        self.wall_jumping_right = False
        self.wall_jumping_left = True
    
    # Switch from sword to no sqord
    def switch_weapons(self, weapon):
        if weapon == "sword":
            if self.has_sword_equipped:
                self.game.should_remove_sword_lines = True
                self.game.should_show_sword_lines = False
                self.switching_to_sword = False
                self.removing_sword = True
                self.image_index = 0
            else:
                self.game.should_remove_sword_lines = False
                self.game.should_show_sword_lines = True
                self.has_sword_equipped = True
                self.switching_to_sword = True
                self.image_index = 0

    def stop(self):

        # To slow down instead of coming to a harsh stop
        if not self.sliding and not self.walking and not self.vx == 0:
            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5
        
        # For after attacking or sliding
        if not self.restarting and self.image_index >= len(self.images):
            self.image_index = 0
            self.sliding = False
            self.attacking = False
        
        self.jumping = False
        self.walking = False
        self.crouching = False
        if self.vy == 0:
            self.wall_sliding = False
        self.shaking = False
        if self.on_platform:
            self.jumps_remaining = 2
    
    def is_alive(self):
        return self.health > 0
    
    def figure_angle(self):
        pass

    # Check if enemy is to_right of player or not, and then knockback the player
    def knockback(self, enemy_pos):
        to_right = self.rect.centerx < enemy_pos
        if to_right:
            self.vx -= 10
            self.vy -= 5
        else:
            self.vx += 10
            self.vy -= 5
    
    # Check collisions with entities
    def check_collisions(self):
        
        # Check collisions with portal
        hits = pygame.sprite.spritecollide(self, self.game.portals, False)
        if hits:
            self.can_gravity = False
        else:
            self.can_gravity = True

        # Check for enemies and knockback or take away health
        if self.escape_time == 0:
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            for enemy in hits:
                if enemy.is_alive:
                    if self.attacking and not self.has_sword_equipped:
                        enemy.health -= 1
                        enemy.hurt = True
                    else:
                        offset_x, offset_y = self.game.get_offsets()
                        self.game.blood_particles.append([[self.rect.centerx - offset_x, self.rect.centery - offset_y], [random.randint(-5, 5), random.randint(-30, 15)/10 - 1.5], random.randint(2, 5)])
                        self.escape_time = 30
                        self.knockback(enemy.rect.centerx)
                        self.game.screen_shake = 25
        if self.escape_time > 0:
            self.escape_time -= 1
        
        hits = pygame.sprite.spritecollide(self, self.game.enemy_drops, False)
        if hits:
            for drop in hits:
                if drop.name == "enemydrop_coin":
                    self.score += 50
                    self.money += 1
                    drop.kill()
                    pickup_coin_snd.play()
    
    # Play walking sounds around every 4 frames or so.
    def play_walk_sounds(self):
        if self.on_platform and not self.vx == 0 and not self.sliding:
            walk_time = 24
            if self.ticks % walk_time == 0:
                walk_snd.play()

    # Functions to be run every frame  
    def run_update_functions(self):

        # print("LEFT: " + str(self.can_wall_jump_left))
        # print("RIGHT: " + str(self.can_wall_jump_right))

        self.play_walk_sounds()

        # Set self loc_x and loc_y variables
        x = self.rect.centerx / 64
        y = self.rect.centery / 64
        self.loc = [round(x, 1), round(y, 1)]
        self.loc_x = x
        self.loc_y = y
        
        # Wall jump to left or right 
        if self.wall_jumping_left:
            if self.wall_jump_counter == 20:
                self.vy = -1 * self.jump_power
                self.vx -= 10
            self.wall_jump_counter -= 1
            if self.wall_jump_counter == 0:
                self.wall_jump_counter = 20
                self.wall_jumping_left = False
        elif self.wall_jumping_right:
            if self.wall_jump_counter == 20:
                self.vy = -1 * self.jump_power
                self.vx += 10
            self.wall_jump_counter -= 1
            if self.wall_jump_counter == 0:
                self.wall_jump_counter = 20
                self.wall_jumping_right = False
        elif self.sliding:
            if self.facing_right:
                if self.vx == self.slide_speed:
                    self.vx = self.slide_speed
                elif self.vx > self.slide_speed:
                    self.vx -= 0.5
                elif self.vx < self.slide_speed:
                    self.vx += 0.5
            elif not self.facing_right:
                if self.vx == -self.slide_speed:
                    self.vx = -self.slide_speed
                elif self.vx > -self.slide_speed:
                    self.vx -= 0.5
                elif self.vx < -self.slide_speed:
                    self.vx += 0.5
            if self.image_index >= len(self.images):
                self.sliding = False

        # To stop when you attack
        elif self.attacking:
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
            else:
                self.vx = 0
                
        if self.game.has_mouse:
            if not self.wall_sliding:
                mx, my = pygame.mouse.get_pos()
                offset_x, offset_y = self.game.get_offsets()
                self.fromx = self.rect.centerx
                self.fromy = self.rect.centery
                if mx > self.rect.centerx - offset_x:
                    self.facing_right = True
                else:
                    self.facing_right = False

    
    # Set images based on what the player is doing
    def set_image_list(self):
        self.animation_speed = 7
        if self.facing_right:
            if self.wall_jumping_right:
                self.images = player_wall_jump_rt_imgs
            elif self.wall_sliding:
                self.images = player_wall_slide_rt_imgs
            elif self.has_sword_equipped:
                if self.switching_to_sword:
                    self.images = player_sword_draw_rt_imgs
                    if self.image_index >= len(self.images) - 1:
                        self.switching_to_sword = False
                elif self.removing_sword:
                    self.images = player_sword_sheathe_rt_imgs
                    if self.image_index >= len(self.images) - 1:
                        self.removing_sword = False
                        self.has_sword_equipped = False
                elif self.attacking:
                    self.animation_speed = 5
                    if self.image_index >= len(self.images):
                        self.attacking = False
                    if self.attacking_method == "1":
                        self.images = player_sword_attack_1_rt_imgs
                    elif self.attacking_method == "2":
                        self.images = player_sword_attack_2_rt_imgs
                    elif self.attacking_method == "3":
                        self.images = player_sword_attack_3_rt_imgs
                elif self.vy > 1 and not self.on_platform:
                    self.images = player_fall_rt_imgs
                elif self.vy < 0 and not self.on_platform:
                    self.images = player_jump_rt_imgs
                elif self.crouching:
                    self.images = player_sword_crouch_rt_imgs
                elif self.sliding:
                    self.images = player_slide_rt_imgs
                elif self.vx > 0 and self.walking:
                    self.images = player_sword_walk_rt_imgs
                else:
                    self.images = player_sword_idle_rt_imgs
            elif self.vy > 1 and not self.on_platform:
                self.images = player_fall_rt_imgs
            elif self.vy < 0 and not self.on_platform:
                self.images = player_jump_rt_imgs
            elif self.crouching:
                self.images = player_crouch_rt_imgs
            elif self.sliding:
                self.images = player_slide_rt_imgs
            elif self.attacking:
                if self.image_index >= len(self.images) - 1:
                    self.attacking = False
                if self.attacking_method == "1":
                    self.images = player_hit_1_rt_imgs
                elif self.attacking_method == "2":
                    self.images = player_hit_2_rt_imgs
                elif self.attacking_method == "3":
                    self.images = player_hit_3_rt_imgs
            elif self.vx > 0 and self.walking:
                self.images = player_walk_rt_imgs
            elif self.on_platform:
                self.images = player_idle_rt_img
        # ///
        elif not self.facing_right:
            if self.wall_jumping_left:
                self.images = player_wall_jump_lt_imgs
            elif self.wall_sliding:
                self.images = player_wall_slide_lt_imgs
            elif self.has_sword_equipped:
                if self.switching_to_sword:
                    self.images = player_sword_draw_lt_imgs
                    if self.image_index >= len(self.images) - 1:
                        self.switching_to_sword = False
                elif self.removing_sword:
                    self.images = player_sword_sheathe_lt_imgs
                    if self.image_index >= len(self.images) - 1:
                        self.removing_sword = False
                        self.has_sword_equipped = False
                elif self.attacking:
                    self.animation_speed = 5
                    if self.image_index >= len(self.images) - 1:
                        self.attacking = False
                    if self.attacking_method == "1":
                        self.images = player_sword_attack_1_lt_imgs
                    elif self.attacking_method == "2":
                        self.images = player_sword_attack_2_lt_imgs
                    elif self.attacking_method == "3":
                        self.images = player_sword_attack_3_lt_imgs
                elif self.vy > 1 and not self.on_platform:
                    self.images = player_fall_lt_imgs
                elif self.vy < 0 and not self.on_platform:
                    self.images = player_jump_lt_imgs
                elif self.crouching:
                    self.images = player_sword_crouch_lt_imgs
                elif self.sliding:
                    self.images = player_slide_lt_imgs
                elif self.vx < 0 and self.walking:
                    self.images = player_sword_walk_lt_imgs
                else:
                    self.images = player_sword_idle_lt_imgs
            elif self.vy > 1 and not self.on_platform:
                self.images = player_fall_lt_imgs
            elif self.vy < 0 and not self.on_platform:
                self.images = player_jump_lt_imgs
            elif self.crouching:
                self.images = player_crouch_lt_imgs
            elif self.sliding:
                self.images = player_slide_lt_imgs
            elif self.attacking:
                if self.image_index >= len(self.images) - 1:
                    self.attacking = False
                if self.attacking_method == "1":
                    self.images = player_hit_1_lt_imgs
                elif self.attacking_method == "2":
                    self.images = player_hit_2_lt_imgs
                elif self.attacking_method == "3":
                    self.images = player_hit_3_lt_imgs
            elif self.vx < 0 and self.walking:
                self.images = player_walk_lt_imgs
            elif self.on_platform:
                self.images = player_idle_lt_img
            
        # set midbottom of rect when wall sliding or wall jumping
        midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom

    def update(self):
        if self.can_gravity:
            self.apply_gravity()
        self.check_collisions()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()
        self.figure_angle()
        self.run_update_functions()
