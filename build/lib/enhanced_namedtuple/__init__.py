from abc import ABCMeta
import collections as _collections
_namedtuple = _collections.namedtuple
___all__ = ['namedtuple']

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
            msg = "Missing required attribute '_fields'"
            raise TypeError(msg)
        
        if len(bases) > 1:
            msg = "Subclasses of namedtuple do not support multiple inheritance."
            raise TypeError(msg)
        
        if __slots__ != ():
            msg = "Subclasses of namedtuple cannot have non_empty slots."
            raise TypeError(msg)

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

def __tests():
    ''' Informal unit tests '''
    # Because when we subclass 'namedtuple' we return a subclass of tuple
    # We want to make sure that 'namedtuple' itself evaluates as a sublcass of tuple.
    assert isinstance(namedtuple, ABCMeta)
    assert not issubclass(namedtuple, type)
    assert namedtuple.__name__ == 'namedtuple'

    assert issubclass(namedtuple, tuple)
    assert not isinstance(namedtuple, tuple)

    # Check the new implementation and the backward compatible one.
    class Vector(namedtuple):
        _fields = ('x', 'y')
        def __abs__(self):
            return (self.x **2 + self.y **2) ** 0.5
    Point = namedtuple('Point',('x','y'))

    # Ensure no exraneous parent classes in the mro
    assert Point.__mro__ == (Point, tuple, object)
    assert Vector.__mro__ == (Vector, tuple, object)

    # But subclasses should still show up as named tuples.
    assert issubclass(Point, namedtuple)
    assert issubclass(Vector, namedtuple)

    # 'verbose' and 'rename' should be treated like normal attributes
    # Only raise errors when the field names are inconsistent.
    class TryVerboseTrue(namedtuple):
        _fields = ('a','b','c')
        verbose = True
    assert TryVerboseTrue.verbose == True
    
    class TryVerboseFalse(namedtuple):
        _fields = ('a','b','c')
        verbose = False
    assert TryVerboseFalse.verbose == False

    class TryRenameTrue(namedtuple):
        _fields = ('a','b','c')
        rename = True
    assert TryRenameTrue.rename == True
    
    class TryRenameFalse(namedtuple):
        _fields = ('a','b','c')
        rename = False
    assert TryRenameFalse.rename == False    
    
    try:
        class Vector1(namedtuple):
            _fields = ('name', 'class','age','gender')
            rename = True
    except ValueError:
        pass
    else:
        raise AssertionError("Should not have allowed raname = True when inheriting")
        
    verbose = False
    WithRenameA = namedtuple('WithRenameA', ('x','class','y'), verbose, True)
    assert WithRenameA._fields == ('x', '_1', 'y')
    
    WithRenameB = namedtuple('WithRenameB', ('x','y','x'), verbose, True)
    assert WithRenameB._fields == ('x','y','_2')
    
    try:
        namedtuple('WithoutRenameA', ('x','class','y'), verbose, False)
    except ValueError:
        pass
    else:
        raise AssertionError("Should not have accepted the field 'class'.")

    try:
        namedtuple('WithoutRenameB', ('x','y','x'), verbose, False)
    except ValueError:
        pass
    else:
        raise AssertionError("Should not have accepted the field 'class'.")

    try:
        class Vector2(namedtuple):
            _fields = ('name', 'age','gender','age')
            verbose = True
    except ValueError:
        pass
    else:
        raise AssertionError("Should not have allowed verbose = True when inheriting")

    class Position(namedtuple):
        _fields = ('x','y','z')
        @property
        def z(self):
            return str(self[2])
    s = Position(3,4,5)
    assert s.z == '5'

    p = Point(3,4)
    assert p.x == 3
    assert p.y == 4
    assert repr(p) == 'Point(x=3, y=4)'
    try:
        abs(p)
    except TypeError:
        pass
    else:
        raise AssertionError("Abs val should not exist for instance of Point")

    try:
        p.a = 1
    except AttributeError:
        pass
    else:
        raise AssertionError("Should not allow attributes to be set on instances of namedtuple")

    v = Vector(3,4)
    assert v.x == 3
    assert v.y == 4
    assert abs(v) == 5.0

    try:
        v.a = 1
    except AttributeError:
        pass
    else:
        raise AssertionError("Should not allow attributes to be set on instances of namedtuple")
    
    assert isinstance(p, namedtuple)
    assert isinstance(v, namedtuple)

    try:
        class Blah(namedtuple, object):
            _fields = ('x','y')
    except TypeError:
        pass
    else:
        raise AssertionError("Multiple inheritance of namedtuple failed to raise an exception.")

    try:
        class Blah2(namedtuple):
            pass
    except TypeError:
        pass
    else:
        raise AssertionError("namedtuple should not permit missing _fields property.")

    # But empty fields, although stupid, should be permitted
    class Empty(namedtuple):
        _fields = ()
    assert Empty() == ()

    try:
        class Blah3(namedtuple, object):
            __slots__ = ('abs',)
            _fields = ('x','y')
    except TypeError:
        pass
    else:
        raise AssertionError("Should not have been able to instantiate nonempty slots.")   
        
if __name__ == '__main__':
    __tests()