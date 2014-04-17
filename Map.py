"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

import collections

class Map( collections.MutableMapping ):

    #nested _Item class
    class _Item:
        __slots__ = '_key', '_value'

        def __init__( self, k, v = None ):
            self._key = k
            self._value = v

        def __eq__( self, other ):
            return self._key == other._key

        def __ne__( self, other ):
            return not( self == other )

        def __lt__( self, other ):
            return self._key < other._key

        def __ge__( self, other ):
            return self._key >= other._key

        def __str__( self ):
            return "<" + str( self._key ) + "," + str( self._value ) + ">"

        def key( self ):
            return self._key

        def value( self ):
            return self._value

    def is_empty( self ):
        return len( self ) == 0

    def __str__( self ):
        if self.is_empty():
            return "{}"
        pp = "{"
        for item in self.items():
            pp += str( item )
        pp += "}"
        return pp

    def get( self, k, d = None ):
        if self[k]:
            return self[k]
        else:
            return d

    def setdefault( self, k, d = None ):
        if self[k]:
            return self[k]
        else:
            self[k] = d
            return d

