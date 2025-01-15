import pdfplumber

def handle_merged_cells(raw_table):
    """
    Reconstruit un tableau avec gestion des cellules fusionnées
    en propageant les valeurs horizontalement et verticalement.
    """
    # Préparation d'une liste pour le tableau reconstruit
    reconstructed_table = []

    # Parcourir les lignes du tableau brut
    for row_idx, row in enumerate(raw_table):
        # Si c'est la première ligne, ajouter directement (assume qu'il n'y a pas de fusion verticale ici)
        if row_idx == 0:
            reconstructed_table.append(row)
            continue

        # Initialiser une ligne vide pour reconstruction
        reconstructed_row = []
        for col_idx, cell in enumerate(row):
            if cell is None or cell == "":
                # Si la cellule est vide, utiliser la valeur au-dessus (fusion verticale)
                reconstructed_row.append(reconstructed_table[row_idx - 1][col_idx])
            else:
                # Sinon, utiliser la valeur actuelle
                reconstructed_row.append(cell)
        
        # Ajouter la ligne reconstruite
        reconstructed_table.append(reconstructed_row)
    
    return reconstructed_table

def table_to_markdown(table):
    """
    Convertit un tableau (liste de listes) en format Markdown.
    """
    header = "| " + " | ".join(table[0]) + " |"
    separator = "| " + " | ".join(["---"] * len(table[0])) + " |"
    rows = "\n".join("| " + " | ".join(row) + " |" for row in table[1:])
    return f"{header}\n{separator}\n{rows}"


def extract_pdf_content(pdf_path):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            
            vertical_lines = page.lines
            print(vertical_lines)
            continue
            
            # Extraire le texte brut
            text = page.extract_text()
            if text:
                # result.append(f"## Page {page_number}\n")
                result.append(f"{text}\n")
            
            # Extraire les tableaux
            tables = page.extract_tables()
            for table_number, raw_table in enumerate(tables, start=1):
                # Gérer les cellules fusionnées
                if raw_table:
                    print("-------------------\n")
                    # print(raw_table)
                    # continue
                    
                    reconstructed_table = handle_merged_cells(raw_table)
                    print(reconstructed_table)
                    continue
                    
                    # Convertir le tableau selon le format choisi
                    if output_format == "markdown":
                        markdown_table = table_to_markdown(reconstructed_table)
                        # result.append(f"### Table {table_number} (Page {page_number})\n")
                        result.append(f"\n{markdown_table}\n")
                    elif output_format == "csv":
                        csv_table = "\n".join(",".join(row) for row in reconstructed_table)
                        # result.append(f"### Table {table_number} (Page {page_number})\n")
                        result.append(f"{csv_table}\n")
                    elif output_format == "html":
                        html_table = "<table>\n" + "\n".join(
                            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in reconstructed_table
                        ) + "\n</table>"
                        # result.append(f"### Table {table_number} (Page {page_number})\n")
                        result.append(f"{html_table}\n")
    
    return "\n".join(result)


