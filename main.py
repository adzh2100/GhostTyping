import pygame
import pygame_gui
from lib.constants import INITIAL_SPEED_CHANGE_TIME, SPEED_CHANGE_TRESHOLD, SPEED_GAP
from services.screen_service import ScreenService

pygame.init()
pygame.key.set_repeat(500, 200)


def main():
    run = True
    screen = ScreenService()

    screen.draw_window()
    time_elapsed_since_last_action = 0
    time_elapsed_playing = 0
    time_gap = INITIAL_SPEED_CHANGE_TIME
    started = False
    first_run = True
    on_menu_page = True
    on_game_over = True

    while run:
        dt = screen.clock.tick(50)
        if not screen.has_lives():
            screen.game_over(time_elapsed_playing)
            on_game_over = True
            started = False
            time_elapsed_playing = 0
            time_gap = INITIAL_SPEED_CHANGE_TIME
            time_elapsed_since_last_action = 0

        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == screen.start_button:
                    on_menu_page = False
                    on_game_over = False
                    started = True
                    first_run = True
                    screen.on_start_clicked()

                if event.ui_element == screen.quit_button:
                    run = False

                if event.ui_element == screen.menu_button:
                    on_menu_page = True
                    on_game_over = False
                    screen.show_menu()

                if event.ui_element == screen.play_again_button:
                    on_menu_page = False
                    on_game_over = False
                    started = True
                    first_run = True
                    screen.on_play_again_clicked()

                if event.ui_element == screen.leaderboard_button:
                    on_game_over = False
                    on_menu_page = False
                    screen.on_leaderboard_clicked()

                if event.ui_element == screen.save_score_button:
                    on_menu_page = False
                    on_game_over = False
                    screen.on_save_clicked()

                if event.ui_element == screen.settings_button:
                    on_menu_page = False
                    on_game_over = False
                    screen.on_settings_clicked()

            elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == screen.difficulty_component:
                    screen.update_difficulty()

                if event.ui_element == screen.music_component:
                    screen.update_music()

            if event.type == pygame.QUIT:
                run = False

            if started and event.type == pygame.KEYDOWN:
                screen.update_fields(event.key)

            if not started and event.type == pygame.KEYDOWN and on_game_over:
                screen.update_name(event.key)

            screen.manager.process_events(event)

        if started:
            time_elapsed_playing += dt
            time_elapsed_since_last_action += dt

            if time_elapsed_since_last_action > time_gap or first_run:
                screen.add_new_word()
                time_elapsed_since_last_action = 0
                first_run = False

            for i in range(1, 5):
                if time_elapsed_playing > SPEED_CHANGE_TRESHOLD * i:
                    time_gap = INITIAL_SPEED_CHANGE_TIME - SPEED_GAP * i

            screen.increase_ghosts_size()
            screen.update_ghosts()

        elif not started and on_menu_page:
            screen.update()

        screen.manager.update(dt)
        screen.manager.draw_ui(screen.screen)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
