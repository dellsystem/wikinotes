class Struct:
    """Used for testing, so that arbitrary attributes for an object created
    on-the-fly can be accessed using dot notation. See wiki/tests/views.py for
    more details."""
    def __init__(self, entries):
        self.__dict__.update(entries)
