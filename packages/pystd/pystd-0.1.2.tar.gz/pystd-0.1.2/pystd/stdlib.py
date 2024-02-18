"""
STDLib implementation file based on utilities and re-implemented data structures.
"""
import builtins, random
from typing import overload, TypeVar, Callable, Iterator
from functools import partial
from .errors import BadConnector

T = TypeVar('T')

class ListEvent:
    """ListEvent class to handle events of list."""
    APPEND = "__pystd_append__"
    MAP = "map"
    FILTER = "filter"
    SHUFFLE = "shuffle"
    SHUFFLED = "shuffled"
    def __init__(self, event: str) -> None:
        self.event = event
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"
    
class ListConnector:
    """ListConnector class to trigger callback function when event performed."""
    DEFAULT_CONNECTOR = lambda *args, caller=None, **kwargs: print(f"new event at {caller} object.")
    def __init__(self, connector: Callable = DEFAULT_CONNECTOR) -> None:
        self.connector = connector
    
    def __call__(self, *args, **kwargs) -> T:
        return self.connector(*args, **kwargs)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"

class std:
    """
    https://github.com/fswair/PythonSTD
    """
    class map(builtins.map):
        def to_list(self) -> "std.list[T]":
            """
            Return a new list containing the results of applying the given function to each item of the list.
            """
            return std.list(iter(self))
        def to_iterator(self) -> Iterator[T]:
            """
            Return a new iterator containing the results of applying the given function to each item of the list.
            """
            return iter(self)
        def to_generator(self) -> Iterator[T]:
            """
            Return a new generator containing the results of applying the given function to each item of the list.
            """
            yield from self.to_iterator()
        def __repr__(self) -> str:
                address = hex(id(self))
                return f"<{self.__class__.__name__} object at {address}>"
    
    class filter(builtins.filter):
        """
        filter(function or None, iterable) --> filter object
        
        Return an iterator yielding those items of iterable for which function(item) is true. If function is None, return the items that are true.
        """
        def to_list(self) -> "std.list[T]":
            """
            Return a new list containing the results of applying the given function to each item of the list.
            """
            return std.list(iter(self))
        def to_iterator(self) -> Iterator[T]:
            """
            Return a new iterator containing the results of applying the given function to each item of the list.
            """
            return iter(self)
        def to_generator(self) -> Iterator[T]:
            """
            Return a new generator containing the results of applying the given function to each item of the list.
            """
            yield from self.to_iterator()
        def __repr__(self) -> str:
                address = hex(id(self))
                return f"<{self.__class__.__name__} object at {address}>"
   
    class list(builtins.list):
        """
        Regenerated implementation of builtins.list with additional methods.

        This class is a subclass of builtins.list and has the same methods and attributes as builtins.list.

        Additional methods:
        - shuffle: None
        - shuffled: List[T]
        - any: bool
        - all: bool
        - map: map[T]
        - filter: List[T]

        Additional attributes:
        - __doc__: str
        """
        handlers = {
            ListEvent.MAP:      [],
            ListEvent.APPEND:   [],
            ListEvent.FILTER:   [],
            ListEvent.SHUFFLE:  [],
            ListEvent.SHUFFLED: []
        }

        events: ListEvent = ListEvent
        def caller(self, func: Callable, *args, **kwargs) -> T:
            for handler in self.handlers[func.__name__]:
                try:
                    handler(*args, **kwargs, caller=hex(id(self)))
                except Exception as e:
                    raise BadConnector(f"Handler stopt by exception. Exception message: {str(e)!r}")
            return func(*args, **kwargs) if kwargs else func(*args)
        def __pystd_append__(self, __object: T) -> None:
            copy_fn = partial(builtins.list.append)
            copy_fn.__name__ = ListEvent.APPEND
            self.caller(copy_fn, self, __object)
        def shuffle(self) -> None:
            """
            Shuffle the list in place and make entire list as shuffled.
            """
            self.caller(random.shuffle, self)
        def to_shuffled(self) -> "std.list":
            """
            Shuffle and return the list but don't change original object.
            """
            copy_it = self.copy()
            self.caller(random.shuffle, copy_it)
            return copy_it
        def any(self) -> bool:
            """
            Return True if at least one element is True.
            """
            return self.caller(any, iter(self))
        def all(self) -> bool:
            """
            Return True if all elements are True.
            """
            return self.caller(all, iter(self))
        def filter(self, function: Callable[[T], bool]) -> "std.filter[T]":
            """
            Return a new filter sequence containing the results of performed predicate function to each item of the iterable.
            """
            return self.caller(std.filter, function, iter(self))
        @overload  
        def map(self, function: Callable[[T], T]) -> "std.map[T]":
            pass
        def map(self, *args, **kwargs) -> "std.map":
            """
            Return a new list containing the results of applying the given function to each item of the list.
            """
            for handler in self.handlers[ListEvent.MAP]:
                try:
                    handler(*args, **kwargs, caller=hex(id(self)))
                except Exception as e:
                    raise BadConnector(f"Connector was invalid. Error message: {e!r}")

            return self.caller(std.map, *args, self, **kwargs)

        def connect(self, event: ListEvent, handler: ListConnector = ListConnector()) -> "std.list":
            """
            Connect the existing event to the specified handler.
            """
            return self.handlers[event].append(handler)