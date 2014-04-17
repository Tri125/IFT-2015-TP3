"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 28 mars 2014.
   Ref: Data Structure & Algorithms in Python
        Goodrich, Tamassia et Goldwasser, 2013
"""

import random
import time
from LinkedBinaryTree import LinkedBinaryTree
from Map import Map

class TreeMap( LinkedBinaryTree, Map ):

    #overriding Position
    class Position( LinkedBinaryTree.Position ):

        def key( self ):
            return self.element()._key
    
        def value( self ):
            return self.element()._value

    #--- non public ---
    def _subtree_search( self, p, k ):
        if k == p.key():
            return p
        elif k < p.key():
            if self.left( p ) is not None:
                return self._subtree_search( self.left( p ), k )
        else:
            if self.right( p ) is not None:
                return self._subtree_search( self.right( p ), k )
        return p

    def _subtree_first_position( self, p ):
        walk = p
        while self.left( walk ) is not None:
            walk = self.left( walk )
        return walk

    def _subtree_last_position( self, p ):
        walk = p
        while self.right( walk ) is not None:
            walk = self.right( walk )
        return walk

    def _first( self ):
        return self._subtree_first_position( self.root() ) if len( self ) > 0 else None

    def _last( self ):
        return self._subtree_last_position( self.root() ) if len( self ) > 0 else None

    def _before( self, p ):
        self._validate( p )
        if self.left( p ):
            return self._subtree_last_position( self.left( p ) )
        else:
            walk = p
            above = self.parent( walk )
            while above is not None and walk == self.left( above ):
                walk = above
                above = self.parent( walk )
            return above

    def _after( self, p ):
        self._validate( p )
        if self.right( p ):
            return self._subtree_first_position( self.right( p ) )
        else:
            walk = p
            above = self.parent( walk )
            while above is not None and walk == self.right( above ):
                walk = above
                above = self.parent( walk )
            return above

    def _find_position( self, k ):
        if self.is_empty():
            return None
        else:
            p = self._subtree_search( self.root(), k )
            self._rebalance_access( p )
            return p

    def find_min( self ):
        if self.is_empty():
            return None
        else:
            p = self._first()
            return (p.key(), p.value() )

    def find_max( self ):
        if self.is_empty():
            return None
        else:
            p = self._last()
            return (p.key(), p.value() )

    def find_ge( self, k ):
        if self.is_empty():
            return None
        else:
            p = self._find_position( k )
            if p.key() < k:
                p = self._after( p )
            return (p.key(), p.value()) if p is not None else None

    def find_gt( self, k ):
        if self.is_empty():
            return None
        else:
            p = self._find_position( k )
            if p.key() == k:
                p = self._after( p )
            return (p.key(), p.value()) if p is not None else None

    def find_le( self, k ):
        if self.is_empty():
            return None
        else:
            p = self._find_position( k )
            if p.key() > k:
                p = self._before( p )
            return (p.key(), p.value()) if p is not None else None

    def find_lt( self, k ):
        if self.is_empty():
            return None
        else:
            p = self._find_position( k )
            if p.key() >= k:
                p = self._before( p )
            return (p.key(), p.value()) if p is not None else None

    def find_range( self, start, stop ):
        if not self.is_empty():
            if start is None:
                p = self._first()
            else:
                p = self._find_position( start )
                if p.key() < start:
                    p = self._after( p )
                while p is not None and (stop is None or p.key() < stop):
                    yield (p.key(), p.value())
                    p = self._after( p )

    def rebalance( self, p ):
        pass

    def _rebalance_delete( self, p ):
        pass

    def _rebalance_access( self, p ):
        pass

    def _rebalance_insert( self, p ):
        pass

    #relink parent and child node (child can be None)
    def _relink( self, parent, child, make_left_child ):
        #make it a left child
        if make_left_child:
            parent._left = child
        #make it a right child
        else:
            parent._right = child
        #make child point to parent
        if child is not None:
            child._parent = parent

    def _rotate( self, p ):
        x = p._node
        y = x._parent
        z = y._parent
        if z is None: #x becomes root
            self._root = x
            x._parent = None
        else:
            #x becomes direct child of z
            self._relink( z, x, y == z._left )
        #rotate x and y, and transfer middle subtree
        if x == y._left:
            self._relink( y, x._right, True )
            self._relink( x, y, False )
        else:
            self._relink( y, x._left, False )
            self._relink( x, y, True )

    def _restructure( self, x ):
        y = self.parent( x )
        z = self.parent( y )
        #check for case #1 and #2
        #single rotation
        if( x == self.right( y ) ) == (y == self.right( z ) ):
            self._rotate( y )
            return y
        #else case #3 or #4
        #double rotation
        else:
            self._rotate( x )
            self._rotate( x )
            return x

    def __getitem__( self, k ):
        if self.is_empty():
            return False
        else:
            p = self._subtree_search( self.root(), k )
            self._rebalance_access( p )
            if k != p.key():
                return False
            return p.value()

    def __str__( self ):
        pp = "["
        for (k,v) in self.items():
            pp += "(" + str( k ) + "," + str( v ) + ")"
        pp += "]"
        return pp

    def __setitem__( self, k, v ):
        if self.is_empty():
            leaf = self._add_root( self._Item( k, v ) )
        else:
            p = self._subtree_search( self.root(), k )
            if p.key() == k:
                p.element()._value = v
                self._rebalance_access( p )
                return
            else:
                item = self._Item( k, v )
                if p.key() < k:
                    leaf = self._add_right( p, item )
                else:
                    leaf = self._add_left( p, item )
        self.rebalance( leaf )

    def __iter__( self ):
        p = self._first()
        while p is not None:
            yield p.key()
            p = self._after( p )

    def delete( self, p ):
        self._validate( p )
        if self.left( p ) and self.right( p ):
            replacement = self._subtree_last_position( self.left( p ) )
            self._replace( p, replacement.element() )
            p = replacement
        parent = self.parent( p )
        self._delete( p )
        self._rebalance_delete( parent )

    def __delitem__( self, k ):
        if not self.is_empty():
            p = self._subtree_search( self.root(), k )
            if k == p.key():
                self.delete( p )
                return
            self._rebalance_access( p )
        return False

"""unit testing
"""
if __name__ == '__main__':

    print( "TreeMap unit testing..." )

#     M = TreeMap( )
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

#     M = TreeMap( )
#     print( len( M ) ) #0
#     M['K'] = 2
#     print( M )
#     print( len( M ) )
#     M['B'] = 4
#     print( M )
#     print( len( M ) )
#     M['U'] = 2
#     print( M )
#     print( len( M ) )
#     M['V'] = 8
#     print( M )
#     print( len( M ) )

#     M['K'] = 9
#     print( M )
#     print( len( M ) )
#     print( M['B'] )
#     print( M['X'] )
#     print( M.get( 'F' ) )
#     print( M.get( 'F', 5 ) )
#     print( M.get( 'K', 5 ) )
#     print( M )
#     print( len( M ) )
#     del M['V']
#     print( "pop(K) = ", M.pop( 'K' ) )
#     print( M )
#     for key in M.keys():
#         print( str( key ) )
#     for value in M.values():
#         print( str( value ) )
#     for item in M.items():
#         print( str( item ) )
#     print( M.setdefault( 'B', 1 ) )
#     print( M.setdefault( 'AA', 1 ) )
#     print( M )
#     print( M.popitem() )
#     print( M )
#     print( M.find_min() )
#     print( M.find_max() )

    M = TreeMap()
    nb = 50
    random.seed( 131341 )
    avant = time.time()
    for i in range( nb ):
        key = random.randint( 0, nb )
        M[key] = key
    apres = time.time()
    print( "Insertion of", nb, "keys in ", apres-avant, "seconds." )
    print( M )

    print( M.find_min() )
    print( M.find_max() )

    print( M.find_ge( 25 ) )
    print( M.find_gt( 25 ) )
    print( M.find_le( 25 ) )
    print( M.find_lt( 25 ) )
    print( M.find_lt( 0 ) )

    for (x,y) in M.find_range( 12, 100 ):
        print( "x =", x, ", y =", y )

    
    print( "End of testing." )
