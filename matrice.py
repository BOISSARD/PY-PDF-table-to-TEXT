class Matrice :
    """
    Classe pour gérer une matrice avec des fonctionnalités d'ajout et d'affichage.
    """

    def __init__(self, matrix=None):
        """
        Initialise une matrice vide.
        """
        self.matrix = None
        if matrix:
            self.matrix = []
            for i, row in enumerate(matrix):
                for j, value in enumerate(row):
                    self.set(value, i, j)

    def set(self, data, row_idx, col_idx):
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
        if not self.matrix : self.matrix = []
        while len(self.matrix) <= row_idx:
            self.matrix.append([])

        # Étendre toutes les lignes pour qu'elles aient au moins col_idx + 1 colonnes
        for row in self.matrix:
            while len(row) <= col_idx:
                row.append(None)

        # Ajouter la donnée à la position spécifiée
        self.matrix[row_idx][col_idx] = data

    def get_column_str_width(self, col_idx):
        """
        Calcule la largeur maximale des éléments dans une colonne spécifique.

        Args:
            col_idx (int): L'index de la colonne.

        Returns:
            int: La largeur maximale des éléments dans la colonne spécifiée.
        """
        if not self.matrix : return 1        
        return max(
            len(str(row[col_idx])) if col_idx < len(row) and row[col_idx] is not None else 4
            for row in self.matrix
        ) + 2

    def __str__(self):
        """
        Affiche la matrice de manière lisible dans la console.
        """
        if not self.matrix:
            return "| |"

        col_widths = []
        max_cols = max(len(row) for row in self.matrix)
        col_widths = [self.get_column_str_width(col_idx) -2 for col_idx in range(max_cols)]

        rows = []
        for row in self.matrix:
            # Formater chaque ligne avec les colonnes alignées individuellement
            formatted_row = " | ".join(
                f"{str(row[col_idx]) if col_idx < len(row) and row[col_idx] is not None else 'None':>{(col_widths[col_idx])}}"
                for col_idx in range(max_cols)
            )
            rows.append(f"| {formatted_row} |")

        return "\n".join(rows)
            
    def to_list(self) :
        return self.matrix
            
if True :
    # matrice = Matrice([ [1, 2, 3], [4, 5, 6] ])
    matrice = Matrice([ [1, 2], [3], [4, 5, 6] ])
    print("Initial :"); print(matrice)
    matrice.set(99, 4, 2) # Ajout à une nouvelle ligne
    matrice.set(88, 0, 4) # Ajout à une colonne existante
    print("Modifiée :"); print(matrice)
    print(matrice.to_list())
    print(Matrice(), Matrice().get_column_str_width(0))