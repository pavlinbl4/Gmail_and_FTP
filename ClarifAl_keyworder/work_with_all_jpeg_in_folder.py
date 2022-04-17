from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from cred import key
from deep_translator import GoogleTranslator
import pyexiv2
from PIL import Image
import os


# models is   - 3df9e7b5c0f74a369919f6c0227afa08, aaa03c23b3724a16a56b629203edc62c, e68c9e00b9db49e2b5ba13934dc4a5ec, 2489aad78abf4b39a128fbbc64a8830c
# workin model  - aaa03c23b3724a16a56b629203edc62c , logo-detection-v2
def get_keywords(file_path):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    api_key = key
    metadata = (('authorization', f'Key {api_key}'),)

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    request = service_pb2.PostModelOutputsRequest(
        model_id='general-image-recognition',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    keywords = []
    for concept in response.outputs[0].data.concepts:
        keywords.append(concept.name)
    return keywords


def translate_english(keywords):  # принимает список с ключевыми словами
    return GoogleTranslator(source='en', target='ru').translate_batch(keywords)


def add_keywords(new_keywords, file_path):  # добавляет новые ключевые слова
    changes = {}
    with open(file_path, 'rb+') as image_file:
        with pyexiv2.ImageData(image_file.read()) as meta_data:
            data = meta_data.read_xmp()
            old_keywords = data.get('Xmp.dc.subject', [])
            changes['Xmp.dc.subject'] = list(set(old_keywords + new_keywords))
            meta_data.modify_xmp(changes)
            image_file.seek(0)
            image_file.truncate()
            image_file.write(meta_data.get_bytes())
        image_file.seek(0)


def choos_keywords(keywords):
    CRED = '\033[91m'
    CGREEN = '\33[0;32m'
    CEND = '\033[0m'
    BLINK = '\33[5m'
    good_words = []
    print(f"если слово подходит - нажмите 'ENTER'\n"
          f"если нет - то любую кнопку и 'ENTER' \n")
    for word in keywords:
        print(CRED + word + CEND)
        choise = input('_?_')
        if choise == '' \
                     '':
            good_words.append(word)
            print(f"слово {CGREEN}{word}{CEND} добавленно")
    print(good_words)
    return good_words


image_folder = "/Volumes/big4photo-2/My photo 2022/add_keywords"
files = os.listdir(image_folder)
for file in files:
    if file.endswith('.JPG'):
        file_path = f"{image_folder}/{file}"
        img = Image.open(file_path)
        img.show()

        new_keywords = translate_english(get_keywords(file_path))  # перевожу ключевые слова на русский
        new_keywords = [word.lower() for word in new_keywords]  # перевожу слова в нижний регистр
        new_keywords = choos_keywords(new_keywords)  # в ручную выбираю нужные ключевые слова

        add_keywords(new_keywords, file_path)
        img.close()

print("ALL DONE")
