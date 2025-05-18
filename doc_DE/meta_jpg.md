# JPG Metadata Functions – Detailed Explanation

Diese Datei dokumentiert zwei zentrale Funktionen aus `zMetaTool.py` zum Lesen und Schreiben von JPG-EXIF-Metadaten.  
Jede Zeile wird dabei kommentiert und erklärt.

---

## Function: `read_JPGmeta(input_path)`

```python
# Reads and displays general EXIF metadata (Make, Model, Artist, etc.) using piexif.
# Only fields from the "0th" block are shown, which contain general image info.
def read_JPGmeta(input_path):
```
Liest EXIF-Metadaten aus JPG-Dateien – aufgeteilt in allgemeine und GPS-Daten.

```python
    try:
        exif_dict = piexif.load(input_path)
        zeroth_ifd = exif_dict.get("0th",{})
        gps_ifd = exif_dict.get("GPS")
```
`piexif.load(...)` lädt alle Metadatenblöcke. `"0th"` enthält allgemeine EXIF-Felder, `"GPS"` die Koordinaten.

```python
        if not zeroth_ifd:
            print("No general EXIF metadata found.")
            return
```
Wenn keine allgemeinen EXIF-Daten vorhanden sind, wird abgebrochen.

```python
        print("\nJPG Metadata (EXIF via piexif):")
        for tag_id, value in zeroth_ifd.items():
            tag_name = piexif.TAGS["0th"][tag_id]["name"]
```
Übersetzt numerische Tag-IDs wie `271` in z. B. `"Make"`.

```python
            # Decode byte strings for readability
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="ignore").strip()
            print(f"  {tag_name}: {value}")
```
EXIF-Werte liegen oft als `bytes` vor – sie werden decodiert und formatiert ausgegeben.

```python
        print("GPS Metadata (via piexif):")
        for tag_id, value in gps_ifd.items():
            tag_name = piexif.TAGS["GPS"][tag_id]["name"]
```
GPS-Metadaten werden separat behandelt – EXIF speichert sie in einem anderen Block.

```python
            if tag_name == "GPSProcessingMethod" and isinstance(value, bytes):
                decoded = value.decode("ascii", errors="ignore").replace("\x00", " ")
                print(f"  {tag_name}: {decoded}")
            else:
                print(f"  {tag_name}: {value}")
```
Felder wie `"GPSProcessingMethod"` werden als ASCII decodiert und Nullbytes entfernt. Andere Werte (z. B. Koordinaten) werden direkt ausgegeben.

```python
    except Exception as e:
        print(f"Error reading GPS with piexif: {e}")
```
Fehlerbehandlung – sichert das Tool gegen unerwartete Metadatenformate ab.

---

## Function: `write_JPGmeta(input_path, output_path, metadata_string=None)`

```python
# Writes or removes EXIF metadata from a JPG file using piexif.
# If no metadata string is provided, all metadata is stripped.
# The original file remains unchanged. The modified image is saved as 'modMeta.jpg'.
def write_JPGmeta(input_path,output_path,metadata_string=None):
```
Schreibt EXIF-Metadaten oder entfernt sie – speichert immer eine Kopie.

```python
        if metadata_string == None:
            shutil.copy2(input_path,output_path)
            piexif.remove(output_path)
            print("Metadata cleared. Modified file saved as 'modMeta.jpg'.")
            return
```
Wenn keine Metadaten übergeben werden:  
→ Original kopieren  
→ Metadaten entfernen  
→ Nur die Kopie wird verändert

```python
        else:
            shutil.copy2(input_path,output_path)
            exif_dict = piexif.load(output_path)
```
Originalbild wird zuerst kopiert, dann Metadaten geladen.

```python
            meta_dict = {}
            pairs = metadata_string.split(";")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    meta_dict[key.strip()] = value.strip()
```
Übergabezeichenkette wie `"Make=Canon;Model=EOS"` wird in ein Dictionary umgewandelt.

```python
            for key, value in meta_dict.items():
                value_bytes = value.encode("utf-8")
                for tag_id, tag_info in piexif.TAGS["0th"].items():
                    if tag_info["name"] == key:
                        exif_dict["0th"][tag_id] = value_bytes
```
Nur erlaubte Felder aus dem `"0th"`-Block werden gesetzt (z. B. `"Artist"`, `"Make"`). Alles wird in `bytes` codiert.

```python
            exif_bytes = piexif.dump(exif_dict)
            image = Image.open(output_path)
            image.save(output_path,exif=exif_bytes,quality=95)
```
Die neuen EXIF-Daten werden serialisiert und mit Pillow in die Bilddatei geschrieben.  
Die `quality=95` sorgt für kaum sichtbaren Qualitätsverlust.

```python
            print("Metadata updated. Modified file saved as 'modMeta.jpg'.")
```
Abschlussmeldung an den Benutzer.

---

## Hinweis

Nur Felder aus dem `"0th"`-Block können derzeit beschrieben werden, z. B.:

- `Make`, `Model`, `Software`, `Artist`, `DateTime`, `Copyright`

GPS-Metadaten zu schreiben ist technisch möglich – aber deutlich komplexer und für spätere Versionen vorgesehen.

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: Mai 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---