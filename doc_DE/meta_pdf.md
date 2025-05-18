# PDF Metadata Functions – Detailed Explanation

Diese Datei dokumentiert zwei zentrale Funktionen aus `zMetaTool.py` zum Lesen und Schreiben von PDF-Metadaten.  
Jede Zeile wird dabei kommentiert und erklärt.

---

## Function: `read_PDFmeta(input_path)`

```python
# Reads and displays metadata from a PDF file.
# Extracts common metadata fields such as Title, Author, Subject, Creation Date, etc.
# If a field is missing, 'unknown' is displayed instead.
def read_PDFmeta(input_path):
```
Öffnet eine PDF-Datei und gibt strukturierte Metadaten aus.

```python
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
```
Datei wird im Binärmodus geöffnet. Der `PdfReader` lädt die Metadaten in ein Dictionary-ähnliches Objekt.

```python
    #Einzelne Metadaten herausholen
    title = metadata.get("/Title","unknown") 
    author = metadata.get("/Author","unknown")
    subject = metadata.get("/Subject","unknown")
    creation_date = metadata.get("/CreationDate","unknown")
    mod_date = metadata.get("/ModDate","unknown")
    creator = metadata.get("/Creator","unknown")
    producer = metadata.get("/Producer","unknown")
```
Jeder einzelne Standard-Metadatenwert wird abgefragt. Wenn ein Feld fehlt, wird `"unknown"` zurückgegeben.

```python
    print(f"""
        Title:    (Title)                       {title}
        Author:   (Author)                      {author}
        Subject:  (Subject)                     {subject}
        Created:  (CreationDate)               {creation_date}
        Modified: (ModDate)                    {mod_date}
        Creator Application:  (Creator)         {creator}
        PDF Producer: (Producer)                {producer}  """)
```
Die Metadaten werden formatiert ausgegeben. Jede Zeile zeigt das Feld und seinen Wert.

```python
    return metadata
```
Gibt die gesammelten Metadaten zurück – z. B. für Weiterverarbeitung oder Tests.

---

## Function: `write_PDFmeta(input_path, output_path, metadata_string=None)`

```python
# Writes or clears metadata in a PDF file.
# If no metadata string is provided, all existing metadata is removed.
# If a metadata string is provided (format: /Key=Value;/Key=Value), it is parsed and written to the PDF.
# The updated PDF is saved to the specified output path.
def write_PDFmeta(input_path, output_path, metadata_string=None):
```
Diese Funktion schreibt neue Metadaten oder löscht alle, wenn keine übergeben werden.

```python
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter(file)
```
PDF wird eingelesen, ein neuer Writer erzeugt eine Kopie.

```python
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)
```
Alle Seiten der Originaldatei werden in den Writer übernommen.

```python
        if metadata_string == None:
            writer.add_metadata({})
            print("Metadata cleared. Modified file saved as 'modMeta.pdf'.")
```
Wenn keine Metadaten übergeben wurden, wird der Metadatenblock geleert.

```python
        else:
            writer.add_metadata(parse_metadata_string(metadata_string))
            print("Metadata updated. Modified file saved as 'modMeta.pdf'.")
```
Wenn ein `metadata_string` vorhanden ist, wird dieser per Hilfsfunktion in ein Dictionary umgewandelt und angewendet.

```python
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
```
Die neue Datei mit den (neuen oder gelöschten) Metadaten wird unter dem neuen Pfad gespeichert.

---

## Hinweis

Die Funktion `parse_metadata_string(...)` zerlegt den String wie:

```text
"/Title=Mein PDF;/Author=Max"
```

...in ein Dictionary wie:

```python
{"/Title": "Mein PDF", "/Author": "Max"}
```

Damit ist die Eingabe leicht über die Kommandozeile möglich.

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: Mai 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---