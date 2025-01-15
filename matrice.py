class Matrice :
    """
    Classe pour gérer une matrice avec des fonctionnalités d'ajout et d'affichage.
    """

    def __init__(self, initial=None):
        """
        Initialise une matrice vide.
        """
        self.matrix = []

    def add_data(self, data, row_idx, col_idx):
        """
        Ajoute un élément dans la matrice tout en maintenant sa cohérence.

        Si l'index de la ligne n'existe pas, des lignes supplémentaires sont ajoutées.
        Si l'index de la colonne n'existe pas, des colonnes supplémentaires sont ajoutées à toutes les lignes.

        Args:
            data: La donnée à ajouter.
            row_idx (int): L'index de la ligne.
            col_idx (int): L'index de la colonne.
        """
        # Ajouter des lignes si nécessaire
        while len(self.matrix) <= row_idx:
            self.matrix.append([])

        # Trouver le nombre maximal de colonnes existantes
        max_cols = max((len(row) for row in self.matrix), default=0)

        # Étendre toutes les lignes pour qu'elles aient au moins col_idx + 1 colonnes
        for row in self.matrix:
            while len(row) <= col_idx:
                row.append(None)

        # Ajouter la donnée à la position spécifiée
        self.matrix[row_idx][col_idx] = data

    def __str__(self):
        """
        Affiche la matrice de manière lisible dans la console.
        """
        if not self.matrix:
            return "[]"

        # Trouver la largeur maximale des éléments pour un affichage aligné
        max_width = max(
            len(str(element)) if element is not None else 4
            for row in self.matrix for element in row
        )

        rows = []
        for row in self.matrix:
            # Formater chaque ligne avec les éléments alignés
            formatted_row = " | ".join(
                f"{str(element) if element is not None else 'None':>{max_width}}"
                for element in row
            )
            rows.append(f"[ {formatted_row} ]")

        return "\n".join(rows)
            
    def to_list(self) :
        return self.matrix
            
# matrice = Matrice([ [1, 2, 3], [4, 5, 6] ])
matrice = Matrice([ [1, 2], [3], [4, 5, 6] ])
print(matrice)
matrice.add_data(99, 3, 2) # Ajout à une nouvelle ligne
matrice.add_data(88, 0, 4) # Ajout à une colonne existante
print(matrice)