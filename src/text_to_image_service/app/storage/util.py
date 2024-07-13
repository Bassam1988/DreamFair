import os
from PIL import Image


def save_to_db(f, order, fs):
    try:
        fid = fs.put(f, filename=order)
        return fid
    except Exception as err:
        raise Exception("internal server error: " + str(err))


def save_to_folder(data):
    try:
        main_folder = data['media_folder']
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        reference = data['reference']
        text2image_operation_id = data['text2image_operation_id']
        order = data['order']
        subfolder_path = os.path.join(
            main_folder, str(reference), str(text2image_operation_id))
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        image_d = data['image']
        image = Image.open(image_d)
        if image.format is None:
            image.format = 'PNG'
        full_path = os.path.join(
            subfolder_path, f"{order}.{image.format.lower()}")
        image.save(full_path, format=image.format)

        return full_path

    except Exception as err:
        raise Exception("internal server error: " + str(err))


def save_image(data, db_or_folder=1, fs=None):
    if db_or_folder == 1:
        url = save_to_folder(data)
        return url
