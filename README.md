1) Preamble
    RFC 822 style headers containing meta-data about the PEP,
    including the PEP number,
    a short descriptive title (limited to a maximum of 44 characters),
    the names, and optionally the contact info for each author, etc.

2) Abstract:

Allow collections.namedtuple to function as an abstract base class,
allowing named tuple classes to be declared using more Pythonic code:

    class Point(namedtuple):
        ''' Simple, customizable, reliable interface. '''
        _fields = ('x','y','z')
        def __abs__(self):
            return sqrt(self.x**2+self.y**2+self.z**2)

Users could add in their own custom functionality into named tuples,
and let the Python builtin libraries take care of the low level
housekeeping such as __slots__, __new__, and __getnewargs__.

Python should encourage the use of immutable objects, which means making
their use as simple and elegant as possible.

The current methods for adding functionality to tuples are subpar.
    class Point(namedtuple('Point',('x','y'))):
        ''' Unneeded base class with same name, making debugging hard.
            Easy to forget to set __slots__ = () in the subclass.  '''
        def __abs__(self):
            return sqrt(self.x**2+self.y**2+self.z**2)

    Point = namedtuple('Point',('x','y'))
    def __abs__(self):
        ''' Monkey patching looks even uglier. '''
        return sqrt(self.x**2+self.y**2+self.z**2)
    Point.__abs__ = __abs__

The interface would maintain backward compatibility.
    ''' This still works. '''
    Vector = namedtuple('Vector', ('x','y','z'), verbose=True, rename=False)

3) Copyright/public domain
    Public Domain License

4) Specification
    Requires the abc module, so Python 2.6 or higher.

5) Motivation
    The namedtuple method is quick and easy on memory, but it's limiting.
    When users want to add their own functionality to this tuple subclass,
    the code is no longer Pythonic.  Users end up doing one of three things:

      a) Creating their own tuple subclasses, often forgetting things such as __slots__ and __getnewargs__.
      b) Making weird intermediate subclasses, often there a child class has the same name as the parent class, making for weird debugging.
      c) Monkey patching manually, which makes for ugly code

    My two use cases are vector calculations and read-only object-relational-maps.
    Many fields can be calculated on the fly, without the need for extra memory.
    Also tuples provide the peace of mind that you know it didn't get corrupted.

6) Rationale
    The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made.
    It should describe alternate designs that were considered and related work, e.g. how the feature is supported in other languages.
    The rationale should provide evidence of consensus within the community and discuss important objections or concerns raised during discussion.

7) Backwards Compatibility
    Fully backward compatible.  namedtuple can still be called the old fashioned way through my implementation.

8) Reference Implementation
    The reference implementation must be completed before any PEP is given status "Final", but it need not be completed before the PEP is accepted. While there is merit to the approach of reaching consensus on the specification and rationale before writing code, the principle of "rough consensus and running code" is still useful when it comes to resolving many discussions of API details.
    The final implementation must include test code and documentation appropriate for either the Python language reference or the standard library reference.
