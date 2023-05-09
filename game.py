
# Imports
import json, pygame, random
from settings import *
from utilities import *
from entities import *
from player import *

# Main game class 
class Game:

    def __init__(self):
        self.running = True
        self.grid_on = False
        self.new_game()
        self.start_loc = [1, 5]
        self.restart_loc = [88, 8]
        self.checkpoint_loc = [0, 0]
        self.health_img = None
        self.background_img = background_img
        self.has_mouse = False
        self.hero_attack = "blank"
        self.start_title_destination = "none"
        self.hero_attacking = False
        self.gameplay_paused = False

        self.screen_shake = 0
        self.shaking = False
        self.menu_gonna_advance = False
        self.hints_gonna_advance = False
        self.hint_1_shown = False
        self.hint_2_shown = False
        self.hint_3_shown = False
        self.hint_4_shown = False
        self.can_control = True
        self.particle_color = black
        self.can_show_shop = False
        self.shop_color_1 = custom_color_2
        self.shop_color_2 = custom_color_2
        self.shop_color_3 = custom_color_2
        self.shop_gonna_advance = False
        self.player_hitting_portal = False

        self.checkpoint_level = 0
        self.title_ticks = 0
        self.restart_ticks = 0
        self.restart_animation_speed = 5
        self.restart_image_index = 0
        self.attack_time_left = 100
        self.attack_counters = 0
        self.attack_cooldown = 5
        self.menu_num = -1
        self.hints_num = -1
        self.hints_num = 0
        self.cloud_offset = 0
        self.shop_num = 0
        self.shop_choice_1_left = 0
        self.shop_choice_1_right = 0
        self.shop_choice_2_left = 0
        self.shop_choice_2_right = 0
        self.shop_choice_3_left = 0
        self.shop_choice_3_right = 0
        self.quick_boots_cost = 6
        self.sharper_sword_cost = 7
        self.invis_potion_cost = 25
        self.enemy_drop_y = 0
        self.enemy_drop_x = 0
        self.advance_ticks = 50
        self.bg_op = 255
        self.sword_op = 0

        self.should_show_hints = False
        self.should_advance = False
        self.should_draw_particles = False
        self.should_show_shop = False
        self.should_show_sword_lines = False
        self.should_remove_sword_lines = False
        self.should_show_cave_bg = False

        self.is_dark = False
        self.blood_particles = []
        self.spark_particles = []
        self.fog_lights = []
        self.dust = []
        self.times = [1]
        self.render_offset = [0, 0]

    # Start the game
    def new_game(self):
        self.player = pygame.sprite.GroupSingle()
        self.hero = Player(self, player_idle_rt_img, "player")
        self.player.add(self.hero)
        self.background_img = background_img
        self.stage = START
        self.level = 2
        self.typewriter_event = pygame.USEREVENT+1
        self.text_surf = None
        self.start_level()
        play_music(title_music)
        play_music(ambient_wind_snd)

    
    # Add all the sprites to their respective groups to add to the screen
    def start_level(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.player_slashes = pygame.sprite.Group()
        self.non_play_chars = pygame.sprite.Group()
        self.enemy_drops = pygame.sprite.Group()
        self.counters = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.floating_platforms = pygame.sprite.Group()
        self.enemy_attacks = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()

        self.should_show_cave_bg = False
        self.player_hitting_portal = False
        self.hero.image_scale_1 = 58
        self.hero.image_scale_2 = 58
        self.hero.image_scale_3 = 360
        self.advance_ticks = 50

        with open(levels[self.level - 1]) as f:
            data = json.load(f)
        self.world_width = data['width'] * GRID_SIZE
        self.world_height = data['height'] * GRID_SIZE
        self.gravity = data['gravity']
        if self.level == 2:
            rand = random.randint(0, 2)
            if rand == 0:
                self.start_loc = data['start'][0], data['start'][1]
                loc = data['start'][0], data['start'][1]
                self.restart_loc = data['start'][0], data['start'][1]
            elif rand == 1:
                self.start_loc = data['start'][2], data['start'][3]
                loc = data['start'][2], data['start'][3]
                self.restart_loc = data['start'][2], data['start'][3]
            else:
                self.should_show_cave_bg = True
                self.start_loc = data['start'][4], data['start'][5]
                loc = data['start'][4], data['start'][5]
                self.restart_loc = data['start'][4], data['start'][5]
        else:
            loc = data['start']
        self.start_loc = data['start']
        self.restart_loc = data['restart']
        self.hero.move_to(loc)
        self.checkpoint_loc = [0, 0]
        
        if "grass_top_middle" in data:
            for loc in data['grass_top_middle']:
                self.platforms.add( Platform(self, grass_top_middle_img, loc) )

        if "grass_inside_bottom" in data:
            for loc in data['grass_inside_bottom']:
                self.platforms.add( Platform(self, grass_inside_bottom_img, loc) )

        if "grass_top_left" in data:
            for loc in data['grass_top_left']:
                self.platforms.add( Platform(self, grass_top_left_img, loc) )

        if "grass_top_right" in data:
            for loc in data['grass_top_right']:
                self.platforms.add( Platform(self, grass_top_right_img, loc) )

        if "grass_inside_left" in data:
            for loc in data['grass_inside_left']:
                self.platforms.add( Platform(self, grass_inside_left_img, loc) )

        if "grass_inside_right" in data:
            for loc in data['grass_inside_right']:
                self.platforms.add( Platform(self, grass_inside_right_img, loc) )

        if "grass_inside_bottom_left" in data:
            for loc in data['grass_inside_bottom_left']:
                self.platforms.add( Platform(self, grass_inside_bottom_left_img, loc) )

        if "grass_inside_bottom_right" in data:
            for loc in data['grass_inside_bottom_right']:
                self.platforms.add( Platform(self, grass_inside_bottom_right_img, loc) )

        if "dirt_middle" in data:
            for loc in data['dirt_middle']:
                self.platforms.add( Platform(self, dirt_middle_img, loc) )

        if "dirt_bottom_left" in data:
            for loc in data['dirt_bottom_left']:
                self.platforms.add( Platform(self, dirt_bottom_left_img, loc) )

        if "dirt_bottom_right" in data:
            for loc in data['dirt_bottom_right']:
                self.platforms.add( Platform(self, dirt_bottom_right_img, loc) )

        if "dirt_top_left" in data:
            for loc in data['dirt_top_left']:
                self.platforms.add( Platform(self, dirt_top_left_img, loc) )

        if "dirt_top_right" in data:
            for loc in data['dirt_top_right']:
                self.platforms.add( Platform(self, dirt_top_right_img, loc) )

        if "lava_top" in data:
            for loc in data['lava_top']:
                self.platforms.add( Platform(self, lava_top_img, loc) )

        if "lava_middle" in data:
            for loc in data['lava_middle']:
                self.platforms.add( Platform(self, lava_middle_img, loc) )
        
        elif "portal" in data:
            for portal in data['portal']:
                self.portals.add( Portal(self, portal_imgs, portal))
        
        if "vines" in data:
            for vine in data['vines']:
                x, y = vine
                rand = random.randint(1, 4)
                if rand == 1:
                    img = vine_1_imgs
                elif rand == 2:
                    img = vine_2_imgs
                elif rand == 3:
                    img = vine_3_imgs
                elif rand == 4:
                    img = vine_4_imgs
                if rand == 3:
                    x, y = np.array([x, y]) + np.array([0, 0.5])
                self.foreground.add( AnimatedWalkThru(self, img, [x, y]))
        
        if "tree" in data:
            for tree in data['tree']:
                x, y = tree
                rand = random.randint(1, 4)
                if rand == 1:
                    img = tree_1_img
                    loc = np.array([x, y]) - np.array([0, 1.5])
                elif rand == 2:
                    img = tree_2_img
                    loc = np.array([x, y]) - np.array([0, 1.5])
                elif rand == 3:
                    img = tree_3_img
                    loc = np.array([x, y]) - np.array([0, 0.4])
                elif rand == 4:
                    img = tree_4_img
                    loc = np.array([x, y]) - np.array([0, 1])
                if rand <= 2:
                    self.foreground.add(WalkThru(self, img, loc))
                else:
                    self.background.add( WalkThru(self, img, loc))
        
        if "grass" in data:
            for grass in data['grass']:
                rand = random.randint(1, 5)
                loc = grass
                if rand == 1:
                    img = grass_1_imgs
                elif rand == 2:
                    img = grass_2_imgs
                elif rand == 3:
                    img = grass_3_imgs
                elif rand == 4:
                    img = grass_4_imgs
                elif rand == 5:
                    img = grass_5_imgs
                rand = random.randint(1, 5)
                if rand <= 2:
                    self.foreground.add( AnimatedWalkThru(self, img, loc))
                else:
                    self.background.add( AnimatedWalkThru(self, img, loc))
        
        if "floating_platform" in data:
            for floating_plat in data['floating_platform']:
                x, y, type, min, max = floating_plat
                loc = x, y
                self.floating_platforms.add( FloatingPlatform(self, floating_platform_1_img, loc, type, min, max))
        
        # ENEMIES
        if "mouse_1" in data:
            for loc in data['mouse_1']:
                self.enemies.add( Mouse_1(self, guard_idle_rt_imgs, loc))

        if "bowman" in data:
            for loc in data['bowman']:
                self.enemies.add( Bowman(self, bowman_idle_rt_imgs, loc))
        
        if "elite" in data:
            for loc in data['elite']:
                self.enemies.add( Elite(self, elite_idle_rt_imgs, loc))

        # NPCS / ITEMS
        if 'merchant' in data:
            for loc in data['merchant']:
                self.non_play_chars.add( Merchant(self, merchant_imgs, loc))
        
        if 'orb' in data:
            for loc in data['orb']:
                self.interactables.add( Orb(self, blank_img, loc))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.background, self.platforms, self.floating_platforms, self.portals, self.non_play_chars, self.interactables, self.player, self.player_slashes, self.enemy_attacks, self.enemies, self.enemy_drops, self.foreground)
    

    # Show title screen by making a number and when the number gets to a certain point, the 
    def show_title_screen(self):
        # Add 1 to menu_num when menu_num is less than zero and menu_gonna_advance is False.
        if self.menu_num < 11 and not self.menu_gonna_advance:
            self.menu_num += 1
        # Game checks when spacebar is pressed and when it is, menu_gonna_advance = True.
        elif self.menu_gonna_advance:
            # Go to whatever next screen is needed based on what letter the game detects types.
            if self.menu_num == 0:
                if self.start_title_destination == "start_menu":
                    self.stage = MENU
                    self.menu_gonna_advance = False
                elif self.start_title_destination == "instructions":
                    self.stage = INSTRUCTIONS
                    self.menu_gonna_advance = False
            else:
                self.menu_num -= 1
        
        # Load the frames with menu_num in place of the frame number so it looks like an animation
        main_surface.blit(load_image('assets/images/other/title_screen/frame-' + str(self.menu_num) + '.png').convert_alpha(), (0, 0))

    # Show win screen
    def show_win_screen(self):
        pass
        
    # Show lose screen
    def show_lose_screen(self):
        pass
    
    # Show pause screen
    def show_pause_screen(self):
        pass
    
    # Show start_menu
    def show_start_menu(self):
        if self.menu_num < 11 and not self.menu_gonna_advance:
            self.menu_num += 1
        elif self.menu_gonna_advance:
            if self.menu_num == 0:
                self.stage = PLAYING
                self.menu_gonna_advance = False
            else:
                self.menu_num -= 1
            
        main_surface.blit(load_image('assets/images/other/start_screen/frame-' + str(self.menu_num) + '.png').convert_alpha(), (0, 0))
    
    # Show instructions 
    def show_instructions(self):
        if self.menu_num < 11 and not self.menu_gonna_advance:
            self.menu_num += 1
        elif self.menu_gonna_advance:
            if self.menu_num == 0:
                self.stage = START
                self.menu_gonna_advance = False
            else:
                self.menu_num -= 1
        main_surface.blit(load_image('assets/images/other/instructions/frame-' + str(self.menu_num) + '.png').convert_alpha(), (0, 0))

    # Show error screen 
    def show_error_screen(self):
        text = error_font.render("Aw snap, something went wrong!", True, custom_color_2)
        rect = text.get_rect()
        rect.centerx = 500
        rect.centery = 500
        main_surface.blit(text, rect)

    # Show hints when player gets to a specific place.
    def show_hints(self):
        if self.should_show_hints:
            if self.hint_to_show == 1 and not self.hint_1_shown:
                if self.hints_num < 11 and not self.hints_gonna_advance:
                    self.hints_num += 1
                elif self.hints_gonna_advance:
                    if self.hints_num == 0:
                        self.should_show_hints = False
                        self.hint_1_shown = True
                        self.hints_gonna_advance = False
                    else:
                        self.hints_num -= 1
                main_surface.blit(load_image('assets/images/other/hint_1/frame-' + str(self.hints_num) + '.png').convert_alpha(), (0, 0))
            elif self.hint_to_show == 2 and not self.hint_2_shown:
                if self.hints_num < 13 and not self.hints_gonna_advance:
                    self.hints_num += 1
                elif self.hints_gonna_advance:
                    if self.hints_num == 0:
                        self.should_show_hints = False
                        self.hint_2_shown = True
                        self.hints_gonna_advance = False
                    else:
                        self.hints_num -= 1
                main_surface.blit(load_image('assets/images/other/hint_2/frame-' + str(self.hints_num) + '.png').convert_alpha(), (0, 0))
            elif self.hint_to_show == 3 and not self.hint_3_shown:
                if self.hints_num < 13 and not self.hints_gonna_advance:
                    self.hints_num += 1
                elif self.hints_gonna_advance:
                    if self.hints_num == 0:
                        self.should_show_hints = False
                        self.hint_3_shown = True
                        self.hints_gonna_advance = False
                    else:
                        self.hints_num -= 1
                main_surface.blit(load_image('assets/images/other/hint_3/frame-' + str(self.hints_num) + '.png').convert_alpha(), (0, 0))
            elif self.hint_to_show == 4 and not self.hint_4_shown:
                if self.hints_num < 13 and not self.hints_gonna_advance:
                    self.hints_num += 1
                elif self.hints_gonna_advance:
                    if self.hints_num == 0:
                        self.should_show_hints = False
                        self.hint_4_shown = True
                        self.hints_gonna_advnace = False
                    else:
                        self.hints_num -= 1
                main_surface.blit(load_image('assets/images/other/hint_4/frame-' + str(self.hints_num) + '.png').convert_alpha(), (0, 0))
    
    # Show shop and remove shop
    def show_shop(self):
        if self.should_show_shop:
            
            self.set_shop_background()
            main_surface.blit(load_image('assets/images/other/shop/frame-' + str(self.shop_num) + '.png').convert_alpha(), (0, 0))
            if self.shop_num > 5:
                self.show_shop_options()
    
    def set_shop_background(self):
        if self.shop_num < 11 and not self.shop_gonna_advance:
            self.shop_num += 1
        elif self.shop_gonna_advance:
            if self.shop_num == 0:
                self.should_show_shop = False
                self.shop_gonna_advance = False
            else:
                self.shop_num -= 1
    
    def show_shop_options(self):
        main_surface.blit(coin_img, (321, 170))
        text = shop_font_1.render(":  " + str(self.hero.money), True, custom_color_2)
        rect = text.get_rect()
        rect.left = 364
        rect.top = 180
        main_surface.blit(text, rect)
        main_surface.blit(coin_img, (850, 170))
        text = shop_font_2.render("Sharper sword: " + str(self.sharper_sword_cost), True, self.shop_color_1)
        rect = text.get_rect()
        rect.left = 655
        rect.top = 177
        self.shop_choice_1_left = rect.left
        self.shop_choice_1_right = rect.right
        main_surface.blit(text, rect)
        text = shop_font_3.render("(Do more damage) (+1)", True, self.shop_color_1)
        rect = text.get_rect()
        rect.left = 698
        rect.top = 220
        main_surface.blit(text, rect)
        main_surface.blit(coin_img, (840, 270))
        text = shop_font_2.render("Quicker boots: " + str(self.quick_boots_cost), True, self.shop_color_2)
        rect = text.get_rect()
        rect.left = 655
        rect.top = 277
        self.shop_choice_2_left = rect.left
        self.shop_choice_2_right = rect.right
        main_surface.blit(text, rect)
        text = shop_font_3.render("(Walk faster) (+1)", True, self.shop_color_2)
        rect = text.get_rect()
        rect.left = 698
        rect.top = 320
        main_surface.blit(text, rect)
        main_surface.blit(coin_img, (880, 370))
        text = shop_font_2.render("Invisibility potion: " + str(self.invis_potion_cost), True, self.shop_color_3)
        rect = text.get_rect()
        rect.left = 655
        rect.top = 377
        self.shop_choice_3_left = rect.left
        self.shop_choice_3_right = rect.right
        main_surface.blit(text, rect)
        text = shop_font_3.render("Go invisible for a few seconds when used [1]", True, self.shop_color_3)
        rect = text.get_rect()
        rect.left = 678
        rect.top = 420
        main_surface.blit(text, rect)
        text = shop_font_3.render("SPACE to dismiss.", True, custom_color_2)
        rect = text.get_rect()
        rect.left = 810
        rect.top = 505
        main_surface.blit(text, rect)
    
    def draw_hud(self):
        rect = pause_icon.get_rect()
        rect.top = main_surface.get_rect().top + 7
        rect.right = main_surface.get_rect().left + 55
        main_surface.blit(pause_icon, (rect))

    # Draw stuff on screen such as the pause icon and blood particles and shop
    def draw_stuff(self):
        self.draw_particles(self.gameplay_paused)
        self.show_shop()
        self.handle_opacity_changes()
        
        self.draw_hud()
    
    def show_mouse(self):
        mx, my = pygame.mouse.get_pos()
        if not self.has_mouse:
            pygame.mouse.set_visible(False)
            if self.should_show_shop:
                img = cursor_img
                main_surface.blit(img, (mx, my))
        else:
            pygame.mouse.set_visible(False)
            img = cursor_img
            main_surface.blit(img, (mx, my))
            
    def handle_opacity_changes(self):
        offset_x, offset_y = self.get_offsets()
        if self.should_show_cave_bg:
            if not self.bg_op < 0:
                self.bg_op -= 8
        else:
            if self.bg_op < 254:
                self.bg_op += 8

        if not self.should_show_cave_bg:
            if self.should_show_sword_lines:
                if self.sword_op < 255:
                    self.sword_op += 10.2
            elif self.should_remove_sword_lines:
                if self.sword_op > 0:
                    self.sword_op -= 10.2
            attack_overlay_img.set_alpha(self.sword_op)
            main_surface.blit(attack_overlay_img, (0, 0))
        
    # Use attack counters to set hero_attacking variable
    def attack_check(self):
        if self.attack_counters >= 3:
            self.attack_counters = 0
        if self.hero_attacking:
            if self.attack_cooldown > 0:
                self.hero.can_attack = False
                self.attack_cooldown -= 1
            else:
                self.hero.can_attack = True
            if self.attack_time_left > 0:
                self.attack_time_left -= 1
            else:
                self.attack_counters = 0
                self.attack_time_left = 50
                self.hero_attacking = False
    
    # Check location of hero to display hints on screen.
    def hint_hero_loc_check(self):
        #print(self.hero.loc_x)
        #print(self.hero.loc_y)
        if 0.7 <= self.hero.loc_x <= 1.7 and 2.6 <= self.hero.loc_y <= 4.8 and self.level == 1:
            self.should_show_hints = True
            self.hint_to_show = 1
        elif 12.5 <= self.hero.loc_x <= 14.5 and 9.5 <= self.hero.loc_y <= 12.5 and self.level == 1:
            self.should_show_hints = True
            self.hint_to_show = 2
        elif 22.3 <= self.hero.loc_x <= 24.3 and 6.0 <= self.hero.loc_y <= 8.0 and self.level == 1:
            self.should_show_hints = True
            self.hint_to_show = 3
        elif 35.7 <= self.hero.loc_x <= 36.7 and 6.15 <= self.hero.loc_y <= 7.8 and self.level == 1:
            self.should_show_hints = True
            self.hint_to_show = 4
        if self.level == 2:
            if 48 < self.hero.loc_x < 50 and 7 < self.hero.loc_y < 9:
                self.should_show_cave_bg = True
            elif 48 < self.hero.loc_x < 50 and 10 < self.hero.loc_y < 12:
                self.should_show_cave_bg = False

    # Functions to be run every frame  
    def run_update_functions(self):
        self.hint_hero_loc_check()
        self.attack_check()
        if self.should_advance:
            self.advance()
        
    # Shake the screen 
    def shake_screen(self):
        if self.screen_shake:

            self.render_offset[0] = random.randint(-2, 2)
            self.render_offset[1] = random.randint(-2, 2)

    # Create checkpoint 
    def create_checkpoint(self):
        self.checkpoint_level = self.level
        self.checkpoint_loc = [self.hero.rect.x / GRID_SIZE, self.hero.rect.y / GRID_SIZE]                

    # Function to help reduce any lag
    def in_area(self, sprite1, sprite2):
        dx = abs(sprite1.rect.centerx - sprite2.rect.centerx)
        dy = abs(sprite1.rect.centery - sprite2.rect.centery)
        return dx < 1 * WIDTH and dy < 1 * HEIGHT
    
    # Fill fog surface with dark gray
    def fill_fog(self):
        fog.fill(dark_dark_gray)
    
    # Draw light image when dark
    def render_fog(self, x=None, y=None, other=None, radius=LIGHT_RADIUS):
        offset_x, offset_y = self.get_offsets()
        mx, my = pygame.mouse.get_pos()
        # Scale light image to proper dimensions (radius), and set light_rect to light image rect
        mask = pygame.transform.scale(light_mask, radius)
        light_rect = mask.get_rect()

        # Sets the light_rect center to whatever position it should be at
        if other == "mouse_pos":
            light_rect.center = mx, my
        elif other == "player_pos":
            light_rect.center = self.hero.rect.centerx - offset_x, self.hero.rect.centery - offset_y
        else:
            if x == None and y == None:
                light_rect.center = other.rect.centerx - offset_x, other.rect.centery - offset_y
            else:
                light_rect.center = x, y
        
        # Draw the actual light image at the center of the light_rect 
        fog.blit(mask, light_rect)

    def reset_fog(self):
        if len(self.times) < 1:
            self.times.append(1)
            self.fog_lights.clear()
    
    def show_darkness(self):
        self.fill_fog()
        for time in self.times:
            self.times.clear()
            self.fog_lights.append([None, None, "player_pos", LIGHT_RADIUS_PLAYER])
            for enemy in self.enemies:
                enemy.create_spotlights()
        for light in self.fog_lights:
            self.render_fog(light[0], light[1], light[2], light[3])
        main_surface.blit(fog, (0, 0), special_flags=pygame.BLEND_MULT)


    # Key event handling
    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                if self.should_show_shop:
                    mx, my = pygame.mouse.get_pos()
                    hovered_1 = self.shop_choice_1_left <= mx <= self.shop_choice_1_right and 165 <= my <= 215
                    hovered_2 = self.shop_choice_2_left <= mx <= self.shop_choice_2_right and 265 <= my <= 310
                    hovered_3 = self.shop_choice_3_left <= mx <= self.shop_choice_3_right and 375 <= my <= 410
                    if hovered_1:
                        self.shop_color_1 = custom_color_1
                        self.shop_color_2 = custom_color_2
                        self.shop_color_3 = custom_color_2
                    elif hovered_2:
                        self.shop_color_1 = custom_color_2
                        self.shop_color_3 = custom_color_2
                        self.shop_color_2 = custom_color_1
                    elif hovered_3:
                        self.shop_color_1 = custom_color_2
                        self.shop_color_2 = custom_color_2
                        self.shop_color_3 = custom_color_1
                    else:
                        self.shop_color_1 = custom_color_2
                        self.shop_color_2 = custom_color_2
                        self.shop_color_3 = custom_color_2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if self.stage == MENU:
                        if 646 <= mx <= 729 and 203 <= my <= 241:
                            self.has_mouse = True
                            self.menu_gonna_advance = True
                            play_music(theme_music)
                            pygame.mixer.music.fadeout(1000)
                        elif 945 <= mx <= 1007 and 203 <= my <= 241:
                            self.has_mouse = False
                            self.menu_gonna_advance = True
                            play_music(theme_music)
                            pygame.mixer.music.fadeout(1000)
                    elif self.stage == PLAYING:
                        if self.has_mouse and self.can_control:
                            self.hero_attacking = True
                            if self.attack_time_left > 0:
                                if self.attack_counters >= 3:
                                    self.attack_counters = 0
                                    self.attack_time_left = 100
                                else:
                                    self.attack_counters += 1
                                    self.attack_time_left = 50
                            if self.hero.has_sword_equipped:
                                self.hero_attack = "sword_slash_" + str(self.attack_counters)
                            else:
                                self.hero_attack = "punch_" + str(self.attack_counters)
                            self.hero.attack()
                        if self.should_show_shop:
                            clicked_1 = self.shop_choice_1_left <= mx <= self.shop_choice_1_right and 165 <= my <= 215
                            clicked_2 = self.shop_choice_2_left <= mx <= self.shop_choice_2_right and 265 <= my <= 310
                            clicked_3 = self.shop_choice_3_left <= mx <= self.shop_choice_3_right and 375 <= my <= 410
                            can_afford_1 = self.hero.money >= self.sharper_sword_cost
                            can_afford_2 = self.hero.money >= self.quick_boots_cost
                            can_afford_3 = self.hero.money >= self.invis_potion_cost
                            if clicked_1 and can_afford_1:
                                self.hero.money -= self.sharper_sword_cost
                                self.sharper_sword_cost += 2
                                self.hero.sword_dmg += 1
                                purchase_snd.play()
                            elif clicked_2 and can_afford_2:
                                self.hero.money -= self.quick_boots_cost
                                self.quick_boots_cost += 2
                                self.hero.walk_speed += 0.5
                                self.hero.slide_speed += 0.5
                                purchase_snd.play()
                            elif clicked_3 and can_afford_3:
                                self.hero.money -= self.invis_potion_cost
                                self.hero.has_invis_potion += 1
                                purchase_snd.play()
                            else:
                                error_snd.play()
                elif event.button == 3:
                    self.hero.switch_weapons("sword")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.grid_on = not self.grid_on

                if self.stage == MENU:
                    if event.key == pygame.K_y:
                        self.has_mouse = True
                        self.menu_gonna_advance = True
                        pygame.mixer.music.fadeout(1000)
                        play_music(theme_music)
                    elif event.key == pygame.K_n:
                        self.has_mouse = False
                        self.menu_gonna_advance = True
                        pygame.mixer.music.fadeout(1000)
                        play_music(theme_music)
                elif self.stage == START:
                    if event.key == pygame.K_RETURN:
                        self.menu_gonna_advance = True
                        self.start_title_destination = "start_menu"
                    elif event.key == pygame.K_i:
                        self.menu_gonna_advance = True
                        self.start_title_destination = "instructions"

                # Playing key events.
                elif self.stage == PLAYING:
                    if event.key == pygame.K_p:
                        self.stage = PAUSED
                        self.random1 = random.randint(1, 3)
                        pause_music() 
                    elif event.key == pygame.K_m:
                        if pygame.mixer.music.get_busy():
                            pause_music()
                        else:
                            unpause_music()
                    elif event.key == pygame.K_1:
                        self.screen_shake = 150
                    elif event.key == pygame.K_SPACE:
                        if self.player_hitting_portal:
                            self.should_advance = True
                        if self.should_show_hints:
                            self.hints_gonna_advance = True
                        if self.should_show_shop:
                            self.gameplay_paused = False
                            self.shop_gonna_advance = True
                        elif self.can_show_shop:
                            merchant_snd.play()
                            self.gameplay_paused = True
                            self.should_show_shop = True
                    elif event.key == pygame.K_UP and not self.should_show_shop and not self.has_mouse or event.key == pygame.K_w and not self.should_show_shop and self.has_mouse:
                        self.hero.jump()
                    elif event.key == pygame.K_e and not self.hero.crouching and not self.should_show_shop:
                        self.hero.set_slide()
                    elif event.key == pygame.K_q and not self.should_show_shop and self.can_control and not self.has_mouse:
                        self.hero_attacking = True
                        if self.attack_time_left > 0:
                            if self.attack_counters >= 3:
                                self.attack_counters = 0
                                self.attack_time_left = 100
                            else:
                                self.attack_counters += 1
                                self.attack_time_left = 50
                        if self.hero.has_sword_equipped:
                            self.hero_attack = "sword_slash_" + str(self.attack_counters)
                        else:
                            self.hero_attack = "punch_" + str(self.attack_counters)
                        self.hero.attack()
                    elif event.key == pygame.K_TAB and not self.should_show_shop:
                        self.hero.switch_weapons("sword")
                    elif event.key == pygame.K_r:
                        self.start_level()
                    elif event.key == pygame.K_n:
                        self.level += 1
                        self.start_level()

                # Won or lost key events.
                elif self.stage == WIN or self.stage == LOSE:
                    if event.key == pygame.K_RETURN:
                        self.restart()
                        unpause_music()

                # Paused key events.
                elif self.stage == PAUSED:
                    if event.key == pygame.K_i:
                        self.stage = INSTRUCTIONS
                    elif event.key == pygame.K_RETURN:
                        self.stage = PLAYING
                        unpause_music()

                # Instructions key events.
                elif self.stage == INSTRUCTIONS:
                    if event.key == pygame.K_RETURN:
                        if self.start_title_destination == 'instructions':
                            self.menu_gonna_advance = True
                        else:
                            self.stage = PAUSED
        
        pressed = pygame.key.get_pressed()
        can_move_left = pressed[pygame.K_LEFT] and not self.hero.switching_to_sword and not self.hero.removing_sword and not self.hero.attacking and not self.should_show_shop and not self.has_mouse or pressed[pygame.K_a] and not self.hero.switching_to_sword and not self.hero.removing_sword and not self.hero.attacking and not self.should_show_shop and self.has_mouse
        can_move_right = pressed[pygame.K_RIGHT] and not self.hero.switching_to_sword and not self.hero.removing_sword and not self.hero.attacking and not self.should_show_shop and not self.has_mouse or pressed[pygame.K_d] and not self.hero.switching_to_sword and not self.hero.removing_sword and not self.hero.attacking and not self.should_show_shop and self.has_mouse
        if pressed[pygame.K_s] and self.has_mouse or pressed[pygame.K_DOWN] and not self.has_mouse:
            self.hero.crouch()
        elif not self.hero.sliding:
            if self.hero.wall_sliding and not self.can_control:
                if self.hero.can_wall_jump_right and pressed[pygame.K_UP] and not self.has_mouse or self.hero.can_wall_jump_right and pressed[pygame.K_w] and self.has_mouse:
                    self.hero.wall_jump_right()
                elif self.hero.can_wall_jump_left and pressed[pygame.K_UP] and not self.has_mouse or self.hero.can_wall_jump_left and pressed[pygame.K_w] and self.has_mouse:
                    self.hero.wall_jump_left()
            elif can_move_left:
                self.hero.walk_left()
            elif can_move_right:
                self.hero.walk_right()
            elif pressed[pygame.K_1]:
                self.shaking = True
            else:
                self.hero.stop()
        else:
            self.hero.stop()
    
    def draw_other_particles(self, loc_x, loc_y):
        self.particles.append([[loc_x - random.randint(-50, 50), loc_y - random.randint(-2, 2)], [random.randint(-5, 5), random.randint(-3, -2)], random.randint(4, 6)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.005
            pygame.draw.circle(main_surface, self.particle_color, [int(particle[0][0]), int(particle[0][1])], particle[2])
            if particle[2] <= 0:
                self.particles.remove(particle)
    
    # I have a list for each type of particle, and I add to them, the start location of the particle: [x, y], the [velocityX, velocityY] for how fast I want them to move, 
    # and the [size], however big I want them to be. All of those get subtracted each frame to make it get smaller, and move. I then draw circles based on those values, 
    # and blit that onto the screen. They get cleared after they get too small to reduce lag. And boom, particles :-)

    # Draw particles such as little blood splatters, and when a slash hits a wall.
    def draw_particles(self, paused):
        offset_x, offset_y = self.get_offsets()

        # particle list: ([[x, y], [velocityX, velocityY], size])
        for particle in self.blood_particles:
            if not paused:
                # particle_x + x_axis velocity
                particle[0][0] += particle[1][0]

                # particle_y + y_axis_velocity
                particle[0][1] += particle[1][1] + offset_y / 160

                # particle_size - 0.035 px
                particle[2] -= .1

            pygame.draw.circle(main_surface, custom_color_2, [int(particle[0][0]), int(particle[0][1])], particle[2])
            if particle[2] <= 0:
                self.blood_particles.remove(particle)
        
        for particle in self.spark_particles:
            if not paused:
                # particle_x + x_axis velocity
                particle[0][0] += particle[1][0]

                # particle_y + y_axis_velocity
                particle[0][1] += particle[1][1] + offset_y / 160

                # particle_size - 0.035 px
                particle[2] -= .035

            pygame.draw.circle(main_surface, custom_color_1, [int(particle[0][0]), int(particle[0][1])], particle[2])
            if particle[2] <= 0:
                self.spark_particles.remove(particle)
    
    # Draw particles in the background for scenery effects
    def draw_dust_particles(self, paused):
        offset_x, offset_y = self.get_offsets()

        # Particle variables
        particle_location = [random.randint(-WIDTH, WIDTH + 500), random.randint(0 - HEIGHT * 2, 0)]
        x_axis_veloctity = random.randint(-2, 2)
        y_axis_veloctity = random.randint(1, 5)
        particle_speed = [x_axis_veloctity, y_axis_veloctity]

        particle_size = random.randint(1, 4)

        # Don't add any particles while paused.
        if not paused:
            self.dust.append([particle_location, particle_speed, particle_size])
        for particle in self.dust:

            # particle_x + x_axis velocity
            particle[0][0] += particle [1][0]
            # particle_y + y_axis_velocity
            particle[0][1] += particle [1][1] + offset_y / 160
            # particle_size - 0.01
            particle[2] -= .01
            #                                           [particle_location_x, particle_location_y,  particle_size]
            pygame.draw.circle(main_surface, dark_gray, [int(particle[0][0]),int(particle[0][1])], int(particle[2]))

            # If size of particle gets too small or goes off screen, particle gets removed.
            if len(self.dust)>1:
                if particle[0][0] > WIDTH+500 or particle[2] <= 0:
                    self.dust.remove(particle)
    
    # Show enemy icons in the corner of the screen, along with their health
    def show_enemies_in_area(self):
        i = 0
        for enemy in self.enemies:
            if self.in_area(enemy, self.hero):
                y = 50 * i + 50
                main_surface.blit(enemy.icon, (1130, y))
                health_length = 25 * enemy.health
                pygame.draw.rect(main_surface, custom_color_2, [1125, y + 30, health_length, 10])
                i += 1


    # Advance levels
    def advance(self):
        self.advance_ticks -= 1
        if self.advance_ticks == 0:
            self.level += 1
            self.start_level()
            self.should_advance = False


    # Restart at beginning of level after you die
    def restart(self):
        if self.checkpoint_level == 0:
            self.hero.move_to(self.start_loc)
        else:
            self.hero.move_to(self.checkpoint_loc)
        self.stage = PLAYING
        self.hero.health = 4
        self.hero.vy = 0
        self.hero.vx = 0
        self.hero.restarting = True

            
    # Game updates everything every frame such as sprite updates and hero updates.
    def update(self):
        if self.stage == PLAYING:
            self.run_update_functions()
            if self.screen_shake > 0:
                self.screen_shake -= 1
                self.shake_screen()
            for sprite in self.all_sprites:
                if (self.in_area(sprite, self.hero)):
                    sprite.update()
            if not self.hero.is_alive():
                self.stage = LOSE
                self.random1 = random.randint(1, 3)
                pause_music()
    

    # Get offsets for scrolling
    def get_offsets(self):
        if self.hero.rect.centerx < WIDTH // 2:
            offset_x = 0
        elif self.hero.rect.centerx > self.world_width - WIDTH // 2:
            offset_x = self.world_width - WIDTH
        else:
            offset_x = self.hero.rect.centerx - WIDTH // 2
            
        if self.hero.rect.centery < HEIGHT // 2:
            offset_y = 0
        elif self.hero.rect.centery > self.world_height - HEIGHT // 2:
            offset_y = self.world_height - HEIGHT
        else:
            offset_y = self.hero.rect.centery - HEIGHT // 2
        
        if self.has_mouse and self.stage == PLAYING:
            mx, my = pygame.mouse.get_pos()
            x = -mx + WIDTH // 2
            y = -my + HEIGHT // 2
            offset_x -= x // GRID_X 
            offset_y -= y // GRID_Y
        return offset_x, offset_y
    
    # Draw cave background paralax layers
    def draw_cave_background(self, bg_dirt_offset_x, bg_dirt_offset_x_2, bg_dirt_offset_x_3, bg_dirt_offset_x_4, bg_dirt_offset_x_5, offset_x, offset_y):
        main_surface.blit(bg_dirt_layer_5_img, [bg_dirt_offset_x_5, 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_5_img, [bg_dirt_offset_x_5 + bg_dirt_layer_5_img.get_width(), 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_4_img, [bg_dirt_offset_x_4, 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_4_img, [bg_dirt_offset_x_4 + bg_dirt_layer_4_img.get_width(), 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_3_img, [bg_dirt_offset_x_3, 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_3_img, [bg_dirt_offset_x_3 + bg_dirt_layer_3_img.get_width(), 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_2_img, [bg_dirt_offset_x_2, 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_2_img, [bg_dirt_offset_x_2 + bg_dirt_layer_2_img.get_width(), 0.05 * -offset_y])
    
    # Draw background paralax layers
    def draw_main_background(self, bg_offset_x, bg_offset_x_2, bg_offset_x_3, bg_offset_x_4, bg_offset_x_5, bg_offset_x_6, offset_x, offset_y):
        main_surface.blit(bg_main_layer_4_img, [bg_offset_x_4, 0.1 * -offset_y])
        main_surface.blit(bg_main_layer_4_img, [bg_offset_x_4 + bg_main_layer_4_img.get_width(), 0.1 * -offset_y])
        main_surface.blit(bg_main_layer_6_img, [bg_offset_x_6, 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_6_img, [bg_offset_x_6 + bg_main_layer_6_img.get_width(), 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_5_img, [bg_offset_x_5 - self.cloud_offset, 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_5_img, [bg_offset_x_5 - self.cloud_offset + bg_main_layer_5_img.get_width(), 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_3_img, [bg_offset_x_3, 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_3_img, [bg_offset_x_3 + bg_main_layer_3_img.get_width(), 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_2_img, [bg_offset_x_2, 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_2_img, [bg_offset_x_2 + bg_main_layer_2_img.get_width(), 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_1_img, [bg_offset_x, 0.2 * -offset_y])
        main_surface.blit(bg_main_layer_1_img, [bg_offset_x + bg_main_layer_1_img.get_width(), 0.2 * -offset_y])

    # Set alphas for parralax layers for background change
    def set_background_alphas(self):
        bg_main_layer_1_img.set_alpha(self.bg_op)
        bg_main_layer_2_img.set_alpha(self.bg_op)
        bg_main_layer_3_img.set_alpha(self.bg_op)
        bg_main_layer_4_img.set_alpha(self.bg_op)
        bg_main_layer_5_img.set_alpha(self.bg_op)
        bg_main_layer_6_img.set_alpha(self.bg_op)

    # Draw cave overlayers.
    def draw_cave_overlayers(self, bg_dirt_offset_x, offset_y):
        self.is_dark = True
        main_surface.blit(bg_dirt_layer_1_img, [bg_dirt_offset_x, 0.05 * -offset_y])
        main_surface.blit(bg_dirt_layer_1_img, [bg_dirt_offset_x + bg_dirt_layer_1_img.get_width(), 0.05 * -offset_y])

    # Draw all sprites
    def draw_sprites(self, offset_x, offset_y):
        for sprite in self.all_sprites:
            if self.in_area(sprite, self.hero):
                main_surface.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y - offset_y])

    # Handle different stage rendering
    def handle_stages(self):
        if self.should_show_hints:
            self.show_hints()
        if self.stage == START:
            self.show_title_screen()
        elif self.stage == WIN:
            self.show_win_screen()
        elif self.stage == LOSE:
            self.show_lose_screen()
        elif self.stage == PAUSED:
            self.show_pause_screen()
        elif self.stage == INSTRUCTIONS:
            self.show_instructions()
        elif self.stage == MENU:
            self.show_start_menu()


    # Draw everything
    def render(self):

        mx, my = pygame.mouse.get_pos()
        offset_x, offset_y = self.get_offsets()
        self.cloud_offset += 0.2
        bg_dirt_offset_x = -1 * (0.8 * offset_x % bg_dirt_layer_1_img.get_width())
        bg_dirt_offset_x_2 = -1 * (0.6 * offset_x % bg_dirt_layer_2_img.get_width())
        bg_dirt_offset_x_3 = -1 * (0.5 * offset_x % bg_dirt_layer_3_img.get_width())
        bg_dirt_offset_x_4 = -1 * (0.4 * offset_x % bg_dirt_layer_4_img.get_width())
        bg_dirt_offset_x_5 = -1 * (0.3 * offset_x % bg_dirt_layer_5_img.get_width())
        bg_offset_x = -1 * (0.85 * offset_x % bg_main_layer_1_img.get_width())
        bg_offset_x_2 = -1 * (0.75 * offset_x % bg_main_layer_2_img.get_width())
        bg_offset_x_3 = -1 * (0.65 * offset_x % bg_main_layer_3_img.get_width())
        bg_offset_x_4 = -1 * (0.45 * offset_x % bg_main_layer_4_img.get_width())
        bg_offset_x_5 = -1 * (0.2 * offset_x % bg_main_layer_5_img.get_width())
        bg_offset_x_6 = -1 * (0.2 * offset_x % bg_main_layer_6_img.get_width())

        self.set_background_alphas()
        # Determine whether to to draw cave or normal backgrounds
        if self.bg_op < 50:
            self.draw_cave_background(bg_dirt_offset_x, bg_dirt_offset_x_2, bg_dirt_offset_x_3, bg_dirt_offset_x_4, bg_dirt_offset_x_5, offset_x, offset_y)
        if self.bg_op > 0:
            self.is_dark = False
            self.reset_fog()
            self.draw_main_background(bg_offset_x, bg_offset_x_2, bg_offset_x_3, bg_offset_x_4, bg_offset_x_5, bg_offset_x_6, offset_x, offset_y)
        
        # Draw background dust particles when not inside a cave.
        if not self.is_dark:
            self.draw_dust_particles(self.gameplay_paused)


        self.draw_sprites(offset_x, offset_y)
        if self.is_dark:
            self.show_darkness()
        if self.bg_op < 50:
            self.draw_cave_overlayers(bg_dirt_offset_x, offset_y)


        self.draw_stuff()
        self.show_enemies_in_area()
        self.handle_stages()
        
        # Draw grid
        if self.grid_on:
            if self.level == 1:
                draw_grid(main_surface, WIDTH, HEIGHT, GRID_SIZE, offset_x, offset_y, color=white)
            else:
                draw_grid(main_surface, WIDTH, HEIGHT, GRID_SIZE, offset_x, offset_y, color=black)
        
        self.show_mouse()
        screen.blit(main_surface, self.render_offset)


    # Update sprites
    def play(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            pygame.display.update()
            clock.tick(FPS)

# Actually start the game
if __name__ == "__main__":
   program = Game()
   program.play()
   pygame.quit()   
