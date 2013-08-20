
def test_compile():
    try:
        import tiddlywebplugins.binarystore
        assert True
    except ImportError:
        assert False
