import requests
import fitz
import re
from flask import Flask, render_template, request

app = Flask(__name__)

def extract_missions_principales_from_pdf(pdf_url):
    # Télécharger le contenu du fichier PDF à partir du lien
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as file:
        file.write(response.content)

    # Extraire les missions principales
    missions_principales = "Aucune information trouvée"
    with fitz.open("temp.pdf") as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            missions_start = re.search(r"Missions\s+principales", page_text, re.IGNORECASE)
            if missions_start:
                missions_start = missions_start.end()
                missions_end = page_text.find("PROFIL", missions_start)
                missions_principales = page_text[missions_start:missions_end].strip()
                break

    return missions_principales

# Route pour afficher le formulaire d'upload de fichier
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route pour traiter le fichier uploadé
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                print(file)
                pdf_url = "http://localhost:5000/uploads/" + file.filename
                # pdf_url = "http://localhost:8000/missions_principales.json"
                missions_principales = extract_missions_principales_from_pdf(pdf_url)
                return render_template('result.html', missions_principales=missions_principales)

    return "Aucun fichier sélectionné"

if __name__ == '__main__':
    app.run(debug=True)
