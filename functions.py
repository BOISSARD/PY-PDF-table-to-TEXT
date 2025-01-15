import pdfplumber
import pandas as pd
# import camelot

def handle_merged_cells(df):
    """
    Gère les cellules fusionnées en remplissant les valeurs manquantes
    avec les valeurs précédentes (horizontalement et verticalement).
    """
    # df = pd.DataFrame(raw_table)
    df = df.fillna("")  # Remplace les valeurs None par des chaînes vides
    
    # Remplissage horizontal (gère les cellules fusionnées en colonnes)
    # df = df.apply(lambda x: x.ffill(), axis=1)
    for i, row in df.iterrows():
        df.iloc[i] = row.ffill()  # Remplit vers la gauche
    
    # Remplissage vertical (gère les cellules fusionnées en lignes)
    df = df.ffill(axis=0)
    
    return df

def extract_pdf_content(pdf_path, output_format="markdown"):
    result = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            print("========================\nPage", page_number)
            # Extraire le texte brut de la page
            text = page.extract_text()
            if text:
                print("-------------------------\ntext\n", text)
                # result.append(f"## Page {page_number}\n")
                result.append(f"{text}\n")

            tables = page.extract_tables()
            for _, table in enumerate(tables, start=1):
                print("-------------------------\ntable avant\n", table)
                # df = pd.DataFrame(table[1:], columns=table[0])  # Convertir en DataFrame
                df = pd.DataFrame(table)
                print(df)
                df = handle_merged_cells(df)
                print("table après\n", df)
                
                if output_format == "markdown":
                    markdown_table = df.to_markdown(index=False)
                    # result.append(f"### Table {table_number} (Page {page_number})\n")
                    result.append(f"\n{markdown_table}\n")
                elif output_format == "csv":
                    csv_string = df.to_csv(index=False)
                    # result.append(f"### Table {table_number} (Page {page_number})\n")
                    result.append(f"{csv_string}\n")
                elif output_format == "html":
                    html_table = df.to_html(index=False)
                    # result.append(f"### Table {table_number} (Page {page_number})\n")
                    result.append(f"{html_table}\n")
    
    return "\n".join(result)