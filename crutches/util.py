def next_uid():
    next_uid.uid += 1
    return next_uid.uid
next_uid.uid = 0


def combine_files(files, directory):
    combined = ""
    for f in files:
        with open(join(directory, f), 'r') as f:
            combined += f.read()
    return combined


def flatten(l):
    """
    Courtesy of: http://stackoverflow.com/a/2158532/453290
    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

class Bunch:
    """
    http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
