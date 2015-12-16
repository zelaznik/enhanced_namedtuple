from collections import namedtuple as orig_namedtuple
from abc import ABCMeta, abstractmethod, abstractproperty
__all__ = ['namedtuple']

class namedtuple_surrogate(ABCMeta):
    """ Singleton class.  Its only instance, called 'namedtupole' can be both
        subclassed and invoked in order to create tuple subclasses.
    """

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
            raise TypeError("Missing required attribute '_fields'")
        if len(bases) > 1:
            raise TypeError("multiple inheritance not supported for subtype of 'namedtuple'")
        if __slots__ != ():
            raise TypeError("nonempty __slots__ not supported for subtype of 'tuple'")

        nt = orig_namedtuple(name, _fields)
        for key in dct:
            setattr(nt, key, dct[key])
        namedtuple.register(nt)
        return nt

    def __call__(self, name, field_names = None, verbose=False, rename=False):
        if field_names is None:
            raise TypeError(("Cannot create instances of the abstract class namedtuple.\n"
            "If you are using this method as a factory to create a namedtuple class,\n"
            "you ned to include 'field_names' as an array or as a delimited string."))

        nt = orig_namedtuple(name, field_names, verbose, rename)
        namedtuple.register(nt)
        return nt

namedtuple = namedtuple_surrogate._wraps()