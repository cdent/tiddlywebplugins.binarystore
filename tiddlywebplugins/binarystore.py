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
