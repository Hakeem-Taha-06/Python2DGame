#map dimensions
ORIGINAL_TILE_SIZE = 16
SCALE = 4
TILE_SIZE = ORIGINAL_TILE_SIZE*SCALE
MAP_WIDTH = 20 * TILE_SIZE
MAP_HEIGHT = 12 * TILE_SIZE
FPS = 60
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass' : -10,
    'invisible' : 0,
}
#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 160
ITEM_BOX_SIZE = 125
UI_FONT = './graphics/fonts/X12Y16PXMARUMONICA.TTF'
UI_FONT_SIZE = 40
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = "#3E3E3E"
UI_BG_COLOR_ACTIVE = "#7B7B7B"
UI_BORDER_COLOR = "#2A004C"
TEXT_COLOR = '#EEEEEE'
TEXT_COLOR_ACTIVE = 'gold'
BAR_COLOR = '#7B7B7B'
BAR_COLOR_ACTIVE = '#3E3E3E'

#weapons
weapon_data = {
    'knight': { 'lance' : {'cooldown' : 300, 'attack_time': 200, 'damage' : 10, 'graphic' : 'graphics/weapons/lance/full_up.png'},
                'axe' : {'cooldown' : 800, 'attack_time': 400, 'damage' : 35, 'graphic' : 'graphics/weapons/axe/full_up.png'},
                'sword' : {'cooldown' : 400, 'attack_time': 300, 'damage' : 15, 'graphic' : 'graphics/weapons/sword/full_up.png'},
                },
    'fighter': { 'hatchet' : {'cooldown' : 300, 'attack_time': 200, 'damage' : 15, 'graphic' : 'graphics/weapons/hatchet/full_up.png'},
                'axe' : {'cooldown' : 600, 'attack_time': 400, 'damage' : 35, 'graphic' : 'graphics/weapons/axe/full_up.png'},
                'greatsword' : {'cooldown' : 400, 'attack_time': 300, 'damage' : 20, 'graphic' : 'graphics/weapons/greatsword/full_up.png'},
                },
    'mage': { 'sword' : {'cooldown' : 400, 'attack_time': 300, 'damage' : 15, 'graphic' : 'graphics/weapons/sword/full_up.png'},
                },
    'monk': { 'hatchet' : {'cooldown' : 300, 'attack_time': 200, 'damage' : 15, 'graphic' : 'graphics/weapons/hatchet/full_up.png'},
                'axe' : {'cooldown' : 600, 'attack_time': 400, 'damage' : 35, 'graphic' : 'graphics/weapons/axe/full_up.png'},
                'greatsword' : {'cooldown' : 400, 'attack_time': 300, 'damage' : 20, 'graphic' : 'graphics/weapons/greatsword/full_up.png'},
                },
    'archer': { 'lance' : {'cooldown' : 300, 'attack_time': 200, 'damage' : 10, 'graphic' : 'graphics/weapons/lance/full_up.png'},
                'axe' : {'cooldown' : 800, 'attack_time': 400, 'damage' : 35, 'graphic' : 'graphics/weapons/axe/full_up.png'},
                'sword' : {'cooldown' : 400, 'attack_time': 300, 'damage' : 15, 'graphic' : 'graphics/weapons/sword/full_up.png'},
                },
}

