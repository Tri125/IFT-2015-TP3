"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 11 avril 2014.
   Ref: Data Structure & Algorithms in Python
        Goodrich, Tamassia et Goldwasser, 2013
"""
import random
import time
from TreeMap import TreeMap

class RedBlackTreeMap( TreeMap ):

    class _Node( TreeMap._Node ):
        __slots__ = '_red'

        def __init__( self, element, parent = None, left = None, right = None ):
            super().__init__( element, parent, left, right )
            self._red = True

    def _set_red( self, p ): p._node._red = True
    def _set_black( self, p ): p._node._red = False
    def _set_color( self, p, make_red ): p._node._red = make_red
    def _is_red( self, p ): return p is not None and p._node._red
    def _is_red_leaf( self, p ): return self._is_red( p ) and self.is_leaf( p )

    def _get_red_child( self, p ):
        for child in ( self.left( p ), self.right( p ) ):
            if self._is_red( child ):
                return child
        return None

    def _rebalance_insert( self, p ):
        #new node always red
        self._resolve_red( p )

    def _resolve_red( self, p ):
        if self.is_root( p ):
            #make root black
            self._set_black( p )
        else:
            parent = self.parent( p )
            if self._is_red( parent ):
                #double red problem
                uncle = self.sibling( parent )
                if not self._is_red( uncle ):
                    #Case 1: misshapen 4-node
                    middle = self._restructure( p ) #do trinode restructuring
                    self._set_black( middle )       #and then fix colors
                    self._set_red( self.left( middle ) )
                    self._set_red( self.right( middle ) )
                else:
                    #Case 2: overfull 5-node
                    grand = self.parent( parent )
                    self._set_red( grand )                #grandparent becomes red
                    self._set_black( self.left( grand ) ) #its children become black
                    self._set_black( self.right( grand ) )
                    self._resolve_red( grand )            #recur at red grandparent

    def _rebalance_delete( self, p ):
        if len( self ) == 1:
            #special case: ensure root is black
            self._set_black( self._root() )
        elif p is not None:
            n = self.num_children( p )
            if n == 1:
                #deficit exists unless child is a red leaf
                c = next( self.children( p ) )
                if not self._is_red_leaf( c ):
                    self._fix_deficit( p, c )
            elif n == 2:
                if self._is_red_leaf( self.left( p ) ):
                    self._set_black( self.left( p ) )
                else:
                    self._set_black( self.right( p ) )
    
    def _fix_deficit( self, z, y ):
        #resolve black deficit at z, where y is the root of z's heavier subtree
        if not self._is_red( y ):
            #y is black; will apply Case 1 or 2
            x = self._get_red_child( y )
            if x is not None:
                #Case 1: y is black and has red child x; do "transfer"
                old_color = self._is_red( z )
                middle = self._restructure( x )
                self._set_color( middle, old_color )
                self._set_black( self.left( middle ) )
                self._set_black( self.right( middle ) )
            else:
                #Case 2: y is black, but no red children; recolor as "fusion"
                self._set_red( y )
                if self._is_red( z ):
                    self._set_black( z ) #this resolves the problem
                elif not self.is_root( z ):
                    self._fix_deficit( self.parent( z ), self.sibling( z ) ) #recur upward
        else:
            #Case 3: y is red; rotate misaligned 3-node and repeat
            self._rotate( y )
            self._set_black( y )
            self._set_red( z )
            if z == self.right( y ):
                self._fix_deficit( z, self.left( z ) )
            else:
                self._fix_deficit( z, self.right( z ) )


"""unit testing
"""
if __name__ == '__main__':

    print( "RedBlackTreeMap unit testing..." )

    M = RedBlackTreeMap( )
    nb = 100000
    random.seed( 131341 )

    #Insertion
    avant = time.time()
    for i in range( nb ):
        key = random.randint( 0, nb )
        M[key] = key
    apres = time.time()
    print( "Insertion of", nb, "keys in ", apres-avant, "seconds." )

    #Access
    random.seed( 131341 )
    avant = time.time()
    for i in range( nb ):
        key = random.randint( 0, nb )
        x = M[key]
    apres = time.time()
    print( "Access of", nb, "keys in ", apres-avant, "seconds." )

    #Delete
    avant = time.time()
    nbdel = 0
    for i in range( nb ):
        key = random.randint( 0, nb )
        del M[key]
    apres = time.time()
    print( "Delete ", nb, "keys in ", apres-avant, "seconds." )

#     M = RedBlackTreeMap( )
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

#     M = RedBlackTreeMap()
#     nb = 50
#     random.seed( 131341 )
#     avant = time.time()
#     for i in range( nb ):
#         key = random.randint( 0, nb )
#         M[key] = key
#     apres = time.time()
#     print( "Insertion of", nb, "keys in ", apres-avant, "seconds." )
#     print( M )

#     print( M.find_min() )
#     print( M.find_max() )

#     print( M.find_ge( 25 ) )
#     print( M.find_gt( 25 ) )
#     print( M.find_le( 25 ) )
#     print( M.find_lt( 25 ) )
#     print( M.find_lt( 0 ) )

#     for (x,y) in M.find_range( 12, 100 ):
#         print( "x =", x, ", y =", y )
    
    print( "End of testing." )

