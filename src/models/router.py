from sultan.api import Sultan

from src.components import *
from src.components.node import Node


# TODO This ist just an idea, not doing anything really - implement it

class Router(Node):
    """
    Class representing a routers as abstract model.
    This class should contain an abstract parts of implemented routers.
    Note:
        Uses sultan as an example project -- py wrapper around shell -- this could be a pythonic way for further API implementation.
    """

    def __init__(self):
        self.sultan = Sultan()
