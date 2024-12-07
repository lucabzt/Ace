"""
Shared resources for frontend and backend. Solves the problem of having e.g. two different instances of the same Queue.
"""
from queue import Queue


class SharedResources:
    def __init__(self):
        self.player_action_queue = Queue()
