# ============================================
# zMetaTool – Metadata Editor for PDF & JPG
# ============================================
# Author:      Jose Luis Ocana(GitHub: @0xZorro)
# Created:     2025-05-01
# Description: A Python tool to read, remove, or replace metadata in supported file types.
#              Currently supports PDF and JPG (EXIF). Designed for future extensions (e.g. DOCX, XLSX).
#              JPG support includes GPS data reading and general EXIF writing.
#
# License:     MIT License (see LICENSE file for details)
# Version:     1.0
# Repository:  https://github.com/0xZorro/zMetaTool
# ============================================

import PyPDF2
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from PIL import Image
import piexif
import shutil

# === Runtime variables ===
output_path_PDF = "modMeta.pdf"
output_path_JPG = "modMeta.jpg"

# Parses a semicolon-separated metadata string into a dictionary.
# Example input: "/Title=My PDF;/Author=Max"
# Returns: {"/Title": "My PDF", "/Author": "Max"}
def parse_metadata_string(meta_string):
    metadata = {}
    pairs = meta_string.split(";")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=",1)
            metadata[key.strip()] = value.strip()
    return metadata



# Reads and displays metadata from a PDF file.
# Extracts common metadata fields such as Title, Author, Subject, Creation Date, etc.
# If a field is missing, 'unknown' is displayed instead.
def read_PDFmeta(input_path):
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata      #Metadaten speichern

    #Einzelne Metadaten herausholen
    title = metadata.get("/Title","unknown") 
    author = metadata.get("/Author","unknown")
    subject = metadata.get("/Subject","unknown")
    creation_date = metadata.get("/CreationDate","unknown")
    mod_date = metadata.get("/ModDate","unknown")
    creator = metadata.get("/Creator","unknown")
    producer = metadata.get("/Producer","unknown")

    print(f"""
        Title:    (Title)                       {title}
        Author:   (Author)                      {author}
        Subject:  (Subject)                     {subject}
        Created:  (CreationDate)               {creation_date}
        Modified: (ModDate)                    {mod_date}
        Creator Application:  (Creator)         {creator}
        PDF Producer: (Producer)                {producer}  """)

    return metadata


# Reads and displays general EXIF metadata (Make, Model, Artist, etc.) using piexif.
# Only fields from the "0th" block are shown, which contain general image info.
def read_JPGmeta(input_path):
    try:
        exif_dict = piexif.load(input_path)
        zeroth_ifd = exif_dict.get("0th",{})
        gps_ifd = exif_dict.get("GPS")

        if not zeroth_ifd:
            print("No general EXIF metadata found.")
            return
        
        print("\nJPG Metadata (EXIF via piexif):")
        for tag_id, value in zeroth_ifd.items():
            tag_name = piexif.TAGS["0th"][tag_id]["name"]
            # Decode byte strings for readability
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="ignore").strip()
            print(f"  {tag_name}: {value}")
   
        print("GPS Metadata (via piexif):")
        for tag_id, value in gps_ifd.items():
            tag_name = piexif.TAGS["GPS"][tag_id]["name"]
            # Decode specific GPS metadata fields that are stored as byte strings with EXIF padding.
            # GPSProcessingMethod indicates how the location was determined (e.g. GPS, CELLID, WLAN).
            # These value are decoded from ASCII and cleaned of null bytes.
            if tag_name == "GPSProcessingMethod" and isinstance(value, bytes):
                decoded = value.decode("ascii", errors="ignore").replace("\x00", " ")
                print(f"  {tag_name}: {decoded}")
            else:
                print(f"  {tag_name}: {value}")
           
    except Exception as e:
        print(f"Error reading GPS with piexif: {e}")
    


