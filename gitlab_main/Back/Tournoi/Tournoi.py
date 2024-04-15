class Match():
    def __init__(self,participant=None,parent=None):
        self.left=None
        self.rigth=None
        self.winner=participant
        self.parent=parent
    
    def is_leaf(self):
        if self.left is None and self.right is None: return True
        else : return False
    
    def is_complete(self):
        if self.is_leaf():  return True
        elif self.left is not None and self.right is None: return False
        elif self.left is  None and self.right is not None: return False
        else : return (self.left.is_complete() and self.right.is_complete())
    
    def add(self,participant):
        if self.is_leaf():
            if self.winner is None :  self.winner = participant
            old=self
            self = Match()
            old.parent=self
            new=Match(participant,self)
            self.left=old
            self.right=new
            self.hauteur = 1
        else: 
            if self.left.is_complete() and not self.right.is_complete():
                if self.left.hauteur < self.right.hauteur:
                    self.left.add(participant)
                elif self.left.hauteur > self.right.hauteur:
                    self.rigth.add(participant)
                else : # ils sont egaux 
                    self.rigth.add(participant)
            else :#self.left.is_complete() and not self.right.is_complete():
                if self.left.hauteur <=self.right.hauteur:
                    self.left.add(participant)
                elif self.left.hauteur > self.right.hauteur:
                    self.rigth.add(participant)