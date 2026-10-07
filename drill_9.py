from pico2d import *


CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024

FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
MIN_X = FRAME_WIDTH // 2
MAX_X = CANVAS_WIDTH - FRAME_WIDTH // 2
MIN_Y = FRAME_HEIGHT // 2
MAX_Y = CANVAS_HEIGHT - FRAME_HEIGHT // 2
IDLE_ROW_Y = {
    'right': 300,
    'left': 200,
}
RUN_ROW_Y = {
    'right': 100,
    'left': 0,
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
animation_frame = 0
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


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def update_character():
    global character_x, character_y, facing, animation_state

    dx, dy = get_movement()
    previous_state = animation_state

    if dx > 0:
        facing = 'right'
    elif dx < 0:
        facing = 'left'

    animation_state = STATE_MOVE if dx != 0 or dy != 0 else STATE_IDLE

    character_x = clamp(character_x + dx * MOVE_STEP, MIN_X, MAX_X)
    character_y = clamp(character_y + dy * MOVE_STEP, MIN_Y, MAX_Y)

    return animation_state != previous_state


def update_animation(state_changed):
    global animation_frame

    if state_changed:
        animation_frame = 0
    else:
        animation_frame = (animation_frame + 1) % FRAME_COUNT


def draw_world(background, character):
    if animation_state == STATE_MOVE:
        row_y = RUN_ROW_Y[facing]
    else:
        row_y = IDLE_ROW_Y[facing]

    clear_canvas()
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    character.clip_draw(
        animation_frame * FRAME_WIDTH, row_y, FRAME_WIDTH, FRAME_HEIGHT,
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
            state_changed = update_character()
            update_animation(state_changed)
            draw_world(background, character)
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
