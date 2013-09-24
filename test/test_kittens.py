"""
Put some kittens in that store and see what happens.
"""

import shutil
import os
import simplejson

from wsgi_intercept import httplib2_intercept
import wsgi_intercept
import httplib2

from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe

from tiddlywebplugins.utils import get_store

KITTEN_DIR = 'kittens'


def setup_module(module):
    try:
        shutil.rmtree('store')
        shutil.rmtree('binarystore')
    except:
        pass

    from tiddlyweb.web import serve
    def app_fn():
        return serve.load_app()
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)
    module.store = get_store(config)
    module.http = httplib2.Http()

    bag = store.put(Bag('kittens'))


def test_put_kittens():
    kittenfiles = os.listdir(KITTEN_DIR)

    locations = []
    for kitten in kittenfiles:
        kitten_path = os.path.join(KITTEN_DIR, kitten)
        with open(kitten_path) as data_file:
            data = data_file.read()
            location = 'http://0.0.0.0:8080/bags/kittens/tiddlers/%s' % kitten
            response, content = http.request(location,
                    method='PUT',
                    headers={'Content-Type': 'image/jpeg'},
                    body=data)
            assert response['status'] == '204'
            assert response['location'] == location
            locations.append(location)

    for location in locations:
        response, content = http.request(location)
        assert response['status'] == '200'
        assert response['content-type'] == 'image/jpeg'


def test_get_kitten_list():
    response, content = http.request(
            'http://0.0.0.0:8080/bags/kittens/tiddlers.json?sort=title')

    assert response['status'] == '200'
    info = simplejson.loads(content)

    assert len(info) == 9

    assert info[0]['title'] == '100.1.jpg'
    assert 'text' not in info[0]

    response, content = http.request(
            'http://0.0.0.0:8080/bags/kittens/tiddlers/100.1.jpg',
            headers={'Accept': 'application/json'})

    assert response['status'] == '200'
    assert response['content-type'] == 'application/json'
    info = simplejson.loads(content)

    assert info['title'] == '100.1.jpg'
    assert 'text' in info
