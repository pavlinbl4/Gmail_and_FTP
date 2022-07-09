from PIL import Image
import imagehash
import csv
import os
import shutil


def move_file(test_image, etalon_file_name):
    print(etalon_image.split(".")[0])
    same_images_folder = f'{os.path.dirname(test_image)}/look_like_{etalon_file_name}'
    os.makedirs(same_images_folder, exist_ok=True)
    shutil.move(test_image, same_images_folder)


def mac_notification(message):
    title = "Task complete"
    command = f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
    os.system(command)


def extract_fie_name_from_link(image_link):
    return image_link.split('/')[-1]


def write_to_csv(test_image):
    with open("simular_images.csv", 'a') as input_file:
        writer = csv.writer(input_file)
        writer.writerow([etalon_image, test_image])


def compare_images(test_image, counter):
    hash0 = imagehash.average_hash(Image.open(etalon_image))
    hash1 = imagehash.average_hash(Image.open(test_image))
    cutoff = 10  # maximum bits that could be different between the hashes.

    if hash0 - hash1 < cutoff:
        print('images are similar')
        counter += 1
        etalon_file_name = extract_fie_name_from_link(etalon_image)
        write_to_csv(etalon_file_name)
        move_file(test_image, etalon_file_name)  # перемещаю похожий файл
    return counter


def all_file_in_folder(foldef_path):
    all_files = os.listdir(foldef_path)
    counter = 0
    for file in all_files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPG"):
            test_image = f"{foldef_path}/{file}"
            counter = compare_images(test_image, counter)
    write_to_csv("одинаковых снимков")
    mac_notification(f"найденно {counter} схожих снимков")


etalon_image = "/Users/evgeniy/Downloads/HR_image/KSP_017551_00105_0h.JPG"

all_file_in_folder("/Users/evgeniy/Downloads/test_images")
