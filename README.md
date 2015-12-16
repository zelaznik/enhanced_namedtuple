# Enhanced namedtuple
## Draft Python Enhancement Proposal (PEP)

- This is my draft proposal to make a small modification to the `collections.namedtuple` library.
- I've never made a PEP.  I welcome all constructive feedback, negative, positve, or neutral.
- Whatever Python says, (probably no), this package has been tested for standalone distribution.
- Add a new interface to the `namedtuple` factory method for use as an abstract base class.
- Interface maintains backward compatibility with all previous versions of Python.

# Python's Required Sections

### Abstract:

Modify `collections.namedtuple` so it also functions as an abstract base class.  This would allow named `tuple` classes to be declared using more Pythonic code.  The interface would maintain backward compatibility.  This code still works:

```python
Vector = namedtuple('Vector', ('x','y','z'), verbose=True, rename=False)
```

But this PEP makes a `namedtuple` declaration look and feel like the rest of Python.
```python
class Point(namedtuple):
    ''' Simple, customizable, reliable interface. '''
    _fields = ('x','y','z')
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```

Coders can add in their own custom functionality into a namedtuple, never needing to wory about low level tasks such as the `__slots__`, `__new__`, and `__getnewargs__` methods.  That boilerplate code would still be delegated to the original `collections.namedtuple` factory method.

Python should encourage the use of immutable objects, which means making their use as simple and elegant as possible.  The current choices for adding functionality to tuples are subpar.  Offering one of three choices:

##### 1\. Adding an extra subclass to the inheritence chain.
```python
class Point(namedtuple('Point',('x','y'))):
    ''' This makes debugging harder.  A child has the same class name as its parent.
        If we rename the parent class, for example 'BasePoint', now the __repr__ function
        for the child class displays the name of the parent.  Finally, there's no need to
        add a second lookup in the `__mro__` chain. '''
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```

##### 2\. Monkey patching
```python
Point = namedtuple('Point',('x','y'))
def __abs__(self):
    ''' Monkey patching looks even uglier. '''
    return sqrt(self.x**2+self.y**2+self.z**2)
Point.__abs__ = __abs__
```

##### 3\. Build your own
```python
class Point(tuple):
    ''' Lots of boilerplate code, even more room for bugs. '''
    x, y, z = (property(itemgetter(_) for _ in range(3)))
    y = property(itemgetter(1))
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x,y))
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```
