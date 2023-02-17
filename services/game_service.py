import random
from lib.constants import DICTIONARY_FILE, INITIAL_GHOST_SIZE, LEADERBOARD_FILE, WINDOW_HEIGHT, WINDOW_WIDTH
from services.file_service import FileService
from models.word_field import WordField
from models.life import Life
from models.score import Score
import pygame


class GameService():
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

    def _generate_random_coordinates(self):
        """Generates random coordinates to use when spawning a new word in"""
        x = random.randrange(INITIAL_GHOST_SIZE[0], WINDOW_WIDTH - INITIAL_GHOST_SIZE[0])
        y = random.randrange(INITIAL_GHOST_SIZE[1], WINDOW_HEIGHT - INITIAL_GHOST_SIZE[1])

        return x, y

    def _generate_random_word(self, depth, max_depth):
        """Generates a random word from a dictionary"""
        unused_words = list(filter(lambda word: word not in self._last_used_words, self._dictionary))
        random_index = random.randint(0, len(unused_words) - 1)
        generated_word = unused_words[random_index]
        
        if any(word[0] == generated_word[0] for word in self.current_words) and depth < max_depth:
            return self._generate_random_word(depth + 1, max_depth)

        if len(self._last_used_words) == 100:
            self._last_used_words.pop()
            
        self.current_words.append(generated_word)
        self._last_used_words.append(generated_word)
        self._words_written += 1
        return generated_word    

    def _extract_score_from_line(self, line):
        name, points = line.split(',')
        return Score(name, points)
    
    def _extract_rect_from_box(self, box):
        x, y = box.get_coordinates()
        ghost_offset = 20
        return box.get_ghost().get_rect(center=(x - ghost_offset, y - ghost_offset * 2))
    
    def _extract_dictionary_from_file(self, file):
        return list(map(lambda word: word[:-1].lower(), self._file_service.read_from_file(file)))

    def generate_random_box(self, other_boxes):
        x, y = self._generate_random_coordinates()
        word = self._generate_random_word(0, 10)
        box = WordField(x, y, word)

        rectangles = list(map(self._extract_rect_from_box, other_boxes))
        rectangle = self._extract_rect_from_box(box)

        collision_index = pygame.Rect.collidelist(rectangle, rectangles)
        if collision_index != -1:
            return self.generate_random_box(other_boxes)
        else:
            return box
    
    def add_points(self, box):
        self._points += len(box.get_original_text())
        self.current_words.remove(box.get_original_text())

    def get_points(self):
        seconds_playing = self._time_elapsed_playing / 1000
        avg_word_length = self._points / self._words_written

        return int(avg_word_length * seconds_playing)

    def get_lives(self):
        return sorted(self._lives, key=lambda life: life.is_used())
    
    def has_lives(self):
        return len([life for life in self._lives if life.is_used() == False]) > 0

    def remove_life(self):
        life = next((l for l in self._lives if l.is_used() == False), None)
        life.mark_as_used()
   
    def refill_lives(self):
        for life in self._lives:
            life.mark_as_unused()
    
    def save_score(self, user):
        self._file_service.append_to_file(
            LEADERBOARD_FILE,
            user + ',' + self.get_points().__str__() + '\n'
            )
        
    def get_leaderboard(self):
        scores = list(map(
            self._extract_score_from_line,
            self._file_service.read_from_file(LEADERBOARD_FILE)
            ))
        
        return sorted(scores, key=lambda score: int(score.get_points()), reverse=True)

    def set_time_elapsed_playing(self, time):
        self._time_elapsed_playing = time

    def reset(self):
        self._points = 0
        self.current_words = []
        self._time_elapsed_playing = 0
        self._words_written = 0
        self.refill_lives()