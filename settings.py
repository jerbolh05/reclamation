# Imports
import pygame
from utilities import *

# Window settings
GRID_SIZE = 48
GRID_X = 25
GRID_Y = 13
WIDTH = GRID_X * GRID_SIZE # 1200
HEIGHT = GRID_Y * GRID_SIZE # 624
TITLE = "Jae's Adventure"
FPS = 60

# Make the game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
main_surface = pygame.surface.Surface([WIDTH, HEIGHT])
fog = pygame.surface.Surface([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Define colors

sky_blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (44, 197, 246)
dark_gray = (26, 26, 26)
dark_dark_gray = (9, 9, 9)
custom_color_1 = (36, 59, 97)
custom_color_2 = (140, 39, 37)

# Create fog effects
RADIUS_DIV = 2.5
LIGHT_RADIUS = [WIDTH/RADIUS_DIV, HEIGHT/RADIUS_DIV]
LIGHT_RADIUS_PLAYER = [WIDTH/1.5, HEIGHT/1.5]
LIGHT_RADIUS_MOUSE = [WIDTH/1.5, HEIGHT/1.5]



# Fonts

error_font = pygame.font.Font(None, 45)
shop_font_1 = pygame.font.Font('assets/fonts/Bellquinas.otf', 30)
shop_font_2 = pygame.font.Font('assets/fonts/Bellquinas.otf', 26)
shop_font_3 = pygame.font.Font('assets/fonts/Bellquinas.otf', 14)

# Load images

background_img = load_image('assets/images/backgrounds/background_main.png')
bg_main_layer_1_img = load_image('assets/images/backgrounds/bg_main_layer_1.png')
bg_main_layer_2_img = load_image('assets/images/backgrounds/bg_main_layer_2.png')
bg_main_layer_3_img = load_image('assets/images/backgrounds/bg_main_layer_3.png')
bg_main_layer_4_img = load_image('assets/images/backgrounds/bg_main_layer_4.png')
bg_main_layer_5_img = load_image('assets/images/backgrounds/bg_main_layer_5.png')
bg_main_layer_6_img = load_image('assets/images/backgrounds/bg_main_layer_6.png')

bg_dirt_layer_1_img = load_image('assets/images/backgrounds/bg_dirt_layer_1.png')
bg_dirt_layer_2_img = load_image('assets/images/backgrounds/bg_dirt_layer_2.png')
bg_dirt_layer_3_img = load_image('assets/images/backgrounds/bg_dirt_layer_3.png')
bg_dirt_layer_4_img = load_image('assets/images/backgrounds/bg_dirt_layer_4.png')
bg_dirt_layer_5_img = load_image('assets/images/backgrounds/bg_dirt_layer_5.png')

light_mask = load_image('assets/images/other/fog_overlay.png')



# ----- TILE IMAGES ----- #

grass_top_middle_img = load_image('assets/images/tiles/grass_top_middle.png')
grass_top_left_img = load_image('assets/images/tiles/grass_top_left.png')
grass_top_right_img = load_image('assets/images/tiles/grass_top_right.png')
grass_top_single_img = load_image('assets/images/tiles/grass_top_single.png')
dirt_middle_img = load_image('assets/images/tiles/dirt_middle.png')
dirt_bottom_right_img = load_image('assets/images/tiles/dirt_bottom_right.png')
dirt_bottom_left_img = load_image('assets/images/tiles/dirt_bottom_left.png')
dirt_top_right_img = load_image('assets/images/tiles/dirt_top_right.png')
dirt_top_left_img = load_image('assets/images/tiles/dirt_top_left.png')
grass_inside_left_img = load_image('assets/images/tiles/grass_inside_left.png')
grass_inside_right_img = load_image('assets/images/tiles/grass_inside_right.png')
grass_inside_bottom_img = load_image('assets/images/tiles/grass_inside_bottom.png')
grass_inside_bottom_left_img = load_image('assets/images/tiles/grass_inside_bottom_left.png')
grass_inside_bottom_right_img = load_image('assets/images/tiles/grass_inside_bottom_right.png')
grass_1_imgs = [load_image('assets/images/tiles/grasses_2_1.png'),
           load_image('assets/images/tiles/grasses_2_2.png'),
           load_image('assets/images/tiles/grasses_2_3.png')]
grass_2_imgs = [load_image('assets/images/tiles/grasses_4.png')]
grass_3_imgs = [load_image('assets/images/tiles/grasses_5.png')]
grass_4_imgs = [load_image('assets/images/tiles/grasses_big_flower.png')]
grass_5_imgs = [load_image('assets/images/tiles/grasses_flower.png')]
vine_1_imgs = [load_image('assets/images/tiles/vine_1_1.png'),
               load_image('assets/images/tiles/vine_1_2.png'),
               load_image('assets/images/tiles/vine_1_3.png'),
               load_image('assets/images/tiles/vine_1_2.png')]
vine_2_imgs = [load_image('assets/images/tiles/vine_2_1.png'),
               load_image('assets/images/tiles/vine_2_2.png'),
               load_image('assets/images/tiles/vine_2_3.png'),
               load_image('assets/images/tiles/vine_2_2.png')]
vine_3_imgs = [load_image('assets/images/tiles/vine_3.png')]
vine_4_imgs = [load_image('assets/images/tiles/vine_4_1.png'),
               load_image('assets/images/tiles/vine_4_2.png'),
               load_image('assets/images/tiles/vine_4_3.png'),
               load_image('assets/images/tiles/vine_4_2.png')]
tree_1_img = load_image('assets/images/tiles/tree_1.png')
tree_2_img = load_image('assets/images/tiles/tree_2.png')
tree_3_img = load_image('assets/images/tiles/tree_3.png')
tree_4_img = load_image('assets/images/tiles/tree_4.png')
portal_imgs = [load_image('assets/images/tiles/portal_1.png'),
               load_image('assets/images/tiles/portal_2.png'),
               load_image('assets/images/tiles/portal_3.png'),
               load_image('assets/images/tiles/portal_4.png'),
               load_image('assets/images/tiles/portal_5.png'),
               load_image('assets/images/tiles/portal_6.png'),
               load_image('assets/images/tiles/portal_7.png'),
               load_image('assets/images/tiles/portal_8.png')]
floating_platform_1_img = load_image('assets/images/tiles/floating_platform_1.png')

lava_top_img = load_image('assets/images/tiles/lava_top_1.png')
lava_middle_img = load_image('assets/images/tiles/lava_middle_1.png')

# ----- ITEM IMAGES ----- #

arrow_rt_img = load_image('assets/images/characters/arrow.png')
arrow_lt_img = flip_image_x(arrow_rt_img)

crystal_imgs = [load_image('assets/images/items/crystal_1.png'),
                load_image('assets/images/items/crystal_2.png'),
                load_image('assets/images/items/crystal_3.png'),
                load_image('assets/images/items/crystal_4.png'),
                load_image('assets/images/items/crystal_5.png'),
                load_image('assets/images/items/crystal_6.png')]


# ----- PLAYER/FRIEND/NPC IMAGES ----- #

merchant_imgs = [load_image('assets/images/characters/NPCS/merchant_1.png'),
                 load_image('assets/images/characters/NPCS/merchant_2.png'),
                 load_image('assets/images/characters/NPCS/merchant_3.png'),
                 load_image('assets/images/characters/NPCS/merchant_4.png'),
                 load_image('assets/images/characters/NPCS/merchant_5.png'),
                 load_image('assets/images/characters/NPCS/merchant_6.png'),
                 load_image('assets/images/characters/NPCS/merchant_7.png'),
                 load_image('assets/images/characters/NPCS/merchant_8.png'),
                 load_image('assets/images/characters/NPCS/merchant_9.png'),
                 load_image('assets/images/characters/NPCS/merchant_10.png')]

player_idle_rt_img = [load_image('assets/images/characters/player/idle_1.png'),
                      load_image('assets/images/characters/player/idle_2.png'),
                      load_image('assets/images/characters/player/idle_3.png'),
                      load_image('assets/images/characters/player/idle_4.png')]
player_idle_lt_img = [flip_image_x(img) for img in player_idle_rt_img]
player_run_rt_imgs = [load_image('assets/images/characters/player/run_1.png'),
                          load_image('assets/images/characters/player/run_2.png'),
                          load_image('assets/images/characters/player/run_3.png'),
                          load_image('assets/images/characters/player/run_4.png'),
                          load_image('assets/images/characters/player/run_5.png'),
                          load_image('assets/images/characters/player/run_6.png')]
player_run_lt_imgs = [flip_image_x(img) for img in player_run_rt_imgs]
player_walk_rt_imgs = [load_image('assets/images/characters/player/walk_1.png'),
                          load_image('assets/images/characters/player/walk_2.png'),
                          load_image('assets/images/characters/player/walk_3.png'),
                          load_image('assets/images/characters/player/walk_4.png'),
                          load_image('assets/images/characters/player/walk_5.png'),
                          load_image('assets/images/characters/player/walk_6.png')]
player_walk_lt_imgs = [flip_image_x(img) for img in player_walk_rt_imgs]
player_jump_rt_imgs = [load_image('assets/images/characters/player/jump_1.png'),
                       load_image('assets/images/characters/player/jump_2.png')]
player_jump_lt_imgs = [flip_image_x(img) for img in player_jump_rt_imgs]
player_crouch_rt_imgs = [load_image('assets/images/characters/player/crouch_1.png'),
                      load_image('assets/images/characters/player/crouch_2.png'),
                      load_image('assets/images/characters/player/crouch_3.png'),
                      load_image('assets/images/characters/player/crouch_4.png')]
player_crouch_lt_imgs = [flip_image_x(img) for img in player_crouch_rt_imgs]
player_fall_rt_imgs = [load_image('assets/images/characters/player/fall_1.png'),
                       load_image('assets/images/characters/player/fall_2.png')]
player_fall_lt_imgs = [flip_image_x(img) for img in player_fall_rt_imgs]
player_wall_slide_rt_imgs = [load_image('assets/images/characters/player/wall_slide_1.png'),
                             load_image('assets/images/characters/player/wall_slide_2.png')]
player_wall_slide_lt_imgs = [flip_image_x(img) for img in player_wall_slide_rt_imgs]
player_wall_jump_rt_imgs = [load_image('assets/images/characters/player/wall_jump_1.png'),
                             load_image('assets/images/characters/player/wall_jump_2.png')]
player_wall_jump_lt_imgs = [flip_image_x(img) for img in player_wall_jump_rt_imgs]
player_slide_rt_imgs = [load_image('assets/images/characters/player/slide_1.png'),
                        load_image('assets/images/characters/player/slide_2.png'),
                        load_image('assets/images/characters/player/slide_1.png'),
                        load_image('assets/images/characters/player/slide_2.png'),
                        load_image('assets/images/characters/player/slide_1.png'),
                        load_image('assets/images/characters/player/slide_2.png')]
player_slide_lt_imgs = [flip_image_x(img) for img in player_slide_rt_imgs]

# Weapon/attack Images

player_sword_draw_rt_imgs = [load_image('assets/images/characters/player/sword_draw_1.png'),
                             load_image('assets/images/characters/player/sword_draw_2.png'),
                             load_image('assets/images/characters/player/sword_draw_3.png'),
                             load_image('assets/images/characters/player/sword_draw_4.png'),
                             load_image('assets/images/characters/player/sword_draw_4.png')]
player_sword_draw_lt_imgs = [flip_image_x(img) for img in player_sword_draw_rt_imgs]
player_sword_crouch_rt_imgs = [load_image('assets/images/characters/player/sword_crouch.png')]
player_sword_crouch_lt_imgs = [flip_image_x(img) for img in player_sword_crouch_rt_imgs]
player_sword_idle_rt_imgs = [load_image('assets/images/characters/player/sword_idle_1.png'),
                             load_image('assets/images/characters/player/sword_idle_2.png'),
                             load_image('assets/images/characters/player/sword_idle_3.png'),
                             load_image('assets/images/characters/player/sword_idle_4.png')]
player_sword_idle_lt_imgs = [flip_image_x(img) for img in player_sword_idle_rt_imgs]
player_sword_sheathe_rt_imgs = [load_image('assets/images/characters/player/sword_draw_4.png'),
                                load_image('assets/images/characters/player/sword_draw_3.png'),
                                load_image('assets/images/characters/player/sword_draw_2.png'),
                                load_image('assets/images/characters/player/sword_draw_1.png')]
player_sword_sheathe_lt_imgs = [flip_image_x(img) for img in player_sword_sheathe_rt_imgs]
player_sword_walk_rt_imgs = [load_image('assets/images/characters/player/sword_walk_1.png'),
                          load_image('assets/images/characters/player/sword_walk_2.png'),
                          load_image('assets/images/characters/player/sword_walk_3.png'),
                          load_image('assets/images/characters/player/sword_walk_4.png'),
                          load_image('assets/images/characters/player/sword_walk_5.png'),
                          load_image('assets/images/characters/player/sword_walk_6.png')]
player_sword_walk_lt_imgs = [flip_image_x(img) for img in player_sword_walk_rt_imgs]
player_sword_attack_1_rt_imgs = [load_image('assets/images/characters/player/sword_attack_1_1.png'),
                                 load_image('assets/images/characters/player/sword_attack_1_2.png'),
                                 load_image('assets/images/characters/player/sword_attack_1_3.png'),
                                 load_image('assets/images/characters/player/sword_attack_1_4.png'),
                                 load_image('assets/images/characters/player/sword_attack_1_5.png')]
player_sword_attack_1_lt_imgs = [flip_image_x(img) for img in player_sword_attack_1_rt_imgs]
player_sword_attack_2_rt_imgs = [load_image('assets/images/characters/player/sword_attack_2_1.png'),
                                 load_image('assets/images/characters/player/sword_attack_2_2.png'),
                                 load_image('assets/images/characters/player/sword_attack_2_3.png'),
                                 load_image('assets/images/characters/player/sword_attack_2_4.png'),
                                 load_image('assets/images/characters/player/sword_attack_2_5.png')]
player_sword_attack_2_lt_imgs = [flip_image_x(img) for img in player_sword_attack_2_rt_imgs]
player_sword_attack_3_rt_imgs = [load_image('assets/images/characters/player/sword_attack_3_1.png'),
                                 load_image('assets/images/characters/player/sword_attack_3_2.png'),
                                 load_image('assets/images/characters/player/sword_attack_3_3.png'),
                                 load_image('assets/images/characters/player/sword_attack_3_4.png'),
                                 load_image('assets/images/characters/player/sword_attack_3_5.png')]
player_sword_attack_3_lt_imgs = [flip_image_x(img) for img in player_sword_attack_3_rt_imgs]

player_slash_1_rt_imgs = [load_image('assets/images/characters/player/slash_1_1.png'),
                          load_image('assets/images/characters/player/slash_1_2.png'),
                          load_image('assets/images/characters/player/slash_1_3.png'),
                          load_image('assets/images/characters/player/slash_1_4.png'),
                          load_image('assets/images/characters/player/slash_1_5.png'),
                          load_image('assets/images/characters/player/slash_1_6.png'),
                          load_image('assets/images/characters/player/slash_1_7.png'),
                          load_image('assets/images/characters/player/slash_1_8.png'),
                          load_image('assets/images/characters/player/slash_1_9.png'),
                          load_image('assets/images/characters/player/slash_1_10.png'),
                          load_image('assets/images/characters/player/slash_1_11.png')]
player_slash_1_lt_imgs = [flip_image_x(img) for img in player_slash_1_rt_imgs]
player_slash_2_rt_imgs = [flip_image_y(img) for img in player_slash_1_rt_imgs]
player_slash_2_lt_imgs = [flip_image_x(img) for img in player_slash_2_rt_imgs]
player_slash_3_rt_imgs = [load_image('assets/images/characters/player/slash_3_1.png'),
                          load_image('assets/images/characters/player/slash_3_2.png'),
                          load_image('assets/images/characters/player/slash_3_3.png'),
                          load_image('assets/images/characters/player/slash_3_4.png'),
                          load_image('assets/images/characters/player/slash_3_5.png'),
                          load_image('assets/images/characters/player/slash_3_6.png'),
                          load_image('assets/images/characters/player/slash_3_7.png'),
                          load_image('assets/images/characters/player/slash_3_8.png'),
                          load_image('assets/images/characters/player/slash_3_9.png')]
player_slash_3_lt_imgs = [flip_image_x(img) for img in player_slash_3_rt_imgs]


player_hit_1_rt_imgs = [load_image('assets/images/characters/player/punch_1_1.png'),
                        load_image('assets/images/characters/player/punch_1_2.png'),
                        load_image('assets/images/characters/player/punch_1_3.png'),
                        load_image('assets/images/characters/player/punch_1_4.png'),
                        load_image('assets/images/characters/player/punch_1_5.png')]
player_hit_1_lt_imgs = [flip_image_x(img) for img in player_hit_1_rt_imgs]
player_hit_2_rt_imgs = [load_image('assets/images/characters/player/punch_2_1.png'),
                        load_image('assets/images/characters/player/punch_2_2.png'),
                        load_image('assets/images/characters/player/punch_2_3.png'),
                        load_image('assets/images/characters/player/punch_2_4.png')]
player_hit_2_lt_imgs = [flip_image_x(img) for img in player_hit_2_rt_imgs]
player_hit_3_rt_imgs = [load_image('assets/images/characters/player/punch_3_1.png'),
                        load_image('assets/images/characters/player/punch_3_2.png'),
                        load_image('assets/images/characters/player/punch_3_3.png'),
                        load_image('assets/images/characters/player/punch_3_4.png')]
player_hit_3_lt_imgs = [flip_image_x(img) for img in player_hit_3_rt_imgs]


friend_1_img = load_image('assets/images/characters/friends/friend_1.png')

# ----- ENEMY IMAGES ----- #

guard_idle_lt_imgs = [load_image('assets/images/characters/enemies/guard_idle_1.png'),
                     load_image('assets/images/characters/enemies/guard_idle_2.png'),
                     load_image('assets/images/characters/enemies/guard_idle_3.png'),
                     load_image('assets/images/characters/enemies/guard_idle_4.png'),]
guard_idle_rt_imgs = [flip_image_x(img) for img in guard_idle_lt_imgs]
guard_walk_rt_imgs = [load_image('assets/images/characters/enemies/guard_walk_1.png'),
                     load_image('assets/images/characters/enemies/guard_walk_2.png'),
                     load_image('assets/images/characters/enemies/guard_walk_3.png'),
                     load_image('assets/images/characters/enemies/guard_walk_4.png'),
                     load_image('assets/images/characters/enemies/guard_walk_5.png'),
                     load_image('assets/images/characters/enemies/guard_walk_6.png'),
                     load_image('assets/images/characters/enemies/guard_walk_7.png'),
                     load_image('assets/images/characters/enemies/guard_walk_8.png')]
guard_walk_lt_imgs = [flip_image_x(img) for img in guard_walk_rt_imgs]
guard_attack_rt_imgs = [load_image('assets/images/characters/enemies/guard_hit_1.png'),
                     load_image('assets/images/characters/enemies/guard_hit_2.png'),
                     load_image('assets/images/characters/enemies/guard_hit_3.png'),
                     load_image('assets/images/characters/enemies/guard_hit_4.png'),
                     load_image('assets/images/characters/enemies/guard_hit_5.png'),
                     load_image('assets/images/characters/enemies/guard_hit_6.png'),
                     load_image('assets/images/characters/enemies/guard_hit_7.png'),
                     load_image('assets/images/characters/enemies/guard_hit_8.png')]
guard_attack_lt_imgs = [flip_image_x(img) for img in guard_attack_rt_imgs]
guard_hurt_rt_imgs = [load_image('assets/images/characters/enemies/guard_hurt.png'),
                      load_image('assets/images/characters/enemies/guard_hurt_2.png')]
guard_hurt_lt_imgs = [flip_image_x(img) for img in guard_hurt_rt_imgs]
guard_die_rt_imgs = [load_image('assets/images/characters/enemies/guard_death_1.png'),
                     load_image('assets/images/characters/enemies/guard_death_2.png'),
                     load_image('assets/images/characters/enemies/guard_death_3.png'),
                     load_image('assets/images/characters/enemies/guard_death_4.png'),
                     load_image('assets/images/characters/enemies/guard_death_5.png'),
                     load_image('assets/images/characters/enemies/guard_death_6.png')]
guard_die_lt_imgs = [flip_image_x(img) for img in guard_die_rt_imgs]
guard_icon_img = load_image('assets/images/characters/enemies/guard_icon.png')


bowman_idle_rt_imgs = [load_image('assets/images/characters/enemies/bowman_idle_1.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_2.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_3.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_4.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_5.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_6.png'),
                       load_image('assets/images/characters/enemies/bowman_idle_7.png')]
bowman_idle_lt_imgs = [flip_image_x(img) for img in bowman_idle_rt_imgs]
bowman_walk_rt_imgs = [load_image('assets/images/characters/enemies/bowman_walk_1.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_2.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_3.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_4.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_5.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_6.png'),
                       load_image('assets/images/characters/enemies/bowman_walk_7.png')]
bowman_walk_lt_imgs = [flip_image_x(img) for img in bowman_walk_rt_imgs]
bowman_attack_rt_imgs = [load_image('assets/images/characters/enemies/bowman_attack_1.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_2.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_3.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_4.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_5.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_6.png'),
                       load_image('assets/images/characters/enemies/bowman_attack_7.png')]
bowman_attack_lt_imgs = [flip_image_x(img) for img in bowman_attack_rt_imgs]
bowman_die_rt_imgs = [load_image('assets/images/characters/enemies/bowman_death_1.png'),
                     load_image('assets/images/characters/enemies/bowman_death_2.png'),
                     load_image('assets/images/characters/enemies/bowman_death_3.png'),
                     load_image('assets/images/characters/enemies/bowman_death_4.png'),
                     load_image('assets/images/characters/enemies/bowman_death_5.png'),
                     load_image('assets/images/characters/enemies/bowman_death_6.png')]
bowman_die_lt_imgs = [flip_image_x(img) for img in bowman_die_rt_imgs]
bowman_icon_img = load_image('assets/images/characters/enemies/bowman_icon.png')

elite_idle_rt_imgs = [load_image('assets/images/characters/enemies/elite_idle_1.png'),
                      load_image('assets/images/characters/enemies/elite_idle_2.png'),
                      load_image('assets/images/characters/enemies/elite_idle_3.png'),
                      load_image('assets/images/characters/enemies/elite_idle_4.png'),
                      load_image('assets/images/characters/enemies/elite_idle_5.png'),
                      load_image('assets/images/characters/enemies/elite_idle_6.png')]
elite_idle_lt_imgs = [flip_image_x(img) for img in elite_idle_rt_imgs]

elite_icon_img = load_image('assets/images/characters/enemies/elite_icon.png')


# ----- OTHER IMAGES ----- #

load_image('assets/images/other/title_screen/frame-1.png')
load_image('assets/images/other/title_screen/frame-2.png')
load_image('assets/images/other/title_screen/frame-3.png')
load_image('assets/images/other/title_screen/frame-4.png')
load_image('assets/images/other/title_screen/frame-5.png')
load_image('assets/images/other/title_screen/frame-6.png')
load_image('assets/images/other/title_screen/frame-7.png')
load_image('assets/images/other/title_screen/frame-8.png')
load_image('assets/images/other/title_screen/frame-9.png')
load_image('assets/images/other/title_screen/frame-10.png')
load_image('assets/images/other/title_screen/frame-11.png')
load_image('assets/images/other/start_screen/frame-1.png')
load_image('assets/images/other/start_screen/frame-2.png')
load_image('assets/images/other/start_screen/frame-3.png')
load_image('assets/images/other/start_screen/frame-4.png')
load_image('assets/images/other/start_screen/frame-5.png')
load_image('assets/images/other/start_screen/frame-6.png')
load_image('assets/images/other/start_screen/frame-7.png')
load_image('assets/images/other/start_screen/frame-8.png')
load_image('assets/images/other/start_screen/frame-9.png')
load_image('assets/images/other/start_screen/frame-10.png')
load_image('assets/images/other/start_screen/frame-11.png')
load_image('assets/images/other/hint_1/frame-1.png')
load_image('assets/images/other/hint_1/frame-2.png')
load_image('assets/images/other/hint_1/frame-3.png')
load_image('assets/images/other/hint_1/frame-4.png')
load_image('assets/images/other/hint_1/frame-5.png')
load_image('assets/images/other/hint_1/frame-6.png')
load_image('assets/images/other/hint_1/frame-7.png')
load_image('assets/images/other/hint_1/frame-8.png')
load_image('assets/images/other/hint_1/frame-9.png')
load_image('assets/images/other/hint_1/frame-10.png')
load_image('assets/images/other/hint_1/frame-11.png')
load_image('assets/images/other/hint_2/frame-1.png')
load_image('assets/images/other/hint_2/frame-2.png')
load_image('assets/images/other/hint_2/frame-3.png')
load_image('assets/images/other/hint_2/frame-4.png')
load_image('assets/images/other/hint_2/frame-5.png')
load_image('assets/images/other/hint_2/frame-6.png')
load_image('assets/images/other/hint_2/frame-7.png')
load_image('assets/images/other/hint_2/frame-8.png')
load_image('assets/images/other/hint_2/frame-9.png')
load_image('assets/images/other/hint_2/frame-10.png')
load_image('assets/images/other/hint_2/frame-11.png')
load_image('assets/images/other/hint_3/frame-1.png')
load_image('assets/images/other/hint_3/frame-2.png')
load_image('assets/images/other/hint_3/frame-3.png')
load_image('assets/images/other/hint_3/frame-4.png')
load_image('assets/images/other/hint_3/frame-5.png')
load_image('assets/images/other/hint_3/frame-6.png')
load_image('assets/images/other/hint_3/frame-7.png')
load_image('assets/images/other/hint_3/frame-8.png')
load_image('assets/images/other/hint_3/frame-9.png')
load_image('assets/images/other/hint_3/frame-10.png')
load_image('assets/images/other/hint_3/frame-11.png')
load_image('assets/images/other/hint_4/frame-1.png')
load_image('assets/images/other/hint_4/frame-3.png')
load_image('assets/images/other/hint_4/frame-2.png')
load_image('assets/images/other/hint_4/frame-4.png')
load_image('assets/images/other/hint_4/frame-5.png')
load_image('assets/images/other/hint_4/frame-6.png')
load_image('assets/images/other/hint_4/frame-7.png')
load_image('assets/images/other/hint_4/frame-8.png')
load_image('assets/images/other/hint_4/frame-9.png')
load_image('assets/images/other/hint_4/frame-10.png')
load_image('assets/images/other/hint_4/frame-11.png')
load_image('assets/images/other/instructions/frame-1.png')
load_image('assets/images/other/instructions/frame-2.png')
load_image('assets/images/other/instructions/frame-3.png')
load_image('assets/images/other/instructions/frame-4.png')
load_image('assets/images/other/instructions/frame-5.png')
load_image('assets/images/other/instructions/frame-6.png')
load_image('assets/images/other/instructions/frame-7.png')
load_image('assets/images/other/instructions/frame-8.png')
load_image('assets/images/other/instructions/frame-9.png')
load_image('assets/images/other/instructions/frame-10.png')
load_image('assets/images/other/instructions/frame-11.png')
load_image('assets/images/other/shop/frame-0.png')
load_image('assets/images/other/shop/frame-1.png')
load_image('assets/images/other/shop/frame-2.png')
load_image('assets/images/other/shop/frame-3.png')
load_image('assets/images/other/shop/frame-4.png')
load_image('assets/images/other/shop/frame-5.png')
load_image('assets/images/other/shop/frame-6.png')
load_image('assets/images/other/shop/frame-7.png')
load_image('assets/images/other/shop/frame-8.png')
load_image('assets/images/other/shop/frame-9.png')
load_image('assets/images/other/shop/frame-10.png')
load_image('assets/images/other/shop/frame-11.png')

blank_img = load_image('assets/images/other/blank.png')
cursor_img = load_image('assets/images/other/cursor.png')
pause_icon = load_image('assets/images/other/pause.png')
attack_overlay_img = load_image('assets/images/other/attack_overlay.png')
spacebar_img = load_image('assets/images/other/spacebar.png')
blood_imgs = [load_image('assets/images/characters/blood_1.png'),
              load_image('assets/images/characters/blood_2.png'),
              load_image('assets/images/characters/blood_3.png'),
              load_image('assets/images/characters/blood_4.png')]
spark_imgs = [load_image('assets/images/characters/spark_1.png'),
              load_image('assets/images/characters/spark_2.png'),
              load_image('assets/images/characters/spark_3.png'),
              load_image('assets/images/characters/spark_4.png')]
coin_img = load_image('assets/images/items/coin_gold.png')
counterx2_img = load_image('assets/images/other/counterx2.png')
counterx3_img = load_image('assets/images/other/counterx3.png')





# Load sounds
sword_swoosh_snd = load_sound('assets/sounds/sword_swoosh.ogg')
merchant_snd = load_sound('assets/sounds/merchant_snd.ogg')
error_snd = load_sound('assets/sounds/error.ogg')
purchase_snd = load_sound('assets/sounds/cash_out.ogg')
pickup_coin_snd = load_sound('assets/sounds/coin.ogg')
walk_snd = load_sound('assets/sounds/walk.ogg')
fall_snd = load_sound('assets/sounds/fall.ogg')
ambient_wind_snd = ('assets/sounds/ambient_wind.ogg')

# Load music
title_music = ('assets/music/irrational_machines.ogg')
theme_music = ('assets/music/theme.ogg')
boss_music = ('assets/music/boss_music.ogg')

# Levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json',
          'assets/levels/world-4.json',
          'assets/levels/world-5.json']

# Other constants and settings
START = 0
PLAYING = 1
PAUSED = 2
WIN = 3
LOSE = 4
INSTRUCTIONS = 5
PLAYING_TUTORIAL = 6
MENU = 7



# directions
LEFT = -1
STAY = 0
RIGHT = 1