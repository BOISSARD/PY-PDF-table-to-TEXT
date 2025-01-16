import pdfplumber
from matrice import Matrice 

def table_to_markdownlike(raw_table):
    """
    Convertit une matrice en Markdown, en utilisant les bordures horizontales pour ajouter des séparateurs.
    """
    print("\ntable_to_markdown")
    
    markdown = []
    blocs = ["-"]
    # Création des rows
    for row in raw_table:
        # A partir de la row de raw_table on va construire les row réelles du tableau, notamment car si il n'y a pas de séparateur (border) alors ce n'est parfois pas considéré comme une nouvelle row et ça ajoute juste un saut à la ligne dans la cellule et ceux pour toutes les colonnes de la row
        new_markdown_rows = Matrice()
        
        max_height = max(len(cel.split("\n")) if cel else 1 for cel in row)
        
        for cel_idx, cel in enumerate(row):
            # Ajouter des lignes vides pour combler la hauteur restante
            for i in range(0, max_height):
                new_markdown_rows.set("", i, cel_idx)
            
            if not cel :
                new_markdown_rows.set(cel, 0, cel_idx)
                continue
                
            textes = cel.split("\n")
            for texte_idx, texte in enumerate(textes) :
                new_markdown_rows.set(texte, texte_idx, cel_idx)
     
        for new_row in new_markdown_rows.to_list() : 
            blocs.append(new_row)
        blocs.append("-")
        
    # Calcul des colonnes, largeur etc avant la génération du markdown
    nb_max_columns = 0
    config_display = []
    for bloc in blocs :
        config_columns = "-"
        
        nb_columns = 0 
        if isinstance(bloc, list) :
            nb_columns = len(bloc)
            config_columns = []
            for i, col in enumerate(bloc) :
                if col is None :
                    if i > 0 and len(config_columns) > 0 :
                        config_columns[len(config_columns)-1]["span"] += 1
                        continue
                
                config_col = {
                    "value": col,
                    "min_width": (len(str(col))+2) if col is not None else 1,
                    "col": i,
                    "span": 1,
                }
                config_columns.append(config_col)
            if nb_columns > nb_max_columns : nb_max_columns = nb_columns
            
        config_display.append(config_columns)
        
    columns_width = [0] * nb_max_columns
    # config_display[1][0]["min_width"] = 150 # TODO : to remove, juste a hard test
    
    for i in range(nb_max_columns) :
        sorted_rows = sorted(
            [row for row in config_display if row != "-"],
            key=lambda row: next((col["span"] for col in row if col["col"] <= i < col["col"] + col["span"]), float('inf'))
        )
        
        for row in sorted_rows :
            col_of_row = next((col for col in row if col["col"] <= i < col["col"] + col["span"]))
            total_span_width = sum(columns_width[c] for c in range(col_of_row["col"], col_of_row["col"] + col_of_row["span"]))
            if col_of_row["span"] == 1 and col_of_row["min_width"] > columns_width[i] :
                columns_width[i] = col_of_row["min_width"]
            elif col_of_row["span"] > 1 and i == (col_of_row["col"] + col_of_row["span"] - 1) and col_of_row["min_width"] > total_span_width :
                excess_width = col_of_row["min_width"] - total_span_width
                for j in range(excess_width) :
                    columns_width[j%col_of_row["span"]] += 1
        
    # Génération du markdown
    for display in config_display :
        if display == "-":
            # Générer une ligne de séparation horizontale
            separator = "|" + "|".join("-" * (width) for width in map(int, columns_width)) + "|"
            markdown.append(separator)
        elif isinstance(display, list):
            # Générer une ligne de contenu
            line = []
            for cel in display:
                width = sum(columns_width[col] for col in range(cel["col"], cel["col"] + cel["span"])) -3 + cel["span"]# 
                if cel["value"] is None:
                    line.append(" " * (width ))
                else :
                    line.append(f"{cel["value"]:>{width}}" if cel["col"] > 0 else f"{cel["value"]:<{width}}")
            line_markdown = "| " + " | ".join(line) + " |"
            markdown.append(line_markdown)
                
    retour = "\n".join(markdown)
    return retour


def extract_pdf_content(pdf_path):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            result.append(f"--- Page {page_number}\n")

            # Récupérer les zones des tableaux et leur contenu
            tables = page.find_tables()
            print(page.find_tables())
            print(page.extract_tables())
            exit()
            elements = []

            # Ajouter les tableaux comme éléments avec leurs positions
            for table_idx, table in enumerate(tables, start=1):
                raw_table = page.extract_tables()[table_idx - 1]
                markdown_table = table_to_markdownlike(raw_table)
                elements.append({
                    "type": "table",
                    "content": markdown_table,
                    "bbox": table.bbox
                })

            # Extraire les mots pour reconstituer les lignes
            words = page.extract_words()
            lines = []
            current_line = []
            current_top = None

            for word in words:
                # Si nous passons à une nouvelle ligne (position verticale différente)
                if current_top is None or abs(word["top"] - current_top) > 3:
                    # Ajouter la ligne actuelle aux lignes et démarrer une nouvelle
                    if current_line:
                        lines.append(current_line)
                    current_line = [word]
                    current_top = word["top"]
                else:
                    # Ajouter le mot à la ligne actuelle
                    current_line.append(word)

            # Ajouter la dernière ligne
            if current_line:
                lines.append(current_line)

            # Ajouter les lignes comme éléments avec leurs positions
            for line in lines:
                line_text = " ".join(word["text"] for word in line)
                line_bbox = [min(word["x0"] for word in line), line[0]["top"],
                             max(word["x1"] for word in line), line[0]["bottom"]]

                # Vérifier si cette ligne intersecte un tableau
                intersects_table = False
                for table in elements:
                    if table["type"] == "table":  # Vérifier uniquement les tableaux
                        table_bbox = table["bbox"]
                        if (line_bbox[0] < table_bbox[2] and line_bbox[2] > table_bbox[0] and
                                line_bbox[1] < table_bbox[3] and line_bbox[3] > table_bbox[1]):
                            intersects_table = True
                            break

                if not intersects_table:
                    # Ajouter la ligne si elle n'est pas dans une zone de tableau
                    elements.append({
                        "type": "text",
                        "content": line_text,
                        "bbox": line_bbox
                    })

            # Trier tous les éléments par leur position verticale (top)
            elements.sort(key=lambda e: e["bbox"][1])

            # Construire le contenu final avec des espaces entre les éléments
            for idx, element in enumerate(elements):
                if idx > 0:
                    # Ajouter un espace avant chaque élément sauf le premier
                    result.append("")
                result.append(element["content"])

            result.append("")

    return "\n".join(result)

