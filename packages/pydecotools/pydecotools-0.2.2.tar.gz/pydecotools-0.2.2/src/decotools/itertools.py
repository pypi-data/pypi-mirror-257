from contextlib import suppress as _suppress
from itertools import (
    count,
    cycle,
    repeat,
    accumulate,
    chain,
    compress,
    dropwhile,
    filterfalse,
    groupby,
    islice as _islice,
    starmap,
    takewhile,
    tee,
    zip_longest,
    product,
    permutations,
    combinations,
    combinations_with_replacement,
    pairwise,
    batched,
)

from .applier import smart_partial as _smart_partial


@_smart_partial
def islice(*args):
    @_smart_partial
    def wrapper(iterable):
        return _islice(iterable, *args)
    return wrapper


count @= _smart_partial
cycle @= _smart_partial
repeat @= _smart_partial
accumulate @= _smart_partial
chain @= _smart_partial
compress @= _smart_partial
dropwhile @= _smart_partial
filterfalse @= _smart_partial
groupby @= _smart_partial
starmap @= _smart_partial
takewhile @= _smart_partial
tee @= _smart_partial
zip_longest @= _smart_partial
product @= _smart_partial
permutations @= _smart_partial
combinations @= _smart_partial
combinations_with_replacement @= _smart_partial
pairwise @= _smart_partial
batched @= _smart_partial
