from collections import namedtuple as orig_namedtuple
from abc import ABCMeta, abstractmethod, abstractproperty
__all__ = ['namedtuple']

class namedtuple_meta(ABCMeta):
    def __new__(mcls, name, bases, dct):
        _fields = dct.pop('_fields', None)
        __slots__ = dct.pop('__slots__', ())

        if _fields is None:
            raise TypeError("Missing required attribute '_fields' for subtype of 'namedtuple'")
        if len(bases) > 1:
            raise TypeError("multiple inheritance not supported for subtype of 'namedtuple'")
        if __slots__ != ():
            raise TypeError("nonempty __slots__ not supported for subtype of 'tuple'")

        # Create old-school named tuple.  Monkeypatch before returning
        nt = orig_namedtuple(name, _fields)
        for key, value in dct.items():
            setattr(nt, key, value)
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

namedtuple = ABCMeta.__new__(namedtuple_meta, 'namedtuple', (tuple,), {})
