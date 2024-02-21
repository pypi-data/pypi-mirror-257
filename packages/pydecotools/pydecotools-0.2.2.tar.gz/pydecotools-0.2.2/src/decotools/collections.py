from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    UserString,
    defaultdict,
    deque,
    namedtuple,
)

from .applier import smart_partial as _smart_partial

ChainMap @= _smart_partial
Counter @= _smart_partial
OrderedDict @= _smart_partial
UserDict @= _smart_partial
UserList @= _smart_partial
UserString @= _smart_partial
defaultdict @= _smart_partial
deque @= _smart_partial
namedtuple @= _smart_partial
