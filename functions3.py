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
    """
    Extrait les tableaux d'un PDF et les convertit en Markdown avec gestion des bordures et des fusions.
    """
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        
        for page_number, page in enumerate(pdf.pages, start=1):
            result.append(f"## Page {page_number}\n")
            
            text = page.extract_text()
            if text:
                # result.append(f"## Page {page_number}\n")
                result.append(f"{text}\n")
            
            # Extraire les tableaux
            raw_tables = page.extract_tables()
            for table_idx, raw_table in enumerate(raw_tables, start=1):
                # if table_idx != 2: continue
                
                print("\n------------", f"\nTable {table_idx}", raw_table)
                
                # Construire le tableau
                if raw_table:
                    # table, horizontal_lines, vertical_lines = detect_borders_and_build_table(page, table)
                    markdownlike_table = table_to_markdownlike(raw_table)
                    result.append(markdownlike_table)
                    result.append("")
                
    return "\n".join(result)

