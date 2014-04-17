"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

from Map import Map
import random
import time

class SortedListMap( Map ):

    def _find_index( self, k, low, high ):
        """
         Binary search
         Return the index of the leftmost item with key >= k
             return j such that:
                 T[low:j] have key < k
                 T[j:high+1] have key >= k
        """
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._T[mid]._key:
                return mid
            elif k < self._T[mid]._key:
                return self._find_index( k, low, mid - 1 )
            else:
                return self._find_index( k, mid + 1, high )

    def __init__( self ):
        self._T = []

    def __len__( self ):
        return len( self._T )

    def __getitem__( self, k ):
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j == len( self._T ) or self._T[j]._key != k:
            return False
        return self._T[j]._value

    def __setitem__( self, k, v ):
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j < len( self._T ) and self._T[j]._key == k:
            self._T[j]._value = v
        else:
            self._T.insert( j, self._Item( k, v ) )

    def __delitem__( self, k ):
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j == len( self._T ) or self._T[j]._key != k:
            return False
        self._T.pop( j )

    def __iter__( self ):
        for item in self._T:
            yield item._key

    def __reversed__( self ):
        for item in reversed( self._T ):
            yield item._key

    def find_min( self ):
        if len( self._T ) > 0:
            return (self._T[0]._key,self._T[0]._value)
        else:
            return None

    def find_max( self ):
        if len( self._T ) > 0:
            return (self._T[-1]._key,self._T[-1]._value)
        else:
            return None

    def find_ge( self, k ):
        #return (key,value) where key >= k
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j < len( self._T ):
            return (self._T[j]._key,self._T[j]._value)
        else:
            return None

    def find_le( self, k ):
        #return (key,value) where key <= k
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j > 0:
            return (self._T[j-1]._key,self._T[j-1]._value)
        else:
            return None

    def find_gt( self, k ):
        #return (key,value) where key > k
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j < len( self._T ) and self._T[j]._key == k:
            j += 1
        if j < len( self._T ):
            return (self._T[j]._key,self._T[j]._value)
        else:
            return None

    def find_lt( self, k ):
        #return (key,value) where key < k
        j = self._find_index( k, 0, len( self._T ) - 1 )
        if j > 0:
            return (self._T[j-1]._key,self._T[j-1]._value)
        else:
            return None

    def find_range( self, start, stop ):
        #iterate (key,value) where start <= key < stop
        if start is None:
            j = 0
        else:
            j = self._find_index( start, 0, len( self._T ) - 1 )
        while j < len( self._T ) and (stop is None or self._T[j]._key < stop):
            yield (self._T[j]._key,self._T[j]._value)
            j += 1


"""unit testing
"""
if __name__ == '__main__':

    print( "UnsortedListMap unit testing..." )

    M = SortedListMap()

#     nb = 500000
#     random.seed( 131341 )
#     avant = time.time()
#     for i in range( nb ):
#         key = random.randint( 0, nb )
#         M[key] = key
#     apres = time.time()
#     print( "Insertion of", nb, "keys in ", apres-avant, "seconds." )

#     avant = time.time()
#     for i in range( nb ):
#         key = random.randint( 0, nb )
#         M.get( key )
#     apres = time.time()
#     print( "Access to", nb, "keys in ", apres-avant, "seconds." )

#     print( len( M ) ) #0
#     M['K'] = 2
#     M['B'] = 4
#     M['U'] = 2
#     M['V'] = 8
#     M['K'] = 9
#     print( M['B'] )
#     print( M['X'] )
#     print( M.get( 'F' ) )
#     print( M.get( 'F', 5 ) )
#     print( M.get( 'K', 5 ) )
#     print( len( M ) )
#     del M['V']
#     print( M.pop( 'K' ) )
#     for key in M.keys():
#         print( str( key ) )
#     for value in M.values():
#         print( str( value ) )
#     for item in M.items():
#         print( str( item ) )
#     print( M.setdefault( 'B', 1 ) )
#     print( M.setdefault( 'A', 1 ) )
#     print( M )
#     print( M.popitem() )    

    nb = 50
    random.seed( 131341 )
    avant = time.time()
    for i in range( nb ):
        key = random.randint( 0, nb )
        M[key] = key
    apres = time.time()
    print( "Insertion of", nb, "keys in ", apres-avant, "seconds." )
    print( M )

    print( M.find_ge( 25 ) )
    print( M.find_gt( 25 ) )
    print( M.find_le( 25 ) )
    print( M.find_lt( 25 ) )
    for (x,y) in M.find_range( 12, 38 ):
        print( "x =", x, ", y =", y )

    print( "End of testing." )