# Writes or removes EXIF metadata from a JPG file using piexif.
# If no metadata string is provided, all metadata is stripped.
# The original file remains unchanged. The modified image is saved as 'modMeta.jpg'.
def write_JPGmeta(input_path,output_path,metadata_string=None):
    try:
        if metadata_string == None:
            # Step 1: Copy original file to output_path
            shutil.copy2(input_path,output_path)
            # Step 2: Remove EXIF metadata from the copied file
            piexif.remove(output_path)
            # Re-save image without EXIF data
            print("Metadata cleared. Modified file saved as 'modMeta.jpg'.")
            return
        else:
            # Step 1: Copy original file to output_path
            shutil.copy2(input_path,output_path)
            # Step 2: Load EXIF from copied image
            exif_dict = piexif.load(output_path)
            # Step 3: Parse metadata string into dictionary
            meta_dict = {}
            pairs = metadata_string.split(";")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    meta_dict[key.strip()] = value.strip()

            # Step 4: Insert values into "0th" IFD (main EXIF section)
            for key, value in meta_dict.items():
                value_bytes = value.encode("utf-8")

                for tag_id, tag_info in piexif.TAGS["0th"].items():
                    if tag_info["name"] == key:
                        exif_dict["0th"][tag_id] = value_bytes

            # Step 5: Save image with updated EXIF
            exif_bytes = piexif.dump(exif_dict)
            image = Image.open(output_path)
            image.save(output_path,exif=exif_bytes,quality=95)

            print("Metadata updated. Modified file saved as 'modMeta.jpg'.")

    except Exception as e:
        print(f"Error writing JPG metadata: {e}")



# Writes or clears metadata in a PDF file.
# If no metadata string is provided, all existing metadata is removed.
# If a metadata string is provided (format: /Key=Value;/Key=Value), it is parsed and written to the PDF.
# The updated PDF is saved to the specified output path.
def write_PDFmeta(input_path, output_path, metadata_string=None):
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        if metadata_string == None:
            writer.add_metadata({})
            print("Metadata cleared. Modified file saved as 'modMeta.pdf'.")
        else:
            writer.add_metadata(parse_metadata_string(metadata_string))
            print("Metadata updated. Modified file saved as 'modMeta.pdf'.")
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)





def main():
    parser = ArgumentParser(description ="""
zMetaTool -  Read or write metadata for supported file types (PDF, JPG).

Supported file types:
    - PDF
    - JPG

Valid metadata keys for PDF:
    /Title, /Author, /Subject, /Creator, /Producer, /CreationDate, /ModDate

Example PDF metadata input:
    "/Title=My PDF;/Author=Max;/CreationDate=D:20250517093000"

                            
Valid metadata tags for JPG (EXIF):
    - Make               (Camera manufacturer)
    - Model              (Camera model)
    - DateTimeOriginal   (Original date/time of photo)
    - DateTime           (File modification date/time)
    - Artist             (Photographer or creator)
    - Copyright          (Copyright notice)
    - Software           (Software used to create the image)
    - Orientation        (Image orientation)
    - GPSInfo            (GPS coordinates)
    - ExposureTime       (Shutter speed)
    - FNumber            (Aperture)
    - ISOSpeedRatings    (ISO value)
    - FocalLength        (Focal length)
    - Flash              (Flash fired or not)
    - ImageDescription   (Caption or description)
                            
Example JPG metadata input:
    "Make=Canon;Model=EOS 5D;Artist=Zorro;DateTimeOriginal=2025:05:17 14:30:00"
                            
Example usage:
    PDF:
        python zMetaTool.py file.pdf r
        python zMetaTool.py file.pdf w --metadata "/Title=Test;/Author=Zorro;/CreationDate=D:20250517120000"
                            
    JPG:
        python zMetaTool.py image.jpg r
        python zMetaTool.py image.jpg w --metadata "Make=Canon;Model=EOS 5D;Artist=Zorro;DateTimeOriginal=2025:05:17 14:30:00"
                      
    """,
    formatter_class=RawDescriptionHelpFormatter
)
    parser.add_argument("filePath", help="Path to the input PDF file")
    parser.add_argument("operation", help="Operation to perform: 'r' = read metadata, 'w' = write metadata") 
    parser.add_argument("-m", "--metadata", type=str, help="Metadata string to write into the PDF (example: \"/Title=My PDF;/Author=Max\")")
    args = parser.parse_args() 
    
    file_ext = os.path.splitext(args.filePath)[1].lower()  #os.path.splitext("test.jpg") → ("test", ".jpg")

    if args.operation == "r":
        if file_ext == ".pdf":
            read_PDFmeta(args.filePath)
        elif file_ext == ".jpg":
            read_JPGmeta(args.filePath)
        else:
            print("Unsupported file type for reading metadata.")
    elif args.operation == "w":
        if file_ext == ".pdf":
            write_PDFmeta(args.filePath,output_path_PDF,args.metadata)
        else:
            write_JPGmeta(args.filePath,output_path_JPG,args.metadata)
    else:
        print("Invalid option. Use 'r' to read metadata or 'w' to write metadata.")



if __name__ == "__main__":
   main()
