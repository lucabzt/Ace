from queue import Queue


class SharedResources:
    def __init__(self):
        self.player_action_queue = Queue()