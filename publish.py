# touch export/O515567L2J_IMG_Neki_Nok1.jpg && touch export/O515567L2J_IMG_Neki_Nok2.jpg && touch export/O515567L2J_IMG_Neki_Nok3.jpg && touch export/98PP8ZB9AI_IMG_37293_1.jpg && touch export/98PP8ZB9AI_IMG_37293_2.jpg 

# Prekopiraš vse iz export v publish v folder z imenom kode
# Vsako sliko še shraniš pomajšano, velikost 600px, 85% JPG compressoin po najdaljši stranici in ji daš ime: "(original_ime).thumb.jpg"
# Ustvariš ZIP datoteko v mapi z imenom kode, ZIP ime naj bo "(koda)_Slike.zip", notri daš vse original slike.

import os
import shutil
import zipfile
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def move_files_to_code_folders(export_path, publish_path):
    # Check if export folder exists
    if not os.path.exists(export_path):
        print(f"Export folder '{export_path}' does not exist.")
        return

    # Iterate through each file in the export folder
    for file in os.listdir(export_path):
        if file.endswith(".jpg") or file.endswith(".png"):  # Check if the file is an image
            code = file.split('_')[0]  # Extract 'code' from the file name
            code_folder_path = os.path.join(publish_path, code)  # Path for the 'code' folder in 'publish'

            # Create 'code' folder if it does not exist
            if not os.path.exists(code_folder_path):
                os.makedirs(code_folder_path)

            # Move file to the 'code' folder
            shutil.move(os.path.join(export_path, file), os.path.join(code_folder_path, file))

def zip_images(code_folder_path, code):
    """
    Create a ZIP archive of all the original images in the code folder.
    The ZIP file is named "sv-Stefan_{code}_slike.zip".
    """
    zip_filename = f"{code}_svStefan_slike.zip"
    zip_filepath = os.path.join(code_folder_path, zip_filename)
    
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for file in os.listdir(code_folder_path):
            if file.endswith(".jpg") or file.endswith(".png"):
                # Include only original images, not thumbnails
                if not file.endswith(".thumb.jpg"):
                    zipf.write(os.path.join(code_folder_path, file), file)


def resize_image_with_compression(image_path, output_path, max_size=600, quality=80):
    """
    Resize the image, maintaining aspect ratio, so that its longest side is `max_size` pixels,
    and save it with JPEG compression at the specified quality level.
    """
    with Image.open(image_path) as img:
        # Calculate the new size maintaining aspect ratio
        ratio = max_size / max(img.size)
        new_size = tuple([int(x * ratio) for x in img.size])

        # Resize the image
        resized_img = img.resize(new_size, resample=Image.LANCZOS)

        # Save the resized image with JPEG compression
        resized_img.save(output_path, quality=quality, optimize=True)

def move_resize_and_zip_images(export_path, publish_path):
    # Keep track of the codes processed
    processed_codes = set()

    # Check if export folder exists
    if not os.path.exists(export_path):
        print(f"Export folder '{export_path}' does not exist.")
        return

    # Iterate through each file in the export folder
    for file in os.listdir(export_path):
        if file.endswith(".jpg") or file.endswith(".png"):  # Check if the file is an image
            code = file.split('_')[0]  # Extract 'code' from the file name
            processed_codes.add(code)
            code_folder_path = os.path.join(publish_path, code)  # Path for the 'code' folder in 'publish'

            # Create 'code' folder if it does not exist
            if not os.path.exists(code_folder_path):
                os.makedirs(code_folder_path)

            # Full path for the original and the thumbnail image
            original_path = os.path.join(export_path, file)
            publish_code_path = os.path.join(code_folder_path, file)
            thumbnail_path = os.path.join(code_folder_path, file.rsplit('.', 1)[0] + ".thumb.jpg")

            # Move the original file to the 'code' folder
            shutil.move(original_path, publish_code_path)

            # Create and save the thumbnail with compression
            resize_image_with_compression(publish_code_path, thumbnail_path)

    # After moving all files, create ZIP archives for each code
    for code in processed_codes:
        zip_images(os.path.join(publish_path, code), code)


# move_resize_and_zip_images(os.getenv('LIGHTROOM_OUT_FOLDER'), os.getenv('PUBLISH_FOLDER'))