"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

from ArrayQueue import ArrayQueue

#ADT Tree "interface"
class Tree:

    class Position:

        def element( self ):
            pass

        def __eq__( self, other ):
            pass

        def __ne__( self, other):
            return not( self == other )

    def root( self ):
        pass

    def parent( self, p ):
        pass

    def num_children( self, p ):
        pass

    def children( self, p ):
        pass

    def __len__( self ):
        pass

    def is_root( self, p ):
        return self.root() == p

    def is_leaf( self, p ):
        return self.num_children( p ) == 0

    def is_empty( self ):
        return len( self ) == 0

    def depth( self, p ):
        #returns the number of ancestors of p
        if self.is_root( p ):
            return 0
        else:
            return 1 + self.depth( self.parent() )

    def height1( self, p ):
        #returns the maximum depth of the leaf positions
        return max( self.depth( p ) for p in self.positions() if self.is_leaf( p ))

    def height2( self, p ):
        #returns the height of the subtree at Position p
        if self.is_leaf( p ):
            return 0
        else:
            return 1 + max( self.height2( c ) for c in self.children( p ) )

    def height( self, p = None ):
        #returns the height of the subtree rooted at Position p
        #if p is None, then the height of the entire tree
        if p is None:
            p = self.root()
        return self.height2( p )
        
    def preorder_print( self, p ):
        print( p )
        for c in self.children( p ):
            self.preorder_print( c )

    def postorder_print( self, p ):
        for c in self.children( p ):
            self.preorder_print( c )
        print( p )

    def breadth_first_print( self ):
        Q = ArrayQueue()
        Q.enqueue( self.root() )
        while not Q.is_empty():
            p = Q.dequeue()
            print( p )
            for c in self.children( p ):
                Q.enqueue( c )
            
