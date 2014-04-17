"""Code Python pour le cours IFT2015
   Mise à jour par François Major le 23 mars 2014.
"""

from Tree import Tree

class BinaryTree( Tree ):

    def left( self, p ):
        pass

    def right( self, p ):
        pass

    def sibling( self, p ):
        #return the sibling Position
        parent = self.parent()
        if parent is None:
            return None
        else:
            if p == self.left( parent ):
                return self.right( parent )
            else:
                return self.left( parent )

    def children( self, p ):
        if self.left( p ) is not None:
            yield self.left( p )
        if self.right( p ) is not None:
            yield self.right( p )

    def inorder_print( self, p ):
        if self.left( p ) is not None:
            self.inorder_print( self.left( p ) )
        print( p )
        if self.right( p ) is not None:
            self.inorder_print( self.right( p ) )
