# Enhanced namedtuple
## Draft Python Enhancement Proposal (PEP)

- This is my draft proposal to make a small modification to the collections.namedtuple library.
- I've never made a PEP.  I welcome all constructive feedback, negative, positve, or neutral.
- Whatever Python says, (probably no), this package has been tested for standalone distribution.
- Add a new interface to the namedtuple factory method for use as an abstract base class.
- Interface maintains backward compatibility with all previous versions of Python.

# Python's Required Sections

### Abstract:

Modify "collections.namedtuple" so it also functions as an abstract base class.  This would allow named tuple classes to be declared using more Pythonic code.

```python
class Point(namedtuple):
    ''' Simple, customizable, reliable interface. '''
    _fields = ('x','y','z')
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```

Users could add in their own custom functionality into a namedtuple, never needing to wory about low level tasks such as the \_\_slots\_\_, \_\_new\_\_, and \_\_getnewargs\_\_ methods.  That boilerplate code would still be delegated to the original collections.namedtuple factory method.  **Python should encourage the use of immutable objects, which means making their use as simple and elegant as possible.**

### The current choices for adding functionality to tuples are subpar.

```python
class Point(namedtuple('Point',('x','y'))):
    ''' Unneeded base class in the method resolution order.
        Base class has came name as child, making debugging hard,
        Easy to forget to set __slots__ = () in the subclass.  '''
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)

class Point(namedtuple('BasePoint',('x','y'))):
    ''' No name conflict, but now the '__repr__' function displays the wrong class name. '''
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)

Point = namedtuple('Point',('x','y'))
def __abs__(self):
    ''' Monkey patching looks even uglier. '''
    return sqrt(self.x**2+self.y**2+self.z**2)
Point.__abs__ = __abs__

class Point(tuple):
    ''' Building your own, is one choice.  But this is a lot of code.
        Introduces a lot of room for bugs.
    '''
    x = property(itemgetter(0))
    y = property(itemgetter(1))

    def __new__(cls, x, y):
        return tuple.__new__(cls, (x,y))
        
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```

The interface would maintain backward compatibility.

```python
''' This still works. '''
Vector = namedtuple('Vector', ('x','y','z'), verbose=True, rename=False)
```
