import os

# Images to pdf
from pdf2image import convert_from_path

# Slicing
from PIL import Image

# Deskewing
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew

# Images to PDFs
import pytesseract

# Merge PDFs
from pypdf import PdfWriter


class Recognizer:

    def __init__(self, pdfname, languages='eng', split=0.5):

        self.pdf_name = pdfname
        self.languages = languages
        self.split = split

    # Converts a pdf to single images
    def pdf_to_images(self):

        print('Starting with file ' + self.pdf_name)
        print('Converting pdf files to images. This may take a while...')
        convert_from_path('input/' + self.pdf_name, output_folder='tmp/images', output_file=self.pdf_name, fmt='png')
        print('Images created.')

    # Splits the images in two parts
    def image_slicer(self):

        print('Slicing images. This may take a while...')

        for file in sorted(os.listdir('tmp/images')):
            catIm = Image.open('tmp/images/' + file)
            # catIm.size[0] = width, catIm.size[1] = height
            # left, top, right, bottom
            lefthalf = catIm.crop((0, 0, catIm.size[0]*self.split/100, catIm.size[1]))
            lefthalf.save('tmp/slicedimages/' + file[:-4] + 'a.png')
            righthalf = catIm.crop((catIm.size[0]*self.split/100, 0, catIm.size[0], catIm.size[1]))
            righthalf.save('tmp/slicedimages/' + file[:-4] + 'b.png')
        print('Slicing completed.')

    # Deskews the sliced images
    def deskew_images(self):

        print('Deskewing images. This may take a while...')

        for file in sorted(os.listdir('tmp/slicedimages')):
            image = io.imread('tmp/slicedimages/' + file)
            grayscale = rgb2gray(image)
            angle = determine_skew(grayscale)
            rotated = rotate(image, angle, resize=True) * 255
            io.imsave('tmp/deskewedimages/' + file, rotated.astype(np.uint8))

        print('Deskewing completed.')

    # Does OCR for the images and converts them to single PDFs. Additionally creates a text-Version of the OCR-Text.
    def images_to_pdfs(self):

        print('Converting images to pdf files. This may take a while...')
        ocr_String = ''

        for file in sorted(os.listdir('tmp/deskewedimages')):
            try:
                ocr_String += pytesseract.image_to_string(Image.open('tmp/deskewedimages/'+file), lang=self.languages)
                pdf = pytesseract.image_to_pdf_or_hocr(Image.open('tmp/deskewedimages/'+file), lang=self.languages)
                with open('tmp/ocrcompletedpdfs/' + file[:-4] + '.pdf', 'w+b') as f:
                    f.write(pdf)
            except Exception as e:
                print('File ' + file + ' could not be converted to PDF. Skipping.')

        with open('output/'+self.pdf_name[:-4] + '.txt', 'w+') as f:
            f.write(ocr_String)

        print('PDFs converted.')

    # Combines the PDFs and saves them to the output folder
    def pdfs_to_pdf(self):

        print('Combining pdfs to a single file. This may take a while...')

        filelist = sorted(os.listdir('tmp/ocrcompletedpdfs'))

        writer = PdfWriter()

        for file in filelist:
            writer.append('tmp/ocrcompletedpdfs/' + file)

        writer.write("output/"+self.pdf_name)

        print(self.pdf_name + ' has been finished.')