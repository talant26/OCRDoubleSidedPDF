import os

from recognizer import Recognizer
from utils import clean_tmp, create_directories

# Prints the intro-text
def print_intro():
    print('''This script is intended for double-sided PDF scans (like scientific papers). It splits the double-sided pages into individual pages, aligns them correctly and performs text recognition for the specified languages. 

Procedure:
- Place the PDFs to be recognized in the “input” folder. You either have to create the folder or just run the mainscript once (than all folders are automatically created).
- Specify the language.
- The pages are normally separated in the middle. You can adjust the value as required so that the page is not split at 50, but at 55 or 60 percent.
- The results appear in the output folder.
########################################
''')

# Asks the user for input for the parameters languages and spplit
# languages(str) = Languages for Text Recognition
# Split(int) = Where the pdfs shall be split
def get_parameters():

    languages = input(
        'Please enter the languages to be recognized (default = “eng”).Separate multiple values with a "+" (e.g. "eng+lat").\nA list of the languages to be recognized can be found here (separate several languages with a "+", e.g. lat+deu):\nhttps://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html\n').strip()
    if not languages:
        print('Invalid input. Using default value ("eng").')
        languages = ('eng')

    try:
        split = int(input('Please specify where the pages should be separated. Default = 50 (=50 %)\n'))
    except ValueError:
        print('Invalid input. Using default value (50).')
        split = 50

    return languages, split

# Loops through each PDF, checks wether it has already been scanned, and if
# not starts with the OCR-Process. Arguments: The list of PDFs
def loopThroughPDFs(pdfs):


    output_files = set(os.listdir('output/'))
    languages, split = get_parameters()
    print(languages)

    for file in pdfs:
        if file in output_files:
            print('File "' + file + '" already exists in output-directory. Skipping.')
            continue

        clean_tmp()
        currentFile = Recognizer(file, languages=languages, split=split)
        currentFile.pdf_to_images()
        currentFile.image_slicer()
        currentFile.deskew_images()
        currentFile.images_to_pdfs()
        currentFile.pdfs_to_pdf()

    print('All files have been converted.')

if __name__ == '__main__':

    # Create necessary folders
    create_directories()

    # Print the introduction
    print_intro()

    # Search PDFs in the folder "input"
    pdfs = [f for f in sorted(os.listdir('input/')) if f.endswith('.pdf')]

    if len(pdfs) == 0:
        print('No files found.')
    else:
        # Start the script
        loopThroughPDFs(pdfs)

