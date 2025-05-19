<p align="center">
  <img src="Banner.png" alt="zMetaTool" width="300"/>
</p>

<p align="right">
  <a href="./README.md">Zur deutschen Version wechseln</a>
</p>

# zMetaTool – PDF & JPG Metadata Inspector

**zMetaTool** is a practical Python tool to read, delete, or selectively modify metadata in files.  
Currently supported file types: PDF documents and JPG images (including EXIF and GPS data).

> ⚠️ Note: This tool was created for **educational, documentation, and analysis purposes only**.  
> Do not use it to manipulate files without permission.

---

## Features

- Read, replace, or completely remove metadata from **PDF files**
- View EXIF metadata from **JPG images** – including location, camera, and software info
- GPS coordinates are shown in a structured (EXIF-compliant) format
- Deleting metadata always creates a **copy** (original remains unchanged)
- Clean command-line interface with argument parser and usage examples
- Easily extendable to Office formats, PNG, and more

---

## Motivation

This project was created to offer a lightweight, CLI-based tool for **metadata inspection and removal**,  
especially useful for privacy and security scenarios.

- How much hidden info do files carry?
- Which tools can safely inspect or erase metadata?
- How can we remove authorship or location information?

---

## Requirements

- Python 3.10 or higher
- Libraries: `PyPDF2`, `Pillow`, `piexif`

Install using:
```bash
pip install PyPDF2 pillow piexif
```

---

## Installation & Usage

1. Clone the repository or download the script:
```bash
git clone https://github.com/0xZorro/zMetaTool.git
```

2. Run the tool using example files:
```bash
python zMetaTool.py example.pdf r
python zMetaTool.py photo.jpg r
python zMetaTool.py example.pdf w --metadata "/Title=Demo;/Author=Zorro"
python zMetaTool.py photo.jpg w --metadata "Make=Canon;Model=EOS 90D"
```

---

## Command-Line Arguments

```bash
python zMetaTool.py <file> <operation> [--metadata "Key=Value;..."]
```

| Argument     | Meaning                                                            |
|--------------|---------------------------------------------------------------------|
| `file`       | Path to input file (PDF or JPG)                                    |
| `operation`  | `r` = read, `w` = write (set or remove metadata)                   |
| `--metadata` | (Optional) Metadata to set, format: `Key=Value;Key=Value;...`       |

If `--metadata` is not provided, all existing metadata will be removed.

---

## Example Output

```bash
Title:       Privacy Report
Author:      Max Mustermann
Creator:     LibreOffice 7.3
Producer:    PyPDF2
CreationDate: D:20240512123000
```

```bash
Make:         Canon
Model:        EOS 700D
GPSLatitude:  ((53, 1), (41, 1), (269033, 10000))
GPSLongitude: ((11, 1), (29, 1), (376618, 10000))
```

---

## Documentation

- [PDF Metadata – Read & Write (meta_pdf.md)](./doc_EN/meta_pdf_en.md)
- [JPG Metadata – Read & Write (meta_jpg.md)](./doc_EN/meta_jpg_en.md)

---

## Security Notes

Metadata can reveal sensitive information:

- GPS location
- Creator names, editing software
- Modification timestamps

**This tool helps you detect and remove such data when needed.**

---

## Planned Features

- `--list-fields` to list allowed metadata keys per file type
- Support for DOCX, XLSX, PNG, TIFF and more
- Validation and warnings for unsupported metadata keys
- Logging and optional silent mode
- Web frontend with drag & drop zone

---

## License

This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## Author

**Created by Jose Luis Ocana**

Cybersecurity Learner | Python & C++ Tools

(GitHub: [0xZorro](https://github.com/0xZorro))  
TryHackMe: https://tryhackme.com/p/0xZorro  
Contact: zorro.jose@gmx.de

---

## Contributions

Contributions are welcome!  
Feel free to fork the repo, make changes, and open a pull request.

---

## ⚠️ Legal Notice

This tool is intended for **educational, analysis, and demonstration purposes only**.  
It is **not designed** to obfuscate metadata for malicious use.

---

## Disclaimer

Use this tool **at your own risk**.  
The author accepts **no liability** for direct or indirect damage caused by this software.

Only use zMetaTool on files you are **legally authorized** to edit.

---

<div align="center">
  <img src="brand.png" alt="by 0xZorro" width="120"/>
  <br/>
  <sub>© 2025 0xZorro</sub>
</div>

---
