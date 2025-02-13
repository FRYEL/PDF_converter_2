# PDF Translator and Summarizer

## 📌 Beschreibung

Diese Anwendung ermöglicht es Nutzern, Text aus PDF-Dokumenten zu extrahieren, in eine andere Sprache zu übersetzen und anschließend zusammenzufassen. Die Anwendung nutzt **Flask** als Backend und **HTML, CSS und JavaScript** für das Frontend. Für die Übersetzung wird die **Google Translate API** oder die **DeepL API** verwendet, während die Zusammenfassung über die **Hugging Face Inference API** erfolgt.

## 🚀 Funktionen

✅ **PDF-Text-Extraktion**: Lädt ein PDF hoch und extrahiert den enthaltenen Text.  
✅ **Automatische Übersetzung**: Unterstützt mehrere Sprachen (Englisch, Deutsch, Französisch, Spanisch, Italienisch).  
✅ **Text-Zusammenfassung**: Komprimiert lange Texte mithilfe eines NLP-Modells.  
✅ **Benutzerfreundliche Web-Oberfläche**: Einfache Bedienung mit Drag & Drop und interaktiven Elementen.  
✅ **Fehlermanagement**: Implementierte Retry-Logik für API-Anfragen.  

## 📂 Projektstruktur

```
/project-root
│── app.py                # Haupt-Backend-Anwendung mit Flask
│── ml_api_utils.py       # Funktionen für Übersetzung und Zusammenfassung
│── templates/
│   └── index.html        # Web-Oberfläche
│── static/
│   ├── styles.css        # CSS-Datei für das Styling
│── tests/
│   ├── cypress/          # Cypress-Testfälle
│   ├── cypress.config.js # Cypress-Konfiguration
│── requirements.txt      # Python-Abhängigkeiten
│── .env.example         # Beispiel für Umgebungsvariablen
│── README.md             # Diese Datei
```

## 🔧 Installation & Setup

### 1️⃣ Voraussetzungen

Stelle sicher, dass folgende Software installiert ist:

- **Python 3.8 oder höher** [Download](https://www.python.org/downloads/)
- **Node.js und npm** [Download](https://nodejs.org/)

### 2️⃣ Projekt klonen & Abhängigkeiten installieren

```bash
git clone https://github.com/FRYEL/PDF_converter_2.git
cd PDF_converter_2
```

Python-Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Node.js-Abhängigkeiten für Cypress installieren:

```bash
npm install
```

### 3️⃣ Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Hauptverzeichnis und füge folgende Schlüssel ein:

```
FLASK_SECRET_KEY=dein_geheimer_schlüssel
HUGGING_FACE_API_TOKEN=dein_huggingface_api_token
DL_API_KEY=dein_deepl_api_key
```

> **Hinweis:** Ersetze die Werte mit deinen eigenen API-Schlüsseln.

### 4️⃣ Anwendung starten

```bash
python app.py
```

Die Anwendung läuft dann unter:

```
http://127.0.0.1:5000
```

## 🎯 Nutzung

1️⃣ **PDF-Datei hochladen**  
2️⃣ **Zielsprache wählen**  
3️⃣ **"Process"-Button klicken**  
4️⃣ **Ergebnisse (Originaltext, Übersetzung, Zusammenfassung) abrufen**  

## 🛠 Tests mit Cypress

Die Anwendung enthält funktionale Tests, UI-Tests und API-Fehlermanagement mit **Cypress**.

### 1️⃣ Cypress installieren (falls nicht bereits geschehen)

```bash
npm install cypress --save-dev
```

### 2️⃣ Cypress Test Suite ausführen

```bash
npx cypress open
```

Dadurch öffnet sich das Cypress Test-Dashboard, wo die Tests gestartet werden können.

### 3️⃣ Automatische Testausführung im Terminal

```bash
npx cypress run
```

Dies führt die Tests im Terminal-Modus aus.

### 🧪 Beispiel für einen Cypress-Test

```javascript
describe("PDF Translator and Summarizer", () => {
    it("Lädt eine PDF-Datei hoch und verarbeitet sie", () => {
        cy.visit("http://127.0.0.1:5000");
        cy.get('input[type="file"]').attachFile("test.pdf");
        cy.get('select[name="target_lang"]').select("German");
        cy.get('button[type="submit"]').click();
        cy.get("#loading-overlay").should("be.visible");
        cy.get("#results", {timeout: 15000}).should("be.visible");
    });
});
```

## 📜 Lizenz

MIT-Lizenz – siehe [LICENSE](LICENSE) für Details.

---

📌 **Erstellt von:** Furkan Yel  
📌 **DHBW Stuttgart** – Fakultät Wirtschaft und Gesundheit, Studiengang Wirtschaftsinformatik
