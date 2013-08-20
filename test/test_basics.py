
import os
import shutil

from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler

from tiddlywebplugins.utils import get_store

def setup_module(module):
    try:
        shutil.rmtree('store')
        shutil.rmtree('binarystore')
    except (OSError, IOError):
        pass

    module.store = get_store(config)


def test_store_normal():
    bag = Bag('one')
    store.put(bag)
    tiddler = Tiddler('alpha', 'one')
    tiddler.text = 'normal'
    store.put(tiddler)

    tiddler = Tiddler('alpha', 'one')
    tiddler = store.get(tiddler)

    assert tiddler.title == 'alpha'
    assert tiddler.bag == 'one'
    assert tiddler.text == 'normal'

    assert os.path.exists('store/bags/one/tiddlers/alpha/1')


def test_store_binary():
    tiddler = Tiddler('beta', 'one')
    tiddler.type = 'image/png'
    tiddler.text = 'not normal'
    store.put(tiddler)

    tiddler = Tiddler('beta', 'one')
    tiddler = store.get(tiddler)

    assert tiddler.title == 'beta'
    assert tiddler.bag == 'one'
    assert tiddler.text == 'not normal'
    assert tiddler.type == 'image/png'

    assert os.path.exists('binarystore/bags/one/tiddlers/beta/1')
