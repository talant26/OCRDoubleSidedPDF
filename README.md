This script is intended for double-sided PDF scans (like scientific papers). It splits the double-sided pages into individual pages, aligns them correctly and performs text recognition for the specified languages. 

Procedure:
- Place the PDFs to be recognized in the “input” folder. You either have to create the folder yourself or just run the mainscript once (than all folders are automatically created).
- Specify the language. A list of the languages to be recognized can be found here (separate several languages with a "+", e.g. lat+deu): https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
- The pages are normally separated in the middle. You can adjust the value as required so that the page is not split at 50, but e.g. at 55 or 60 percent.
- The results appear in the output folder.

Requirements:
- See requirements.txt
