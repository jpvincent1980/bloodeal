from os import path, listdir

from PIL import Image

from bloodeal.settings import BASE_DIR


images_directory = path.join(BASE_DIR, "images")
new_images_path = path.join(BASE_DIR, "images", "resized_images")
for file in listdir(images_directory):
    image_path = path.join(BASE_DIR, "images", file)
    if path.isfile(image_path):
        with Image.open(path.join(BASE_DIR, "images", file)) as image:
            if image.width > 100 or image.height > 150:
                output_size = (100, 150)
                image.thumbnail(output_size)
                image.save(path.join(BASE_DIR, "images", "resized_images", file))
