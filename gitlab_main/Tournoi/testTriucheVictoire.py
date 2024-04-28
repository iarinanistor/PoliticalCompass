class Candidat:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"Candidat(id={self.id})"

    def __lt__(self, other):  # Permet la comparaison pour le tri
        return self.id < other.id

def generate_flattened_pair_permutations(lst, constraints):
    """
    lst doit etre de taille paire
    """
    from itertools import permutations, product

    def normalize_permutation(perm):
        normalized = []
        for i in range(0, len(perm), 2):
            pair = sorted(perm[i:i+2], key=lambda x: x.id)  # Utilise une clé de tri basée sur l'id
            normalized.extend(pair)
        return tuple(normalized)

    elements_to_permute = [elem for elem in lst if elem not in constraints.keys()]
    free_permutations = permutations(elements_to_permute)
    valid_permutations = set()

    for free_perm in free_permutations:
        free_perm = list(free_perm)
        for position_combination in product(*constraints.values()):
            if len(set(position_combination)) == len(position_combination):
                try:
                    temp_perm = free_perm[:]
                    for element, position in zip(constraints.keys(), position_combination):
                        temp_perm.insert(position, element)
                    norm_perm = normalize_permutation(temp_perm)
                    flattened_perm = [item for pair in zip(norm_perm[::2], norm_perm[1::2]) for item in pair]
                    valid_permutations.add(tuple(flattened_perm))
                except IndexError:
                    continue

    return [list(perm) for perm in valid_permutations]

# Utilisation avec des objets
candidates = [Candidat(1), Candidat(1), Candidat(3)]
constraints = {candidates[2]: [2], candidates[0]: [1]}
result = generate_flattened_pair_permutations(candidates, constraints)
print(result)
