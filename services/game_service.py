import random
import pygame
from lib.constants import (
    DICTIONARY_FILE,
    LEADERBOARD_FILE,
    MAX_GHOST_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from services.file_service import FileService
from models.word_field import WordField
from models.life import Life
from models.score import Score

DIFFICULTY_LEN_MAP = {"Easy": 4, "Medium": 6, "Hard": 100}


class GameService:
    """Service that handles the gameplay logic"""

    def __init__(self):
        pygame.init()
        self._points = 0
        self._lives = [Life() for _ in range(5)]
        self._file_service = FileService()
        self._last_used_words = []
        self._dictionary = self._extract_dictionary_from_file(DICTIONARY_FILE)
        self.current_words = []
        self._time_elapsed_playing = 0
        self._words_written = 0
        self._difficulty = "Easy"

    def generate_random_coordinates(self):
        """Generates random coordinates to use when spawning a new word in"""
        x_coord = random.randrange(MAX_GHOST_SIZE, WINDOW_WIDTH - MAX_GHOST_SIZE)
        y_coord = random.randrange(MAX_GHOST_SIZE, WINDOW_HEIGHT - MAX_GHOST_SIZE)

        return x_coord, y_coord

    def apply_all_fitlers(self, word):
        used = word in self._last_used_words
        max_length = DIFFICULTY_LEN_MAP[self._difficulty]
        exists_with_same_letter = any(word[0] == word[0] for word in self.current_words)

        return not used and len(word) <= max_length and not exists_with_same_letter

    def apply_high_priority_filters(self, word):
        max_length = DIFFICULTY_LEN_MAP[self._difficulty]
        exists_with_same_letter = any(word[0] == word[0] for word in self.current_words)

        return len(word) <= max_length and not exists_with_same_letter

    def apply_difficulty_filter_only(self, word):
        max_length = DIFFICULTY_LEN_MAP[self._difficulty]

        return len(word) <= max_length

    def _generate_random_word(self):
        """Generates a random word from a dictionary"""
        applicable_words = list(filter(self.apply_all_fitlers, self._dictionary))

        if len(applicable_words) == 0:
            applicable_words = list(
                filter(self.apply_high_priority_filters, self._dictionary)
            )

        if len(applicable_words) == 0:
            applicable_words = list(
                filter(self.apply_difficulty_filter_only, self._dictionary)
            )

        random_index = random.randint(0, len(applicable_words) - 1)
        generated_word = applicable_words[random_index]

        if len(self._last_used_words) == 100:
            self._last_used_words.pop()

        self.current_words.append(generated_word)
        self._last_used_words.append(generated_word)
        self._words_written += 1

        return generated_word

    def _extract_score_from_line(self, line):
        name, points = line.split(",")
        return Score(name, points)

    def _extract_rect_from_box(self, box):
        x_coord, y_coord = box.get_coordinates()
        ghost_offset = 20

        return box.get_ghost().get_rect(
            center=(x_coord - ghost_offset, y_coord - ghost_offset * 2)
        )

    def _extract_dictionary_from_file(self, file):
        return list(
            map(lambda word: word[:-1].lower(), self._file_service.read_from_file(file))
        )

    def generate_random_box(self, other_boxes, depth=0, max_depth=10):
        x_coord, y_coord = self.generate_random_coordinates()
        word = self._generate_random_word()
        box = WordField(x_coord, y_coord, word)

        if depth == max_depth:
            return box

        rectangles = list(map(self._extract_rect_from_box, other_boxes))
        rectangle = self._extract_rect_from_box(box)

        collision_index = pygame.Rect.collidelist(rectangle, rectangles)
        if collision_index != -1:
            return self.generate_random_box(other_boxes, depth + 1)
        else:
            return box

    def add_points(self, box):
        self._points += len(box.get_original_text())
        self.current_words.remove(box.get_original_text())

    def get_points(self):
        seconds_playing = self._time_elapsed_playing / 1000
        if self._words_written:
            avg_word_length = self._points / self._words_written
        else:
            avg_word_length = 0

        return int(avg_word_length * seconds_playing)

    def get_lives(self):
        return sorted(self._lives, key=lambda life: life.is_used())

    def has_lives(self):
        return len([life for life in self._lives if not life.is_used()]) > 0

    def remove_life(self):
        life = next((l for l in self._lives if not l.is_used()), None)
        life.mark_as_used()

    def refill_lives(self):
        for life in self._lives:
            life.mark_as_unused()

    def save_score(self, user):
        self._file_service.append_to_file(
            LEADERBOARD_FILE, user + "," + str(self.get_points()) + "\n"
        )

    def get_leaderboard(self):
        scores = list(
            map(
                self._extract_score_from_line,
                self._file_service.read_from_file(LEADERBOARD_FILE),
            )
        )

        return sorted(scores, key=lambda score: int(score.get_points()), reverse=True)

    def set_time_elapsed_playing(self, time):
        self._time_elapsed_playing = time

    def reset(self):
        self._points = 0
        self.current_words = []
        self._time_elapsed_playing = 0
        self._words_written = 0
        self.refill_lives()

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty
