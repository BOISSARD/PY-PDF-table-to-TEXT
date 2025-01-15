from functions3 import * 

# Chemin vers le fichier PDF
file_name = f"facture{1}"

# Appeler la fonction
input_file_name = f"Factures PDF/{file_name}.pdf"
result = extract_pdf_content(input_file_name)

# Sauvegarder le résultat dans un fichier texte
output_file_name = f"Factures TXT/{file_name}.txt"
with open(output_file_name, "w", encoding="utf-8") as file:
    file.write(result)

print(f"Contenu extrait et sauvegardé dans {output_file_name}")