#magic
magic_data = {
    'knight': { 'holy' : {'strength': 20, 'cost': 20, 'duration' : 0, 'graphic': 'graphics/magic/holy/icon.png'},
                'heal' : {'strength': 40, 'cost': 40, 'duration' : 0, 'graphic': 'graphics/magic/heal/icon.png'},
               },
    'fighter': { 'fire' : {'strength': 30, 'cost': 10, 'duration' : 0, 'graphic': 'graphics/magic/fire/icon.png'},
                'boost' : {'strength': 10, 'cost': 20, 'duration' : 10000, 'graphic': 'graphics/magic/boost/icon.png'},
               },
    'mage': {   'holy' : {'strength': 30, 'cost': 30, 'duration' : 0, 'graphic': 'graphics/magic/holy/icon.png'},
                'heal' : {'strength': 40, 'cost': 40, 'duration' : 0, 'graphic': 'graphics/magic/heal/icon.png'},
                'fire' : {'strength': 10, 'cost': 10, 'duration' : 0, 'graphic': 'graphics/magic/fire/icon.png'},
               },
    'monk': {   'fire' : {'strength': 30, 'cost': 10, 'duration' : 0, 'graphic': 'graphics/magic/fire/icon.png'},
                'boost' : {'strength': 10, 'cost': 20, 'duration' : 10000, 'graphic': 'graphics/magic/boost/icon.png'},
               },
    'archer': { 'holy' : {'strength': 20, 'cost': 20, 'duration' : 0, 'graphic': 'graphics/magic/holy/icon.png'},
                'heal' : {'strength': 40, 'cost': 40, 'duration' : 0, 'graphic': 'graphics/magic/heal/icon.png'},
               },
}

#classes
character_data = {
    'knight' : {'health': 120, 'energy': 80, 'attack': 12, 'magic': 6, 'speed': 3, 'graphic': 'graphics/player/knight/showcase.png'},
    'fighter' : {'health': 100, 'energy': 20, 'attack': 14, 'magic': 1, 'speed': 4, 'graphic': 'graphics/player/fighter/showcase.png'},
    'mage' : {'health': 80, 'energy': 100, 'attack': 5, 'magic': 10, 'speed': 3, 'graphic': 'graphics/player/mage/showcase.png'},
    'monk' : {'health': 120, 'energy': 0, 'attack': 14, 'magic': 0, 'speed': 3, 'graphic': 'graphics/player/monk/showcase.png'},
    'archer' : {'health': 80, 'energy': 20, 'attack': 8, 'magic': 3, 'speed': 4, 'graphic': 'graphics/player/archer/showcase.png'}
}

max_stats = {
    'knight' : {'health': 340, 'energy': 160, 'attack': 24, 'magic': 10, 'speed': 5},
    'fighter' : {'health': 300, 'energy': 40, 'attack': 30, 'magic': 5, 'speed': 6},
    'mage' : {'health': 200, 'energy': 200, 'attack': 10, 'magic': 20, 'speed': 6},
    'monk' : {'health': 400, 'energy': 0, 'attack': 40, 'magic': 0, 'speed': 7},
    'archer' : {'health': 200, 'energy': 40, 'attack': 20, 'magic': 8, 'speed': 7}
}

growth_rates = {
    'knight' : {'health': 20, 'energy': 10, 'attack': 2, 'magic': 1, 'speed': 1},
    'fighter' : {'health': 20, 'energy': 10, 'attack': 4, 'magic': 1, 'speed': 1},
    'mage' : {'health': 20, 'energy': 20, 'attack': 1, 'magic': 2, 'speed': 1},
    'monk' : {'health': 40, 'energy': 0, 'attack': 4, 'magic': 0, 'speed': 1},
    'archer' : {'health': 20, 'energy': 10, 'attack': 2, 'magic': 1, 'speed': 1}
}

upgrade_cost = {'health' : 100, 'energy' : 200, 'attack' : 150, 'magic' : 200, 'speed' : 400}

#enemy
monster_data = {
    'slime' : {'health': 50, 'exp': 100, 'damage': 10, 'attack_type': 'ice', 'attack_sound': 'audio/water1.wav', 'speed': 3, 'resistance': 200, 'attack_radius' : 80, 'notice_radius' : 360, 'death_sound': 'audio/slime_death.wav'},
    'bamboo' : {'health': 100, 'exp': 150, 'damage': 8, 'attack_type': 'grass', 'attack_sound': 'audio/grass.wav', 'speed': 4, 'resistance': 10, 'attack_radius' : 80, 'notice_radius' : 360, 'death_sound': 'audio/bamboo_death.wav'},
    'raccoon' : {'health': 250, 'exp': 300, 'damage': 20, 'attack_type': 'claw', 'attack_sound': 'audio/claw.wav', 'speed': 3, 'resistance': 3, 'attack_radius' : 120, 'notice_radius' : 360, 'death_sound': 'audio/raccoon_death.wav'},
}