from pico2d import *


CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024

FRAME_WIDTH = 100
FRAME_HEIGHT = 100

BACKGROUND_PATH = 'TUK_GROUND.png'
CHARACTER_PATH = 'animation_sheet.png'

FRAME_DELAY = 0.05


running = True
character_x = CANVAS_WIDTH // 2
character_y = CANVAS_HEIGHT // 2


def handle_events():
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw_world(background, character):
    clear_canvas()
    background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    character.clip_draw(
        0, 300, FRAME_WIDTH, FRAME_HEIGHT,
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
            draw_world(background, character)
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
