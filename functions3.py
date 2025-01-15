import pdfplumber
from matrice import Matrice 

def table_to_markdownlike(raw_table):
    """
    Convertit une matrice en Markdown, en utilisant les bordures horizontales pour ajouter des séparateurs.
    """
    print("\ntable_to_markdown")
    
    markdown = []
    blocs = []
    # Création des rows
    for row_idx, row in enumerate(raw_table):
        print("row", row_idx)
        
        # A partir de la row de raw_table on va construire les row réelles du tableau, notamment car si il n'y a pas de séparateur (border) alors ce n'est parfois pas considéré comme une nouvelle row et ça ajoute juste un saut à la ligne dans la cellule et ceux pour toutes les colonnes de la row
        new_markdown_rows = Matrice()
        
        max_height = max(len(cel.split("\n")) if cel else 1 for cel in row)
        # print(max_height)
        
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
            
        print(new_markdown_rows)
        print(new_markdown_rows.get_column_str_width(0))
     
        for new_row in new_markdown_rows.to_list() : 
            blocs.append(new_row)   
        blocs.append("-")
    # print(blocs)
        
    # Calcul des colonnes, largeur etc avant la génération du markdown
    nb_max_columns = 0
    config_display = []
    for bloc in blocs :
        # print(bloc)
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
                    "value": col, # if col is not None else "",
                    "min_width": (len(str(col))+2) if col is not None else 1,
                    "span": 1,
                }
                config_columns.append(config_col)
            if nb_columns > nb_max_columns : nb_max_columns = nb_columns
            
        print(nb_columns, config_columns)
        config_display.append(config_columns)
        
    # Génération du markdown
    
    print("markdown\n"); print(markdown)
    return "\n".join(markdown)


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
                if table_idx != 2: continue
                
                print("\n------------", f"\nTable {table_idx}", raw_table)
                
                # Construire le tableau
                if raw_table:
                    # table, horizontal_lines, vertical_lines = detect_borders_and_build_table(page, table)
                    markdownlike_table = table_to_markdownlike(raw_table)
                    result.append(markdownlike_table)
                
    return "\n".join(result)

