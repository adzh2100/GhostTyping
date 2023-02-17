import pygame
import pygame_gui
from lib.constants import *
from services.game_service import GameService
from models.name_field import NameField


class ScreenService:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ghost Typing!")

        house = pygame.image.load("assets/images/house.jpeg").convert()
        logo = pygame.image.load("assets/images/logo.png")
        self._house = pygame.transform.smoothscale(house, self.screen.get_size())
        self._logo = pygame.transform.smoothscale(logo, (1000, 1000))
        self._leaderboard_image = pygame.image.load("assets/images/leaderboard.png")
        self._settings_image = pygame.image.load("assets/images/settings.png")
        self._difficulty_image = pygame.image.load("assets/images/difficulty.png")
        self._music_image = pygame.image.load("assets/images/music.png")
        self._translucent_ghost_image = pygame.image.load(
            "assets/images/translucent-ghost.png"
        )
        self._translucent_ghost_image_2 = pygame.image.load(
            "assets/images/translucent_ghost_2.png"
        )
        self._bat_image = pygame.image.load("assets/images/bat.png")
        self._initial_bat_image = self._bat_image

        # Clock
        self.clock = pygame.time.Clock()

        # Text font
        self._font_input = pygame.font.Font("assets/fonts/carnevalee_freakshow.ttf", 32)
        self._font_game_over = pygame.font.Font(
            "assets/fonts/carnevalee_freakshow.ttf", 64
        )

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

        center_x = WINDOW_WIDTH // 2 - BUTTON_SIZE[0] // 2
        center_y = WINDOW_HEIGHT // 2

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, center_y), BUTTON_SIZE),
            text="Start",
            manager=self.manager,
        )
        self.leaderboard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x, center_y + BUTTON_SIZE[1] + 10), BUTTON_SIZE
            ),
            text="Leaderboard",
            manager=self.manager,
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x, center_y + (BUTTON_SIZE[1] + 10) * 2), BUTTON_SIZE
            ),
            text="Settings",
            manager=self.manager,
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x, center_y + (BUTTON_SIZE[1] + 10) * 3), BUTTON_SIZE
            ),
            text="Quit",
            manager=self.manager,
        )
        self.save_score_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, center_y), BUTTON_SIZE),
            text="Save score",
            manager=self.manager,
            visible=False,
        )
        self.play_again_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x, (center_y + BUTTON_SIZE[1] + 10)), BUTTON_SIZE
            ),
            text="Play again",
            manager=self.manager,
            visible=False,
        )
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (center_x, (center_y + BUTTON_SIZE[1] + 10) * 2), BUTTON_SIZE
            ),
            text="Menu",
            manager=self.manager,
            visible=False,
        )

        self.leaderboard_component = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                (100, 110), (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 300)
            ),
            html_text="",
            manager=self.manager,
            visible=False,
        )

        self.difficulty_component = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 125, 420), (250, 66)),
            manager=self.manager,
            item_list=["Easy", "Medium", "Hard"],
            default_selection="Easy",
            visible=False,
        )

        self.music_component = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 125, 590), (250, 46)),
            item_list=["On", "Off"],
            default_selection="On",
            visible=False,
        )

        self.wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.mp3")
        pygame.mixer.music.load("assets/sounds/soundtrack.mp3")
        pygame.mixer.music.play(-1)

        self._playing = False
        self._game_service = GameService()
        self._input_fields = []
        self._name_input = NameField(
            WINDOW_WIDTH // 2 - 320 // 2, WINDOW_HEIGHT // 2 - 32 // 2 - 30, "..."
        )
        self._background_starting_position = (
            -self._translucent_ghost_image.get_width(),
            WINDOW_HEIGHT // 2,
        )
        self.y_change = 1
        self.bat_coordinates = self._game_service.generate_random_coordinates()

    def draw_window(self):
        self.screen.blit(self._house, (0, 0))
        self.screen.blit(self._logo, (WINDOW_WIDTH // 10, -WINDOW_HEIGHT // 7))

    def add_new_word(self):
        box = self._game_service.generate_random_box(self._input_fields)
        self._input_fields.append(box)

        x, y = box.get_coordinates()
        txt_surface = self._font_input.render(box.get_text(), True, box.get_color())

        ghost_offset = 20

        rect = box.get_box()

        self.screen.blit(box.get_ghost(), (x - ghost_offset, y - ghost_offset * 2))
        self.screen.blit(
            txt_surface,
            (
                rect.center[0] - txt_surface.get_width() // 2,
                rect.center[1] - txt_surface.get_height() // 2,
            ),
        )

        pygame.draw.rect(self.screen, box.get_color(), rect, border_radius=5)
        pygame.draw.rect(
            self.screen,
            COLOR_BLACK,
            (rect.x - 1, rect.y - 1, rect.width + 2, rect.height + 2),
            width=2,
            border_radius=5,
        )

    def update_fields(self, key):
        if key in KEY_LETTER_MAP:
            letter = KEY_LETTER_MAP[key]
            active_fields = list(
                filter(lambda field: field.is_active(), self._input_fields)
            )
            valid = False
            if len(active_fields) == 0:
                active_fields = self._input_fields
            for box in active_fields:
                text = box.get_text()
                if text[0] == letter:
                    self._input_fields.remove(box)
                    box.set_text(text[1:])

                    if box.get_text() != "":
                        self._input_fields.append(box)
                    else:
                        self._game_service.add_points(box)

                    self.rerender()
                    valid = True
                    break
            if not valid:
                pygame.mixer.Sound.play(self.wrong_sound)
        elif key == pygame.K_BACKSPACE:
            active_fields = list(
                filter(lambda field: field.is_active(), self._input_fields)
            )
            if len(active_fields) == 0:
                pygame.mixer.Sound.play(self.wrong_sound)
            else:
                field = active_fields[0]
                field.deactivate()
        else:
            pygame.mixer.Sound.play(self.wrong_sound)

    def rerender(self):
        self.screen.blit(self._house, (0, 0))
        if self._playing:
            x = LIVES_OFFSET
            distance = LIFE_SIZE[0] + 1

            for life in self._game_service.get_lives():
                if life.is_used():
                    self.screen.blit(life.get_icon_inactive(), (x, 0))
                else:
                    self.screen.blit(life.get_icon_active(), (x, 0))
                x = x + distance

        for field in self._input_fields:
            x, y = field.get_coordinates()

            box = field.get_box()

            ghost_offset = 20

            txt_surface = self._font_input.render(field.get_text(), True, COLOR_BLACK)
            self.screen.blit(
                field.get_ghost(), (x - ghost_offset, y - ghost_offset * 2)
            )

            pygame.draw.rect(self.screen, field.get_color(), box, border_radius=5)
            pygame.draw.rect(
                self.screen,
                COLOR_BLACK,
                (box.x - 1, box.y - 1, box.width + 2, box.height + 2),
                width=2,
                border_radius=5,
            )

            self.screen.blit(
                txt_surface,
                (
                    box.center[0] - txt_surface.get_width() // 2,
                    box.center[1] - txt_surface.get_height() // 2,
                ),
            )

    def increase_ghosts_size(self):
        for field in self._input_fields:
            field.enlarge_ghost()
            self.rerender()

    def update_ghosts(self):
        for field in self._input_fields:
            if field.get_ghost_size() > (MAX_GHOST_SIZE, MAX_GHOST_SIZE):
                self._input_fields.remove(field)
                self._game_service.remove_life()
                self.rerender()

    def has_lives(self):
        return self._game_service.has_lives()

    def hide_after_buttons(self):
        self.save_score_button.hide()
        self.play_again_button.hide()
        self.menu_button.hide()
        self.leaderboard_component.hide()
        self._game_service.reset()

    def show_after_buttons(self):
        center_x = WINDOW_WIDTH // 2 - BUTTON_SIZE[0] // 2
        center_y = WINDOW_HEIGHT // 2

        self.save_score_button.show()
        self.play_again_button.show()
        self.menu_button.set_position((center_x, center_y + (BUTTON_SIZE[1] + 10) * 2))
        self.menu_button.show()

    def show_menu_buttons(self):
        self.music_component.hide()
        self.difficulty_component.hide()
        self.start_button.show()
        self.settings_button.show()
        self.leaderboard_button.show()
        self.quit_button.show()

    def hide_menu_buttons(self):
        self.start_button.hide()
        self.leaderboard_button.hide()
        self.settings_button.hide()
        self.quit_button.hide()
        self._game_service.reset()

    def show_menu(self):
        self.draw_window()
        self.hide_after_buttons()
        self.show_menu_buttons()

    def refill_lifes(self):
        return self._game_service.refill_lives()

    def game_over(self, time_elapsed_playing):
        self._game_service.set_time_elapsed_playing(time_elapsed_playing)
        self.screen.blit(self._house, (0, 0))
        self._input_fields = []
        self._playing = False
        self.show_after_buttons()
        self.show_score()
        self.refill_lifes()

    def show_score(self):
        points = str(self._game_service.get_points())
        game_over_text = "Game over! Your score is " + points + " points"
        txt_surface = self._font_game_over.render(
            game_over_text, True, COLOR_WHITE, COLOR_BLACK
        )

        self.screen.blit(
            txt_surface,
            (
                WINDOW_WIDTH // 2 - txt_surface.get_width() // 2,
                WINDOW_HEIGHT // 2 - 150,
            ),
        )
        txt_surface = self._font_input.render(
            self._name_input.get_text(), True, COLOR_WHITE
        )

        pygame.draw.rect(self.screen, COLOR_GREY, self._name_input.get_box())
        pygame.draw.rect(
            self.screen,
            COLOR_BLACK,
            (
                WINDOW_WIDTH // 2 - (self._name_input.get_box().width + 4) // 2,
                WINDOW_HEIGHT // 2 - (self._name_input.get_box().height + 4) // 2 - 30,
                324,
                34,
            ),
            2,
        )

        self.screen.blit(
            txt_surface,
            (
                WINDOW_WIDTH // 2 - txt_surface.get_width() // 2 + 5,
                WINDOW_HEIGHT // 2 - txt_surface.get_height() // 2 - 30,
            ),
        )

    def update_name(self, key):
        current_text = self._name_input.get_text()

        if key in KEY_LETTER_MAP:
            letter = KEY_LETTER_MAP[key]
            self._name_input.set_text(current_text + letter)
        elif key == pygame.K_BACKSPACE:
            self._name_input.set_text(current_text[:-1])

        self.screen.blit(self._house, (0, 0))
        self.show_score()

    def on_start_clicked(self):
        self.hide_menu_buttons()
        self._playing = True

    def on_save_clicked(self):
        user = self._name_input.get_text()
        self._game_service.save_score(user)
        self._game_service.reset()

        self._name_input.set_text("...")
        self.hide_after_buttons()
        self.show_leaderboard()

    def on_leaderboard_clicked(self):
        self.hide_menu_buttons()
        self.show_leaderboard()

    def on_play_again_clicked(self):
        self.hide_after_buttons()
        self._playing = True

    def on_settings_clicked(self):
        self.hide_menu_buttons()
        self.show_settings()

    def show_leaderboard(self):
        self.screen.blit(self._house, (0, 0))
        center_x = WINDOW_WIDTH // 2 - BUTTON_SIZE[0] // 2

        self.screen.blit(self._leaderboard_image, (WINDOW_WIDTH // 2 - 250, -175))
        self.leaderboard_component.show()
        self.menu_button.set_position((center_x, WINDOW_HEIGHT - 150))
        self.menu_button.show()
        self.leaderboard_component.clear()
        scores = self._game_service.get_leaderboard()

        counter = 1
        for score in scores:
            place = str(counter)
            name = score.get_name()
            points = score.get_points()
            self.leaderboard_component.append_html_text(
                place + ". " + name + " - " + points + "\n"
            )
            counter += 1

    def show_settings(self):
        self.screen.blit(self._house, (0, 0))
        self.screen.blit(self._settings_image, (WINDOW_WIDTH // 2 - 250, 0))
        self.screen.blit(self._difficulty_image, (WINDOW_WIDTH // 2 - 250, 150))
        self.difficulty_component.show()
        self.screen.blit(self._music_image, (WINDOW_WIDTH // 2 - 250, 320))

        self.music_component.show()
        center_x = WINDOW_WIDTH // 2 - BUTTON_SIZE[0] // 2
        self.menu_button.set_position((center_x, WINDOW_HEIGHT - 250))
        self.menu_button.show()

    def update(self):
        self.draw_window()

        if self._bat_image.get_width() < 500:
            self._bat_image = pygame.transform.smoothscale(
                self._initial_bat_image,
                (self._bat_image.get_width() + 1, self._bat_image.get_height() + 1),
            )
        else:
            self.bat_coordinates = self._game_service.generate_random_coordinates()
            self._bat_image = pygame.transform.smoothscale(self._bat_image, (50, 50))

        self.screen.blit(
            self._translucent_ghost_image, self._background_starting_position
        )
        self.screen.blit(
            self._translucent_ghost_image_2,
            (
                self._background_starting_position[0]
                - self._translucent_ghost_image_2.get_width(),
                self._background_starting_position[0]
                - self._translucent_ghost_image_2.get_width(),
            ),
        )
        self.screen.blit(self._bat_image, self.bat_coordinates)

        if self._background_starting_position[0] == WINDOW_WIDTH:
            self._background_starting_position = (
                0,
                self._background_starting_position[1],
            )

        if self._background_starting_position[1] == WINDOW_HEIGHT // 2 + 20:
            self.y_change = -1
        if self._background_starting_position[1] == WINDOW_HEIGHT // 2 - 20:
            self.y_change = 1

        self._background_starting_position = (
            self._background_starting_position[0] + 1,
            self._background_starting_position[1] + self.y_change,
        )

    def update_music(self):
        selection = self.music_component.get_single_selection()

        if selection == "On":
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def update_difficulty(self):
        selection = self.difficulty_component.get_single_selection()

        self._game_service.set_difficulty(selection)
