from collections import namedtuple as orig_namedtuple
import sys as _sys
try:
    from abc import ABCMeta
except ImportError:
    # For rare versions of Python before abstract base classes
    ABCMeta = type

__all__ = ['namedtuple']

class namedtuple_meta(ABCMeta):
    @classmethod
    def instance(mcls):
        try:
            return mcls.__instance
        except AttributeError:
            cls = ABCMeta.__new__(mcls, 'namedtuple', (tuple,), {})
            cls.__module__ = __name__
            mcls.__instance = cls
            return cls

    # If ABCMeta is not available, override
    # virtual subclass registration with a dummy
    if ABCMeta is type:
        def register(mcls, cls):
            pass

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

    def __call__(cls, name, field_names = None, verbose=False, rename=False):
        """%s""" % (orig_namedtuple.__doc__,)
        if field_names is None:
            raise TypeError(("Cannot create instances of the abstract class 'namedtuple'.\n"
            "If you want to use this method as a factory to create a namedtuple class,\n"
            "you need to include 'field_names' as an array or as a delimited string."))

        nt = orig_namedtuple(name, field_names, verbose, rename)

        # For pickling to work, the __module__ variable needs to be set to the frame
        # where the named tuple is created.  Bypass this step in enviroments where
        # sys._getframe is not defined (Jython for example) or sys._getframe is not
        # defined for arguments greater than 0 (IronPython).
        try:
            nt.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
        except (AttributeError, ValueError):
            pass

        namedtuple.register(nt)
        return nt

namedtuple = namedtuple_meta.instance()
