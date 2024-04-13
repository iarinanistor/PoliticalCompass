from collections import deque

class Match():
    def __init__(self, participant=None,parent = None):
        self.winner = participant
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
        if self.winner is None and self.is_leaf():
            self.winner = participant
        elif self.is_leaf() and self.winner is not None:
            # Stocker le gagnant actuel et réinitialiser le gagnant du nœud actuel
            tmp = self.winner
            self.winner = None

            # Créer des nœuds enfants pour le gagnant actuel et le nouveau participant
            self.left = Match(tmp, self)
            self.right = Match(participant, self)
            
            # Mise à jour de la hauteur à travers les branches
            self.udpate_branche_hauteur()
        else:
            # Ajouter récursivement le participant au sous-arbre avec la hauteur la plus basse
            if self.left is None or (self.right is not None and self.left.hauteur >= self.right.hauteur):
                if self.left is None:
                    self.left = Match(parent=self)
                self.left.ajoute(participant)
            else:
                if self.right is None:
                    self.right = Match(parent=self)
                self.right.ajoute(participant)
            
            # Mise à jour de la hauteur à travers les branches
            self.udpate_branche_hauteur()

    
        
    
    
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
                   
def print_tree(node, level=0):
    if node is not None:
        # Affiche le sous-arbre droit en premier, avec une augmentation du niveau d'indentation
        print_tree(node.right, level + 1)
        
        # Prépare l'indentation pour le niveau actuel
        indent = '   ' * level
        
        # Affiche les informations du match actuel
        # Pour les feuilles, affiche le participant comme 'p1 vs p2' n'est pas applicable
        if node.is_leaf():
            match_info = f"{indent}-> Participant: {node.winner if node.winner else 'En attente'}"
            print(match_info)
        else:
            # Pour les nœuds internes, affiche 'Match en attente' car les participants ne sont pas directement stockés
            winner_info = f" | Vainqueur: {node.winner if node.winner else 'En attente'}"
            print(f"{indent}-> Match en attente" + winner_info)
        
        # Affiche le sous-arbre gauche, avec le même niveau d'indentation
        print_tree(node.left, level + 1)

        
# Créer une instance racine de Match
racine = Match()
# Ajouter plusieurs participants pour tester
l = [ str(i) for i in range(0, 35)]
participants = ['1', '2', '3', '4', '5', '6','7', '8', '9', '10', '11','12','13']
#['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
for participant in l:
    racine.ajoute(participant)

print_tree(racine)
