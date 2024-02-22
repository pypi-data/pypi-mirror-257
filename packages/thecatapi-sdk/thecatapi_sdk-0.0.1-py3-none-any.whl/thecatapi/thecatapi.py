from .images import Images
from .votes import Votes
from .breeds import Breeds
from .facts import Facts
from .favourites import Favourites


class TheCatAPI:

    def __init__(self, api_key):
        self.images = Images(api_key=api_key)
        self.votes = Votes(api_key=api_key)
        self.breeds = Breeds(api_key=api_key)
        self.facts = Facts(api_key=api_key)
        self.favourites = Favourites(api_key=api_key)
