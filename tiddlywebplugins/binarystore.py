"""
A store that handles binary tiddlers in a special way.
"""

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store as StoreBoss, NoBagError
from tiddlyweb.stores import StorageInterface
from tiddlyweb.util import binary_tiddler


class BinaryTiddler(Tiddler):
    """
    Establish text as a property so that we can lazily load
    the tiddler's text from the binary store.
    """

    @property
    def text(self):
        if self._text is None:
            found_tiddler = self.store.storage.binary_store.tiddler_get(
                    Tiddler(self.title, self.bag))
            self._text = found_tiddler.text
        return self._text


class Store(StorageInterface):

    def __init__(self, store_config=None, environ=None):
        super(Store, self).__init__(store_config, environ)
        self.config = environ.get('tiddlyweb.config')
        self.binary_store = StoreBoss('text', {'store_root': 'binarystore'},
                environ=environ).storage
        self.core_store = StoreBoss(self.config['binarystore.child'][0],
                self.config['binarystore.child'][1], environ=environ).storage

    def bag_put(self, bag):
        self.core_store.bag_put(bag)

    def bag_get(self, bag):
        return self.core_store.bag_get(bag)

    def bag_delete(self, bag):
        return self.core_store.bag_delete(bag)

    def recipe_put(self, recipe):
        self.core_store.recipe_put(recipe)

    def recipe_get(self, recipe):
        return self.core_store.recipe_get(recipe)

    def recipe_delete(self, recipe):
        return self.core_store.recipe_delete(recipe)

    def user_put(self, user):
        self.core_store.user_put(user)

    def user_get(self, user):
        return self.core_store.user_get(user)

    def user_delete(self, user):
        return self.core_store.user_delete(user)

    def tiddler_delete(self, tiddler):
        self.core_store.tiddler_delete(tiddler)
        if binary_tiddler(tiddler):
            self.binary_store.tiddler_delete(tiddler)

    def tiddler_put(self, tiddler):
        if binary_tiddler(tiddler):
            try:
                self.binary_store.tiddler_put(tiddler)
            except NoBagError:
                self.binary_store.bag_put(Bag(tiddler.bag))
                self.binary_store.tiddler_put(tiddler)
            tiddler.text = ''
        self.core_store.tiddler_put(tiddler)

    def tiddler_get(self, tiddler):
        found_tiddler = self.core_store.tiddler_get(tiddler)
        if binary_tiddler(found_tiddler):
            found_tiddler.__class__ = BinaryTiddler
            found_tiddler._text = None
        return found_tiddler

    def list_recipes(self):
        return self.core_store.list_recipes()

    def list_bags(self):
        return self.core_store.list_bags()

    def list_users(self):
        return self.core_store.list_users()

    def list_bag_tiddlers(self, bag):
        return self.core_store.list_bag_tiddlers(bag)

    def list_tiddler_revisions(self, tiddler):
        return self.core_store.list_tiddler_revisions(tiddler)

    def search(self, search_query):
        return self.core_store.search(search_query)
