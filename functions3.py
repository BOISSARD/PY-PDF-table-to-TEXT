import pdfplumber

def table_to_markdown(raw_table):
    """
    Convertit une matrice en Markdown, en utilisant les bordures horizontales pour ajouter des séparateurs.
    """
    print("\ntable_to_markdown")
    markdown = []
    cur_ligne = 0
    cur_col = 0
    for row_idx, row in enumerate(raw_table):
        print("row", row_idx, row)
        
        # A partir de la row de raw_table on va construire les row réelles du tableau, notamment car si il n'y a pas de séparateur (border) alors ce n'est parfois pas considéré comme une nouvelle row et ça ajoute juste un saut à la ligne dans la cellule et ceux pour toutes les colonnes de la row
        new_markdown_rows = []
        
        for cel_idx, cel in enumerate(row):
            print("cel", cel_idx)
            if not cel :
                new_markdown_rows.append
                
            textes = cel.split("\n")
            print(textes)
        
        # markdown.
    
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
                    markdown_table = table_to_markdown(raw_table)
                    result.append(markdown_table)
                
    return "\n".join(result)

