from collections import deque

class Match():
    def __init__(self, participant1=None, participant2=None,parent = None):
        self.p1 = participant1
        self.p2 = participant2
        self.winner = None
        self.hauteur = 0
        self.left = None
        self.right = None
        self.parent = parent
            
    def is_leaf(self):   
        if self.left is None and self.right is None : return True
        else : return False
        
    def leaf_complete(self):
        if self.p1 is None or self.p2 is None: return False
        return True
    
    def branch_complete(self): 
        if self.is_leaf(): return self.leaf_complete()
        
        return self.left.branch_complete() and self.right.branch_complete()
    
    def update_hauteur(self):
        # Mise à jour de la hauteur pour refléter la hauteur réelle du sous-arbre
        if self.is_leaf():
            self.hauteur = 0
        else:
            self.hauteur = 1 + max(
                self.left.hauteur if self.left is not None else 0,
                self.right.hauteur if self.right is not None else 0
            )
    def udpate_branche_hauteur(self):
        if self.parent is None: 
            self.update_hauteur() 
            return
        else : 
            self.update_hauteur()
            self.parent.udpate_branche_hauteur()
            
    def ajoute(self, participant):
        if(self.is_leaf()):
            if not self.leaf_complete():
                if self.p1 is None: self.p1 = participant
                else: self.p2 = participant
            else:
                self.left  = Match(self.p1, self.p2,self)
                self.right= Match(participant,parent=self)
                self.p1 = None
                self.p2 = None
                self.udpate_branche_hauteur()
    
        else:
            if self.left.branch_complete() and self.right.branch_complete():
                if self.right.hauteur>=self.left.hauteur: self.left.ajoute(participant)
                else: self.right.ajoute(participant)
            elif not self.right.branch_complete():
                self.right.ajoute(participant)
            else: self.left.ajoute(participant)
            
class Node:
    def __init__(self, participant=None, parent=None):
        self.p1 = None
        self.p2 = None
        self.left = None
        self.right = None
        self.hauteur = 1
        self.parent = parent
        if participant:
            self.p1 = participant

    def is_leaf(self):
        return not self.left and not self.right
    
    def is_leaf(self):   
        if self.left is None and self.right is None : return True
        else : return False
        
    def leaf_complete(self):
        if self.p1 is None or self.p2 is None: return False
        return True
    
    def branch_complete(self): 
        if self.is_leaf(): return self.leaf_complete()
        return self.left.branch_complete() and self.right.branch_complete()
    
    def has_room(self):
        return self.p1 is None or self.p2 is None

class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, participant):
        if not self.root:
            self.root = Node(participant)
        else:
            self.root = self._insert(self.root, participant)

    def _insert(self, node, participant):
        if node.is_leaf():
            if node.has_room():
                if not node.p1:
                    node.p1 = participant
                elif not node.p2:
                    node.p2 = participant
                return node
            else:
                # Si les deux participants sont déjà présents, créer de nouveaux nœuds
                node.left = Node(node.p1, node)
                node.left.p2 = node.p2
                node.p1, node.p2 = None, None
                node.right = Node(participant, node)
                return self._rebalance(node)
        else:
            # Priorité au sous-arbre gauche pour l'insertion
            if not node.left or not node.left.branch_complete():
                if not node.left:
                    node.left = Node(parent=node)
                node.left = self._insert(node.left, participant)
            elif not node.right or not node.right.branch_complete():
                if not node.right:
                    node.right = Node(parent=node)
                node.right = self._insert(node.right, participant)
            else:
                # Si les deux sous-arbres sont complets, continuez à suivre la logique d'insertion à gauche
                node.left = self._insert(node.left, participant)
            return self._rebalance(node)


    def _rebalance(self, node):
        self._update_height(node)
        
        balance = self._get_balance(node)
        # Simple gauche
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Simple droite
        elif balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, x):
        y = x.right
        y.parent = x.parent
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.left = x
        x.parent = y
        self._update_height(x)
        self._update_height(y)
        return y

    def _rotate_right(self, y):
        x = y.left
        x.parent = y.parent
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.right = y
        y.parent = x
        self._update_height(y)
        self._update_height(x)
        return x

    def _update_height(self, node):
        node.hauteur = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_height(self, node):
        if not node:
            return 0
        return node.hauteur

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)


            
def afficher_arbre(racine):
    if not racine:
        return "L'arbre est vide."
    
    queue = deque([racine])
    niveau = 0
    while queue:
        taille_niveau = len(queue)
        print(f"Niveau {niveau}: ", end='')
        while taille_niveau > 0:
            noeud = queue.popleft()
            if noeud.left is not None:  
                queue.append(noeud.left)
            if noeud.right is not None:  
                queue.append(noeud.right)
            
            details_match = f"[{noeud.p1 if noeud.p1 else 'N/A'} vs {noeud.p2 if noeud.p2 else 'N/A'}, Winner: {noeud.winner if noeud.winner else 'N/A'}]"
            print(details_match, end=' ')
            
            taille_niveau -= 1
        print()  
        niveau += 1

from collections import deque

def afficher_arbre_avl(avl_tree):
    # Vérifie si l'arbre est vide en vérifiant la racine de l'AVLTree
    if not avl_tree.root:
        return "L'arbre est vide."
    
    queue = deque([avl_tree.root])  # Commence avec le nœud racine de l'arbre
    niveau = 0
    while queue:
        taille_niveau = len(queue)
        print(f"Niveau {niveau}: ", end='')
        while taille_niveau > 0:
            noeud = queue.popleft()
            # Vérifie et ajoute les enfants du nœud actuel à la file d'attente
            if noeud.left is not None:
                queue.append(noeud.left)
            if noeud.right is not None:
                queue.append(noeud.right)
            
            # Affiche les détails pour chaque nœud
            if noeud.is_leaf():
                details_match = f"[{noeud.p1 if noeud.p1 else 'N/A'} vs {noeud.p2 if noeud.p2 else 'N/A'}, Hauteur: {noeud.hauteur}]"
            else:
                details_match = f"[Nœud interne, Hauteur: {noeud.hauteur}]"
            print(details_match, end=' ')
            
            taille_niveau -= 1
        print()  # Nouveau ligne après chaque niveau
        niveau += 1



# Créer une instance racine de Match
racine = Match()
root = AVLTree()
# Ajouter plusieurs participants pour tester
participants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
for participant in participants:
    racine.ajoute(participant)
    root.insert(participant)
print("       ")

# Afficher l'arbre de matchs
#afficher_arbre(racine)
afficher_arbre_avl(root)
