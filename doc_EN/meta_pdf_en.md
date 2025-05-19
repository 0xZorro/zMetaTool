# PDF Metadata Functions – Detailed Explanation (English)

This document explains two essential functions from `zMetaTool.py` used for reading and writing PDF metadata.  
Each line of code is commented and described.

---

## Function: `read_PDFmeta(input_path)`

```python
# Reads and displays metadata from a PDF file.
# Extracts common metadata fields such as Title, Author, Subject, Creation Date, etc.
# If a field is missing, 'unknown' is displayed instead.
def read_PDFmeta(input_path):
```
Opens a PDF file and displays structured metadata.

```python
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
```
Opens the file in binary mode. `PdfReader` loads metadata into a dictionary-like object.

```python
    # Extract individual metadata fields
    title = metadata.get("/Title","unknown") 
    author = metadata.get("/Author","unknown")
    subject = metadata.get("/Subject","unknown")
    creation_date = metadata.get("/CreationDate","unknown")
    mod_date = metadata.get("/ModDate","unknown")
    creator = metadata.get("/Creator","unknown")
    producer = metadata.get("/Producer","unknown")
```
Each standard metadata field is queried. If missing, `"unknown"` is returned.

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
Prints the metadata in a formatted block. Each line shows the key and its value.

```python
    return metadata
```
Returns the collected metadata – useful for further processing or inspection.

---

## Function: `write_PDFmeta(input_path, output_path, metadata_string=None)`

```python
# Writes or clears metadata in a PDF file.
# If no metadata string is provided, all existing metadata is removed.
# If a metadata string is provided (format: /Key=Value;/Key=Value), it is parsed and written to the PDF.
# The updated PDF is saved to the specified output path.
def write_PDFmeta(input_path, output_path, metadata_string=None):
```
This function writes new metadata or clears all if none is provided.

```python
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter(file)
```
Reads the PDF and prepares a writer for creating a copy.

```python
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)
```
All pages from the original PDF are added to the new writer.

```python
        if metadata_string == None:
            writer.add_metadata({})
            print("Metadata cleared. Modified file saved as 'modMeta.pdf'.")
```
If no metadata string is passed, all metadata is removed (empty dictionary).

```python
        else:
            writer.add_metadata(parse_metadata_string(metadata_string))
            print("Metadata updated. Modified file saved as 'modMeta.pdf'.")
```
If metadata is provided as a string, it is parsed into a dictionary and applied.

```python
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
```
Saves the modified PDF (with updated or cleared metadata) to the given output path.

---

## Note

The function `parse_metadata_string(...)` converts a string like:

```text
"/Title=My PDF;/Author=Max"
```

...into a dictionary:

```python
{"/Title": "My PDF", "/Author": "Max"}
```

This makes it easy to pass metadata directly from the command line.

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: Mai 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---