import os.path

# Clean the tmp directory and its subfolders
def clean_tmp():

    tmp_folder = 'tmp/'

    # Check if tmp-folder exists
    if not os.path.exists(tmp_folder):
        return

    # Loop trough subfolders an clean them
    for fileOrDirectory in os.listdir('tmp/'):

        filepath = os.path.join('tmp/', fileOrDirectory)

        if os.path.isdir(filepath):
            for file in os.listdir(filepath):
                os.remove(os.path.join(filepath, file))

def create_directories():
    folders = ['input', 'output', 'tmp', 'tmp/deskewedimages', 'tmp/images', 'tmp/ocrcompletedpdfs', 'tmp/slicedimages']

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

