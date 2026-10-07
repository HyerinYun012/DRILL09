from pico2d import *


CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024

FRAME_WIDTH = 100
FRAME_HEIGHT = 100
IDLE_ROW_Y = {
    'right': 300,
    'left': 200,
}

BACKGROUND_PATH = 'TUK_GROUND.png'
CHARACTER_PATH = 'animation_sheet.png'

FRAME_DELAY = 0.05
MOVE_STEP = 5

STATE_IDLE = 'idle'
STATE_MOVE = 'move'


running = True
character_x = CANVAS_WIDTH // 2
character_y = CANVAS_HEIGHT // 2
facing = 'right'
animation_state = STATE_IDLE
pressed_keys = set()


def handle_events():
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                pressed_keys.add('left')
            elif event.key == SDLK_RIGHT:
                pressed_keys.add('right')
            elif event.key == SDLK_UP:
                pressed_keys.add('up')
            elif event.key == SDLK_DOWN:
                pressed_keys.add('down')
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                pressed_keys.discard('left')
            elif event.key == SDLK_RIGHT:
                pressed_keys.discard('right')
            elif event.key == SDLK_UP:
                pressed_keys.discard('up')
            elif event.key == SDLK_DOWN:
                pressed_keys.discard('down')


def get_movement():
    dx = int('right' in pressed_keys) - int('left' in pressed_keys)
    dy = int('up' in pressed_keys) - int('down' in pressed_keys)
    return dx, dy


def update_character():
    global character_x, character_y, facing, animation_state

    dx, dy = get_movement()

    if dx > 0:
        facing = 'right'
    elif dx < 0:
        facing = 'left'

    animation_state = STATE_MOVE if dx != 0 or dy != 0 else STATE_IDLE

    character_x += dx * MOVE_STEP
    character_y += dy * MOVE_STEP


def draw_world(background, character):
    row_y = IDLE_ROW_Y[facing]

    clear_canvas()
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    character.clip_draw(
        0, row_y, FRAME_WIDTH, FRAME_HEIGHT,
        character_x, character_y,
    )
    update_canvas()


def main():
    global running

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        background = load_image(BACKGROUND_PATH)
        character = load_image(CHARACTER_PATH)

        while running:
            handle_events()
            update_character()
            draw_world(background, character)
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
