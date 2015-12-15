from abc import ABCMeta
import collections as _collections
_namedtuple = _collections.namedtuple
__all__ = ['namedtuple']

class namedtuple_surrogate(ABCMeta):
    ''' Singleton class.  Its only instance, called 'namedtupole' can be both
        subclassed and invoked in order to create tuple subclasses.
    '''

    @classmethod
    def _wraps(mcls):
        ''' Bypass the overridden __new__ method.
            The overridden __new__ method is only invoked
            once Python tries to create a subclass of 'namedtuple'

            We include (tuple,) as a base so the
            transitive property still holds true.
            if issubclass(a, b) and issubclass(b, c):
                assert issubclass(a, c)
        '''
        return ABCMeta.__new__(mcls, 'namedtuple', (tuple,), {})

    def __new__(mcls, name, bases, dct):
        ''' Once the surrogate that is returned from "_wraps"
            gets subclassed we run this function.  This is like
            a class decorator, but one which operates BEFORE
            the class is created rather than after.
        '''

        _fields = dct.pop('_fields', None)
        __slots__ = dct.pop('__slots__', ())

        if _fields is None:
            raise TypeError("Missing required attribute '_fields'.")
        elif len(bases) > 1:
            raise TypeError("Subclasses of namedtuple do not support multiple inheritance.")
        elif __slots__ != ():
            raise TypeError("Subclasses of namedtuple cannot have non_empty slots.")

        nt = _namedtuple(name, _fields)
        for key in dct:
            setattr(nt, key, dct[key])
        namedtuple.register(nt)
        return nt

    def __call__(self, name, field_names, verbose=False, rename=False):
        nt = _namedtuple(name, field_names, verbose, rename)
        namedtuple.register(nt)
        return nt

namedtuple = namedtuple_surrogate._wraps()
