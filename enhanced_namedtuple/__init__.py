import sys, os
base, _ = os.path.split(__file__)
if base not in sys.path:
    sys.path.insert(0, base)

from main import namedtuple
