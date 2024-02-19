class TypeSet(type):
    def __new__( cls, *items ):
        return super().__new__( cls, 'TypeSet', (), { '_items_': () })

    def __init__( self, *items ):
        for i in listFlatten( items, tuples = True ):
            self.add(i)

    def types(self):
        return tuple( i[0] for i in self._items_ )

    def __iter__(self):
        L = [ i[1] for i in self._items_ ]
        for i in L:
            yield i

    def __check_instance(func):
        @wraps(func)
        def __wrap( self, other ):
            if not isinstance( other, type(self) ):
                raise TypeError(f"Can only compare other TypeSets")
            return func( self, other )
        return __wrap

    def __compare(func):
        @wraps(func)
        def __wrap( self, other ):
            print(f"{self = }, {other = }")
            A, B = self.__hash__(), hash(other)
            if len(A) == len(B):

            return func( A, B )
        return __wrap

    @__check_instance
    def __or__(self, other):
        items = type(self)( *list(self) )
        for item in other:
            items.add(item)

        return items

    @__check_instance
    def __and__(self, other):
        items = type(self)()
        for item in other:
            if item in self:
                items.add(item)
        return items

    @__check_instance
    @__compare
    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @__check_instance
    @__compare
    def __gt__(A, B):
        return A > B

    @__check_instance
    @__compare
    def __ge__(A, B):
        return A >= B

    def __le__(self, other):
        return not self.__gt__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __hash__(self):
        return tuple( sum([ ord(i) for i in list(T.__name__) ]) for T in sorted( self.types(), key = lambda x: x.__name__ ))

    def add( self, item ):
        import logging
        log = logging.getLogger(__name__)
        if type(item).__name__ not in self.__type_names__:
            log.error(f"Invalid type for TypeSet - '{type(item).__name__}'")
            return

        if hasattr( item, 'extended' ) and hasattr( item, '__ext__' ) and item.__ext__:
            for e in item.extended():
                self.add(e)
        elif type(item) not in self.types():
            self._items_ = self._items_ + (( type(item), item ),)
