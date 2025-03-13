This script is intended for double-sided PDF scans (like scientific papers). It splits the double-sided pages into individual pages, aligns them correctly and performs text recognition for the specified languages. 

## Features
- Splits **double-sided scanned PDFs** into separate pages  
- Automatically **deskews misaligned pages**  
- Uses **Tesseract OCR** to extract text from images  
- Supports **multiple languages** (e.g., `eng`, `deu`, `lat+eng`)  

## Requirements:
- See requirements.txt

## How to use
1. Place PDFS into the input folder. If the folder does not exist, either create it yourself or run the script once to automatically create it.
2. Run the script:
python main.py --languages LANGUAGES --split SPLIT

### Arguments:
- --languages (optional): Define the OCR-language. Default: "eng". A list of the languages to be recognized can be found here (separate several languages with a "+", e.g. lat+deu): https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
- --split (optional): Define whre the pages should be split (in %). Default: 50. The pages are normally separated in the middle. You can adjust the value as required so that the page is not split at 50, but e.g. at 55 or 60 percent.