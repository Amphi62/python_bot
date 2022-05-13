from entity.blindtest.Music import Music
from entity.blindtest.Queue import Queue


class QueueFactory:
    @staticmethod
    def playlist1():
        queue = Queue(is_random=False, is_boucled=True)

        file_conf = open('resources/config/config1.txt', 'r')

        for line in file_conf.readlines():
            queue.add_in_queue(Music(line))

        return queue
