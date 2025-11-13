import pygame
from utility import load_horizontal_animation_sheet, import_image_from_folder
from settings import TILE_SIZE
from random import choice, randint
class AnimationPlayer:
    def __init__(self):
        self.frames = {
            #magic
            'holy' : load_horizontal_animation_sheet('graphics/magic/holy/sheet.png', 4*TILE_SIZE, 4*TILE_SIZE),
            'heal' : load_horizontal_animation_sheet('graphics/magic/heal/sheet.png', 212, 140),
            'fire' : load_horizontal_animation_sheet('graphics/magic/fire/sheet.png', 32, 48),
            'boost' : load_horizontal_animation_sheet('graphics/magic/boost/sheet.png', 100, 96),
                        
            #attacks
            'claw' : load_horizontal_animation_sheet('graphics/attacks/claw/sheet.png', 2*TILE_SIZE, 2*TILE_SIZE),
            'grass' : load_horizontal_animation_sheet('graphics/attacks/grass/sheet.png', 96, 104),
            'ice' : load_horizontal_animation_sheet('graphics/attacks/ice/sheet.png', 2*TILE_SIZE, 2*TILE_SIZE),
            
            #effects
            'heal_aura' : load_horizontal_animation_sheet('graphics/particles/heal_aura.png', 2*TILE_SIZE, 2*TILE_SIZE),
            
            #monster deaths
            'slime' : load_horizontal_animation_sheet('graphics/particles/blue_smoke.png', 2*TILE_SIZE, 2*TILE_SIZE),
            'raccoon' :load_horizontal_animation_sheet('graphics/particles/big_orange_smoke.png', 4*TILE_SIZE, 4*TILE_SIZE),
            'bamboo' : load_horizontal_animation_sheet('graphics/particles/bamboo.png', TILE_SIZE, 75),

            #leafs
            'leaf' : (import_image_from_folder('graphics/particles/leaf1'),
                      import_image_from_folder('graphics/particles/leaf2'),
                      import_image_from_folder('graphics/particles/leaf3'),
                      import_image_from_folder('graphics/particles/leaf4'),
                      import_image_from_folder('graphics/particles/leaf5'),
                      import_image_from_folder('graphics/particles/leaf6'),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf1')),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf2')),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf3')),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf4')),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf5')),
                      self.reflect_images(import_image_from_folder('graphics/particles/leaf6'))
                ),
        }
    
    def reflect_images(self, frames):
        flipped_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            flipped_frames.append(flipped_frame)
        return flipped_frames
    
    def create_grass_particles(self, sprite_type, pos, groups):
        for _ in range(randint(3,6)):
            animation_frames = choice(self.frames['leaf'])
            x_offset = choice([-20, -15 ,-10 ,0 , 0, 10, 15, 20])
            y_offset = choice([-10, -7 ,-5 ,0 , 0, 5, 7, 10])
            offset = pygame.math.Vector2(x_offset, y_offset - 32)
            pos += offset
            ParticleEffect(pos, sprite_type, animation_frames,randint(2,5)*0.1, groups)
    
    def create_particles(self, sprite_type, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, sprite_type, animation_frames, 0.2, groups)
            

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_type ,animation_frames, animation_speed, groups):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): 
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()