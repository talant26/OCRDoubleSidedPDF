import os
import argparse

from recognizer import Recognizer
from utils import clean_tmp

# Parses the arguments
def get_parameters():

    parser = argparse.ArgumentParser(description='Process Double Sided PDFs with OCR and Deskewing.')

    parser.add_argument(
        "-l", "--languages",
        type=str,
        default="eng",
        help="Languages for text recognition, separate multiple values with + (e.g. 'eng+deu'). Default: 'eng'"
    )

    parser.add_argument(
        "-s", "--split",
        type=int,
        default=50,
        help="Where the page should be split (percentage). Default: 50"
    )

    args = parser.parse_args()
    return args.languages, args.split

# Loops through each PDF, checks wether it has already been scanned, and if
# not starts with the OCR-Process. Arguments: The list of PDFs
def loopThroughPDFs(pdfs):

    output_files = set(os.listdir('output/'))
    languages, split = get_parameters()

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

    # Search PDFs in the folder "input"
    pdfs = [f for f in sorted(os.listdir('input/')) if f.endswith('.pdf')]

    if len(pdfs) == 0:
        print('No files found.')
    else:
        # Start the script
        loopThroughPDFs(pdfs)

