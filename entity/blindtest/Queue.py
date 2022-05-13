import random


class Queue:
    def __init__(self, is_random=False, is_boucled=True):
        self.__queue = []
        self.__increment = 0
        self.__is_boucled = is_boucled
        self.__is_random = is_random

    def add_in_queue(self, musique):
        self.__queue.append(musique)

    def clear_queue(self):
        self.__increment = 0
        self.__queue = []

    def start_queue(self):
        self.__increment = 0
        if self.__is_random:
            random.shuffle(self.__queue)

    def restart_queue(self):
        self.__increment = 0
        if self.__is_random:
            random.shuffle(self.__queue)

    def next_music(self):
        if self.__is_boucled:
            self.__increment = (self.__increment + 1) % len(self.__queue)

    def previous_music(self):
        if self.__is_boucled:
            self.__increment = (self.__increment - 1 + len(self.__queue)) % len(self.__queue)

    def get_current_music(self):
        return self.__queue[self.__increment]
