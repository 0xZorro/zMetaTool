# JPG Metadata Functions – Detailed Explanation (English)

This document explains two key functions from `zMetaTool.py` for reading and writing EXIF metadata in JPG images.  
Each line is annotated and described in detail.

---

## Function: `read_JPGmeta(input_path)`

```python
# Reads and displays general EXIF metadata (Make, Model, Artist, etc.) using piexif.
# Only fields from the "0th" block are shown, which contain general image info.
def read_JPGmeta(input_path):
```
Reads EXIF metadata from JPG files – split into general and GPS sections.

```python
    try:
        exif_dict = piexif.load(input_path)
        zeroth_ifd = exif_dict.get("0th",{})
        gps_ifd = exif_dict.get("GPS")
```
`piexif.load(...)` loads all EXIF sections. `"0th"` contains general fields, `"GPS"` holds geolocation data.

```python
        if not zeroth_ifd:
            print("No general EXIF metadata found.")
            return
```
If no general metadata is found, the function exits.

```python
        print("\nJPG Metadata (EXIF via piexif):")
        for tag_id, value in zeroth_ifd.items():
            tag_name = piexif.TAGS["0th"][tag_id]["name"]
```
Converts numeric tag IDs (e.g. `271`) into human-readable names like `"Make"`.

```python
            # Decode byte strings for readability
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="ignore").strip()
            print(f"  {tag_name}: {value}")
```
Many EXIF fields are stored as byte strings – they are decoded for readability and printed.

```python
        print("GPS Metadata (via piexif):")
        for tag_id, value in gps_ifd.items():
            tag_name = piexif.TAGS["GPS"][tag_id]["name"]
```
GPS data is handled separately – it's stored in the `"GPS"` block of EXIF.

```python
            if tag_name == "GPSProcessingMethod" and isinstance(value, bytes):
                decoded = value.decode("ascii", errors="ignore").replace("\x00", " ")
                print(f"  {tag_name}: {decoded}")
            else:
                print(f"  {tag_name}: {value}")
```
Fields like `"GPSProcessingMethod"` are decoded from ASCII and cleaned of null bytes. Coordinates are shown as-is.

```python
    except Exception as e:
        print(f"Error reading GPS with piexif: {e}")
```
Error handling for robustness against unexpected metadata structures.

---

## Function: `write_JPGmeta(input_path, output_path, metadata_string=None)`

```python
# Writes or removes EXIF metadata from a JPG file using piexif.
# If no metadata string is provided, all metadata is stripped.
# The original file remains unchanged. The modified image is saved as 'modMeta.jpg'.
def write_JPGmeta(input_path, output_path, metadata_string=None):
```
Writes or deletes EXIF metadata – always operates on a copied file.

```python
        if metadata_string == None:
            shutil.copy2(input_path, output_path)
            piexif.remove(output_path)
            print("Metadata cleared. Modified file saved as 'modMeta.jpg'.")
            return
```
No metadata string?  
→ Copy original  
→ Remove metadata  
→ Only the copy is modified

```python
        else:
            shutil.copy2(input_path, output_path)
            exif_dict = piexif.load(output_path)
```
Original is copied and metadata is loaded from the copy.

```python
            meta_dict = {}
            pairs = metadata_string.split(";")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    meta_dict[key.strip()] = value.strip()
```
Parses input like `"Make=Canon;Model=EOS"` into a Python dictionary.

```python
            for key, value in meta_dict.items():
                value_bytes = value.encode("utf-8")
                for tag_id, tag_info in piexif.TAGS["0th"].items():
                    if tag_info["name"] == key:
                        exif_dict["0th"][tag_id] = value_bytes
```
Only fields from the `"0th"` block are supported (like `"Artist"` or `"Make"`). Strings are encoded as bytes.

```python
            exif_bytes = piexif.dump(exif_dict)
            image = Image.open(output_path)
            image.save(output_path, exif=exif_bytes, quality=95)
```
Final image is saved with new EXIF metadata.  
`quality=95` keeps image quality nearly intact.

```python
            print("Metadata updated. Modified file saved as 'modMeta.jpg'.")
```
Success message for the user.

---

## Note

Only fields from the `"0th"` EXIF block can currently be modified, including:

- `Make`, `Model`, `Software`, `Artist`, `DateTime`, `Copyright`

Writing GPS metadata is technically possible, but more complex – planned for future versions.

---

Documentation written by: Jose Luis Ocana (GitHub: [0xZorro](https://github.com/0xZorro))  
Last updated: Mai 2025

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---
