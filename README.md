# Enhanced namedtuple
## Draft Python Enhancement Proposal (PEP)

- This is my draft proposal to make a small modification to the `collections.namedtuple` library.
- I've never made a PEP.  I welcome all constructive feedback, negative, positve, or neutral.
- Whatever Python says, (probably rejected), this package has been tested for standalone distribution.
- Add a new interface to the `namedtuple` factory method for use as an abstract base class.
- Interface maintains backward compatibility with all previous versions of Python.

# Python's Required Sections

### Abstract:

Modify `collections.namedtuple` so it also functions as an abstract base class.  The interface would maintain backward compatibility.  This code still works:

```python
Vector = namedtuple('Vector', ('x','y','z'), verbose=True, rename=False)
```

But this PEP makes a `namedtuple` declaration look and feel like the rest of Python.  By inheriting from `namedtuple`, the code is clearer, more reliable, and gives the user more power.

```python
class Point(namedtuple):
    ''' Simple, customizable, reliable interface. '''
    _fields = ('x','y','z')
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```

Coders can add in their own custom functionality into a namedtuple, never needing to wory about low level tasks such as the `__slots__`, `__new__`, and `__getnewargs__` methods.  That boilerplate code would still be delegated to the original `collections.namedtuple` factory method.

This is accomplished by creating a special singleton metaclass `namedtuple_meta`, whose only instance is `namedtuple`.  The `__new__`, and `__call__` methods are overridden for `namedtuple_meta`.


### Implementation:

When a developer subclasses from `namedtuple`, the `__new__` method is invoked, and the new named tuple, with the user's custom modifications, is created and returned.  When creating the `namedtuple` singleton, we have to bypass the overridden `namedtuple_meta.__new__` method.  This is done by calling `ABCMeta.__new__` directly and passing in `namedtuple_meta` as its first argument.

Python should encourage the use of immutable objects, which means making their use as simple and elegant as possible.  The current choices for adding functionality to tuples are subpar.  Offering one of three choices:

##### 1\. Adding an extra subclass to the inheritence chain.
```python
class Point(namedtuple('Point',('x','y'))):
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```
This makes debugging harder.  A child has the same class name as its parent.  If we rename the parent class, for example 'BasePoint', now the __repr__ function  for the child class displays the name of the parent.  Finally, the parent `namedtuple` will never be reused, so nothing is gained adding a second class lookup in the `__mro__` chain.

##### 2\. Monkey patching
```python
Point = namedtuple('Point',('x','y'))
def __abs__(self):
    return sqrt(self.x**2+self.y**2+self.z**2)
Point.__abs__ = __abs__
```
This is ugly and hard to follow.  I've done this in code.  Learn from my mistakes.

##### 3\. Build your own
```python
class Point(tuple):
    x = property(lambda self: self[0])
    x = property(lambda self: self[1])
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x,y))
    def __abs__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
```
Now it's easy to forget things.  Notice here I left out `__slots__`, so a new dictionary is created for each instance of the tuple.  A novice developer might make my other optimization mistake by using `lambda` rather than `operator.itemgetter`.

### Motivation

I'm a fan of immutable objects and wish Python would gently nudge users in that direction.  A lot of classes in Python are for read-only purposes, so it makes sense to turn them into tuples.  Spare the risk custom property getter and setter methods.

For read-only operations to a database, a modified `namedtuple` works great as a lightweight object relational mapper.  For algorithmic calculations, storing coordinate data in a tuple is efficient, after overloading the mathematical operators, code becomes much more expressive.

### Rationale

I considered a number of different alternatives, and absract-base-classes were the most consistent.  Here are a few alternatives, and my reasons for not going in that direction.

##### Alternative 1\. Decorator pattern
```python
@namedtuple
class Point(tuple):
    _fields = ('x','y')
```
This becomes redundant.  If we're inheriing from namedtuple, shouldn't we automatically inherit from tuple too?  What if we don't include tuple as a base case?  Now the code is a little less clear to those who follow it.  Plus for object relational mapping purposes, much of the metaprogramming needs to occure BEFORE the class is created, not after.

##### Alternative 2\. Metaclass pattern
```python
class Point:
    __metaclass__ = namedtuple
    _fields = ('x','y')
```
The incompatibilities between Python2 and Python3 metaclass syntax means this implementation would neutralize all the benefits I've previously laid out.  Furthermore when talking in plain spoken language about classes created by `collections.namedtuple` we usually say it **is a** named tuple.  That wording screams out that the inheritance pattern makes the most sense.

### Backwards Compatibility
Fully backward compatible through 2.4, when `collections.namedtuple` was first introduced into the standard library.

For Python versions between 2.4 and 2.6, the the core code works exactly the same.  The one minor difference is that without `abc.ABCMeta`, there's no way to register a `namedtuple` subtype as a virtual subclass.

```python
    # Version < 2.6
    from enhaced_namedtuple import namedtuple
    Point = namedtuple('Point',('x','y')
    assert not issubclass(Point, namedtuple)
```

8) Reference Implementation
    The reference implementation must be completed before any PEP is given status "Final", but it need not be completed before the PEP is accepted. While there is merit to the approach of reaching consensus on the specification and rationale before writing code, the principle of "rough consensus and running code" is still useful when it comes to resolving many discussions of API details.
    The final implementation must include test code and documentation appropriate for either the Python language reference or the standard library reference.
