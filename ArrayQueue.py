"""Programme pour le cours IFT2015
   Écrit par François Major le 16 février 2014.
"""

class ArrayQueue:

    #implements the ADT Queue (Queue.py)
    #uses the python default List

    DEFAULT_CAPACITY = 1

    def __init__( self, capacity = DEFAULT_CAPACITY ):
        self._data = [None] * capacity
        self._capacity = capacity
        self._size = 0
        self._front = 0

    def __str__( self ):
        pp = str( self._data )
        pp += "(size = " + str( len( self ) )
        pp += ")[first = " + str( self._front )
        pp += "; capacity = " + str( self._capacity ) + "]"
        return pp

    def __len__( self ):
        return self._size

    def is_empty( self ):
        return self._size == 0

    def first( self ):
        if self.is_empty():
            return False
        else:
            return self._data[self._front]

    def dequeue( self ):
        if self.is_empty():
            return False
        else:
            elem = self._data[self._front]
            self._data[self._front] = None
            self._front = ( self._front + 1 ) % len( self._data )
            self._size -= 1
            return elem

    def enqueue( self, elem ):
        if self._size == len( self._data ):
            self._resize( 2 * len( self._data ) )
        avail = ( self._front + self._size ) % len( self._data )
        self._data[avail] = elem
        self._size += 1

    def _resize( self, newcapacity ):
        old = self._data
        self._data = [None] * newcapacity
        walk = self._front
        for k in range( self._size ):
            self._data[k] = old[walk]
            walk = ( 1 + walk ) % len( old )
        self._front = 0
        self._capacity = newcapacity

"""unit testing
"""
if __name__ == '__main__':

    data = ArrayQueue()
    print( data )

    data.enqueue( 5 )
    print( "enqueue 5" )
    print( data )

    data.enqueue( 3 )
    print( "push 3" )
    print( data )

    print( "len = ", str( len( data ) ) )
    print( "is_empty = ", data.is_empty() )
    print( data )

    print( "dequeue = ", data.dequeue() )
    print( data )
    print( "is_empty = ", data.is_empty() )

    print( "dequeue = ", data.dequeue() )
    print( data )
    print( "is_empty = ", data.is_empty() )

    print( "dequeue = ", data.dequeue() )

    data.enqueue( 7 )
    print( "enqueue 7" )
    print( data )
    data.enqueue( 9 )
    print( "enqueue 9" )
    print( data )

    print( "first = ", data.first() )
    data.enqueue( 4 )
    print( "enqueue 4" )
    print( data )

    print( "len = ", str( len( data ) ) )
    print( "dequeue = ", data.dequeue() )
    print( data )

    data.enqueue( 13 )
    print( "enqueue 13" )
    print( data )

    data.enqueue( 15 )
    print( "enqueue 15" )
    print( data )

    data.enqueue( 21 )
    print( "enqueue 21" )
    print( data )
